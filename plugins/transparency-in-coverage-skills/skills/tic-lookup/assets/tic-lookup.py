#!/usr/bin/env python3
"""
Transparency in Coverage - Price Lookup Tool

Indexes CMS machine-readable In-Network JSON files into a SQLite database,
then provides fast lookups by Payer / Plan / NPI / CPT code.

Usage:
    # Download source files (conditional GET, skips files already up to date)
    python tic_lookup.py --download

    # Build the index (auto-downloads any missing source files first)
    python tic_lookup.py --build

    # Query examples
    python tic_lookup.py --payer Aetna --cpt 99213
    python tic_lookup.py --payer Aetna --plan AetnaEPO --npi 1013915255 --cpt 99213
    python tic_lookup.py --npi 1013915255
    python tic_lookup.py --cpt 27447

    # Export results to CSV
    python tic_lookup.py --cpt 27447 --csv results.csv

    # Filter to non-zero rates only
    python tic_lookup.py --cpt 27447 --nonzero

    # Summary view (min/max/avg per plan)
    python tic_lookup.py --cpt 27447 --summary
"""

import argparse
import csv
import json
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR    = Path(__file__).resolve().parent
INNETWORK_DIR = SCRIPT_DIR / "InNetwork"
NPI_DIR       = SCRIPT_DIR / "NPI"
_default_db   = SCRIPT_DIR / "tic_index.db"
DB_PATH       = Path(os.environ.get("TIC_DB_PATH", str(_default_db)))

TIC_BASE_URL = os.environ.get(
    "TIC_DATA_URL",
    "https://inov8public.z21.web.core.windows.net/Insurance/",
)
TIC_FILES = [
    "InNetwork/Aetna/AetnaEPO.json",
    "InNetwork/Aetna/AetnaPPO.json",
    "InNetwork/BCBS/BCBSTX_HMO.json",
    "InNetwork/BCBS/BCBSTX_PPO.json",
    "InNetwork/Cigna/CignaPPO.json",
    "InNetwork/Cigna/CignaSouthTXHMO.json",
    "InNetwork/UHC/UnitedHMO.json",
    "InNetwork/UHC/UnitedPPO.json",
    "NPI/houstonmetro.csv",
]
CACHE_PATH = SCRIPT_DIR / ".tic-cache.json"

# -----------------------------------------------------------------------
# DOWNLOAD
# -----------------------------------------------------------------------

def _human_size(n):
    n = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.1f %s" % (n, unit)
        n /= 1024
    return "%.1f TB" % n

def _load_cache():
    if not CACHE_PATH.exists():
        return {}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def _save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, sort_keys=True)

def _download_one(rel_path, cache, force=False):
    """Fetch one file with conditional GET. Returns 'updated', 'unchanged', or 'error'."""
    url  = TIC_BASE_URL.rstrip("/") + "/" + rel_path
    dest = SCRIPT_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(url)
    if not force and dest.exists():
        meta = cache.get(rel_path, {})
        if meta.get("etag"):
            req.add_header("If-None-Match", meta["etag"])
        if meta.get("last_modified"):
            req.add_header("If-Modified-Since", meta["last_modified"])

    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            etag = resp.headers.get("ETag")
            lm   = resp.headers.get("Last-Modified")
            tmp  = dest.with_suffix(dest.suffix + ".part")
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, dest)
            cache[rel_path] = {"etag": etag, "last_modified": lm}
            print("  %-44s  updated  (%s)" % (rel_path, _human_size(len(data))))
            return "updated"
    except urllib.error.HTTPError as e:
        if e.code == 304:
            print("  %-44s  up to date" % rel_path)
            return "unchanged"
        print("  %-44s  ERROR: HTTP %s" % (rel_path, e.code), file=sys.stderr)
        return "error"
    except urllib.error.URLError as e:
        print("  %-44s  ERROR: %s" % (rel_path, e.reason), file=sys.stderr)
        return "error"

def download_all(force=False):
    print("Downloading TiC source files from %s" % TIC_BASE_URL)
    cache = _load_cache()
    counts = {"updated": 0, "unchanged": 0, "error": 0}
    for rel in TIC_FILES:
        counts[_download_one(rel, cache, force=force)] += 1
    _save_cache(cache)
    print("\n%d updated, %d unchanged, %d error(s)." %
          (counts["updated"], counts["unchanged"], counts["error"]))
    return counts["error"] == 0

def _missing_source_files():
    return [rel for rel in TIC_FILES if not (SCRIPT_DIR / rel).exists()]

# -----------------------------------------------------------------------
# BUILD
# -----------------------------------------------------------------------

def init_db(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS prices;
        DROP TABLE IF EXISTS npi_registry;
        CREATE TABLE prices (
            id INTEGER PRIMARY KEY,
            payer TEXT NOT NULL, plan TEXT NOT NULL,
            billing_code TEXT NOT NULL, billing_code_type TEXT NOT NULL,
            name TEXT, description TEXT,
            negotiated_rate REAL NOT NULL, negotiated_type TEXT,
            billing_class TEXT, setting TEXT,
            expiration_date TEXT, service_codes TEXT, modifiers TEXT,
            npi INTEGER NOT NULL, tin_type TEXT, tin_value TEXT,
            negotiation_arrangement TEXT
        );
        CREATE TABLE npi_registry (
            npi INTEGER PRIMARY KEY, entity_type INTEGER,
            organization_name TEXT, last_name TEXT, first_name TEXT,
            credential TEXT, address_line1 TEXT, city TEXT,
            state TEXT, zip TEXT, taxonomy1 TEXT
        );
    """)

def load_npi_csv(conn):
    csv_files = list(NPI_DIR.glob("*.csv"))
    if not csv_files:
        print("  Warning: No NPI CSV files found in NPI/")
        return
    total = 0
    for csv_path in csv_files:
        print("  Loading NPI data from %s..." % csv_path.name)
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                rows.append((
                    int(row["NPI"]),
                    int(row.get("EntityTypeCode", 0) or 0),
                    row.get("ProviderOrganizationName", ""),
                    row.get("ProviderLastName", ""),
                    row.get("ProviderFirstName", ""),
                    row.get("ProviderCredentialText", ""),
                    row.get("ProviderFirstLineBusinessPracticeLocationAddress", ""),
                    row.get("ProviderBusinessPracticeLocationAddressCityName", ""),
                    row.get("ProviderBusinessPracticeLocationAddressStateName", ""),
                    row.get("ProviderBusinessPracticeLocationAddressPostalCode", ""),
                    row.get("TaxonomyCode1", ""),
                ))
            conn.executemany("INSERT OR IGNORE INTO npi_registry VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
            total += len(rows)
    print("  Loaded %s NPI records" % "{:,}".format(total))

def index_file(conn, json_path, payer, plan):
    """Parse one In-Network JSON file and insert price rows.

    Handles both provider-reference patterns:
      1. Root-level provider_references array with integer IDs.
      2. Inline provider_groups on each negotiated_rate entry.
    """
    print("  Indexing %s/%s..." % (payer, plan))
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build provider_group_id -> deduplicated (npi, tin_type, tin_value)
    prov_lookup = {}
    for pr in data.get("provider_references", []):
        gid = pr["provider_group_id"]
        entries = []
        seen = set()
        for pg in pr.get("provider_groups", []):
            tin_type  = pg.get("tin", {}).get("type", "")
            tin_value = pg.get("tin", {}).get("value", "")
            for npi in pg.get("npi", []):
                key = (npi, tin_type, tin_value)
                if key not in seen:
                    seen.add(key)
                    entries.append(key)
        prov_lookup[gid] = entries

    rows = []
    for item in data.get("in_network", []):
        bc   = item.get("billing_code", "")
        bct  = item.get("billing_code_type", "")
        nm   = item.get("name", "")
        desc = item.get("description", "")
        arr  = item.get("negotiation_arrangement", "")

        for nr in item.get("negotiated_rates", []):
            provs = []
            for ref_id in nr.get("provider_references", []):
                provs.extend(prov_lookup.get(ref_id, []))
            for pg in nr.get("provider_groups", []):
                tt = pg.get("tin", {}).get("type", "")
                tv = pg.get("tin", {}).get("value", "")
                for npi in pg.get("npi", []):
                    provs.append((npi, tt, tv))

            for price in nr.get("negotiated_prices", []):
                rate     = price.get("negotiated_rate", 0)
                nt       = price.get("negotiated_type", "")
                bc2      = price.get("billing_class", "")
                st       = price.get("setting", "")
                exp      = price.get("expiration_date", "")
                sc       = ",".join(price.get("service_code", []))
                mod      = ",".join(price.get("billing_code_modifier", []))
                base     = (payer, plan, bc, bct, nm, desc, rate, nt, bc2, st, exp, sc, mod)

                if not provs:
                    rows.append(base + (0, "", "", arr))
                else:
                    for (npi, tt, tv) in provs:
                        rows.append(base + (npi, tt, tv, arr))

    conn.executemany(
        """INSERT INTO prices (payer,plan,billing_code,billing_code_type,
           name,description,negotiated_rate,negotiated_type,billing_class,
           setting,expiration_date,service_codes,modifiers,
           npi,tin_type,tin_value,negotiation_arrangement)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        rows)
    print("    -> %s price rows" % "{:,}".format(len(rows)))

def build_index():
    missing = _missing_source_files()
    if missing:
        print("%d source file(s) missing — fetching first..." % len(missing))
        if not download_all(force=False):
            print("Some downloads failed. Aborting build.", file=sys.stderr)
            sys.exit(1)
        print("")
    print("Building index -> %s" % DB_PATH)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=OFF")
    init_db(conn)
    load_npi_csv(conn)
    for payer_dir in sorted(INNETWORK_DIR.iterdir()):
        if not payer_dir.is_dir():
            continue
        for jf in sorted(payer_dir.glob("*.json")):
            index_file(conn, jf, payer_dir.name, jf.stem)
    print("  Creating indexes...")
    conn.executescript("""
        CREATE INDEX idx_cpt  ON prices(billing_code);
        CREATE INDEX idx_npi  ON prices(npi);
        CREATE INDEX idx_pay  ON prices(payer);
        CREATE INDEX idx_plan ON prices(plan);
        CREATE INDEX idx_comp ON prices(payer,plan,billing_code,npi);
    """)
    conn.commit()
    rc = conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
    nc = conn.execute("SELECT COUNT(*) FROM npi_registry").fetchone()[0]
    print("\nDone. %s price rows, %s NPI records." % ("{:,}".format(rc), "{:,}".format(nc)))
    conn.close()

# -----------------------------------------------------------------------
# QUERY
# -----------------------------------------------------------------------

def query_prices(payer=None, plan=None, npi=None, cpt=None, nonzero=False, limit=500):
    if not DB_PATH.exists():
        print("Error: Index not found. Run with --build first.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    clauses, params = [], []
    if payer:
        clauses.append("p.payer = ?"); params.append(payer)
    if plan:
        clauses.append("p.plan = ?"); params.append(plan)
    if npi:
        clauses.append("p.npi = ?"); params.append(int(npi))
    if cpt:
        clauses.append("p.billing_code = ?"); params.append(str(cpt))
    if nonzero:
        clauses.append("p.negotiated_rate > 0")
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = """
        SELECT p.payer, p.plan,
               p.billing_code AS cpt, p.billing_code_type AS code_type,
               p.name AS service_name,
               p.negotiated_rate AS rate, p.negotiated_type AS rate_type,
               p.billing_class, p.setting, p.expiration_date,
               p.npi, p.tin_value AS tin,
               p.negotiation_arrangement AS arrangement,
               n.organization_name AS org_name,
               n.last_name AS provider_last, n.first_name AS provider_first,
               n.city AS provider_city, n.state AS provider_state,
               n.taxonomy1 AS taxonomy
        FROM prices p LEFT JOIN npi_registry n ON p.npi = n.npi
        %s
        ORDER BY p.payer, p.plan, p.billing_code, p.negotiated_rate
        LIMIT ?
    """ % where
    params.append(limit)
    results = [dict(row) for row in conn.execute(sql, params)]
    conn.close()
    return results

def rate_summary(cpt, payer=None):
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    clauses = ["billing_code = ?", "negotiated_rate > 0"]
    params = [str(cpt)]
    if payer:
        clauses.append("payer = ?"); params.append(payer)
    sql = """
        SELECT payer, plan,
               MIN(negotiated_rate) AS min_rate,
               MAX(negotiated_rate) AS max_rate,
               ROUND(AVG(negotiated_rate),2) AS avg_rate,
               COUNT(*) AS cnt
        FROM prices WHERE %s
        GROUP BY payer, plan ORDER BY payer, plan
    """ % " AND ".join(clauses)
    results = [dict(row) for row in conn.execute(sql, params)]
    conn.close()
    return results

def print_results(results, csv_path=None):
    if not results:
        print("No results found.")
        return
    if csv_path:
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=results[0].keys())
            w.writeheader()
            w.writerows(results)
        print("Wrote %d rows to %s" % (len(results), csv_path))
        return
    hdr = "%-8s %-20s %-8s %10s %-12s %-14s %-12s %-30s %-15s" % (
        "Payer","Plan","CPT","Rate","Type","Class","NPI","Provider","City")
    print(hdr)
    print("-" * len(hdr))
    for r in results:
        prov = r["org_name"] or ""
        if not prov:
            last = r["provider_last"] or ""
            first = r["provider_first"] or ""
            prov = ("%s, %s" % (last, first)).strip(", ") if last or first else "-"
        if len(prov) > 28:
            prov = prov[:27] + "."
        print("%-8s %-20s %-8s %10.2f %-12s %-14s %-12s %-30s %-15s" % (
            r["payer"], r["plan"], r["cpt"], r["rate"],
            r["rate_type"], r["billing_class"], str(r["npi"]),
            prov, r["provider_city"] or "-"))
    print("\n(%d rows)" % len(results))

# -----------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------

def list_available(field):
    if not DB_PATH.exists():
        print("Error: Index not found. Run with --build first.", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    vals = [r[0] for r in conn.execute("SELECT DISTINCT %s FROM prices ORDER BY %s" % (field, field))]
    conn.close()
    return vals

def main():
    p = argparse.ArgumentParser(description="TiC In-Network Price Lookup",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("--build", action="store_true", help="Rebuild SQLite index (auto-downloads missing source files)")
    p.add_argument("--download", action="store_true", help="Download source files (conditional GET via ETag/Last-Modified)")
    p.add_argument("--force", action="store_true", help="With --download, re-fetch files even if up to date")
    p.add_argument("--payer", type=str, help="Filter by payer (folder name)")
    p.add_argument("--plan", type=str, help="Filter by plan (file stem)")
    p.add_argument("--npi", type=str, help="Filter by NPI number")
    p.add_argument("--cpt", type=str, help="Filter by billing/CPT code")
    p.add_argument("--nonzero", action="store_true", help="Exclude zero-dollar rates")
    p.add_argument("--limit", type=int, default=500, help="Max rows (default 500)")
    p.add_argument("--csv", type=str, help="Export results to CSV file")
    p.add_argument("--summary", action="store_true", help="Show min/max/avg per plan")
    p.add_argument("--list-payers", action="store_true", help="List available payers")
    p.add_argument("--list-plans", action="store_true", help="List available plans")
    p.add_argument("--list-cpts", action="store_true", help="List available CPT codes")
    args = p.parse_args()

    if args.download:
        ok = download_all(force=args.force)
        sys.exit(0 if ok else 1)
    if args.build:
        build_index()
        return
    if args.list_payers:
        for v in list_available("payer"): print(v)
        return
    if args.list_plans:
        for v in list_available("plan"): print(v)
        return
    if args.list_cpts:
        for v in list_available("billing_code"): print(v)
        return
    if args.summary and args.cpt:
        rows = rate_summary(args.cpt, payer=args.payer)
        if not rows:
            print("No results.")
            return
        print("%-8s %-20s %10s %10s %10s %7s" % ("Payer","Plan","Min","Max","Avg","Count"))
        print("-" * 70)
        for r in rows:
            print("%-8s %-20s %10.2f %10.2f %10.2f %7s" % (
                r["payer"], r["plan"], r["min_rate"], r["max_rate"],
                r["avg_rate"], "{:,}".format(r["cnt"])))
        return
    if not any([args.payer, args.plan, args.npi, args.cpt]):
        p.print_help()
        return
    results = query_prices(payer=args.payer, plan=args.plan,
                           npi=args.npi, cpt=args.cpt,
                           nonzero=args.nonzero, limit=args.limit)
    print_results(results, csv_path=args.csv)

if __name__ == "__main__":
    main()