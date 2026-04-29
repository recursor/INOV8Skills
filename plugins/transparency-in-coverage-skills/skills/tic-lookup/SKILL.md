---
name: tic-lookup
description: >
  Transparency in Coverage (TiC) price lookup tool for querying CMS machine-readable
  in-network rate files. Use this skill whenever the user asks about insurance reimbursement
  rates, negotiated rates, payer pricing, price transparency data, facility rate comparisons,
  or wants to look up what insurance plans pay for specific CPT/HCPCS codes. Also trigger
  when the user mentions TiC files, in-network rates, price transparency, payer/plan rate
  lookups, or wants to compare reimbursement across hospitals, ASCs, or providers. Even if
  the user just asks "what does Aetna pay for a knee replacement" or "compare facility rates
  for CPT 27447", use this skill. This skill handles indexing, querying, and summarizing —
  it does NOT generate reports or presentations (use the pptx or xlsx skills for that).
---

# TiC Price Lookup Skill

## What This Skill Does

This skill indexes and queries CMS Transparency in Coverage (TiC) machine-readable
In-Network JSON files. It builds a SQLite database from pre-filtered JSON files organized
by payer/plan, then provides fast lookups by any combination of Payer, Plan, NPI, and
CPT/HCPCS code.

## Data Layout

The skill expects data in the user's workspace folder with this structure:

```
<workspace>/
├── InNetwork/
│   ├── <Payer>/          # e.g., Aetna, BCBS, Cigna, UHC
│   │   ├── <Plan>.json   # e.g., AetnaEPO.json, AetnaPPO.json
│   │   └── ...
│   └── ...
├── NPI/
│   └── *.csv             # NPI registry exports (from NPPES)
└── tic_lookup.py          # The query tool (copy from scripts/ if not present)
```

The JSON files follow the CMS TiC schema (v2.0) and should already be filtered to the
CPTs and provider NPIs of interest — raw TiC files from insurers can be hundreds of GB.

## How to Use

### Step 1: Ensure tic_lookup.py Is in the Workspace

If the user's workspace doesn't have `tic_lookup.py`, copy it from this skill's
`scripts/` directory:

```bash
cp <skill-path>/scripts/tic_lookup.py <workspace>/tic_lookup.py
```

### Step 2: Build the Index

The SQLite index must be built before querying. Run:

```bash
cd <workspace>
python3 tic_lookup.py --build
```

**Important:** In sandboxed environments where the mounted workspace doesn't support
SQLite WAL mode, set the `TIC_DB_PATH` environment variable to write the database to
a writable location:

```bash
TIC_DB_PATH=/tmp/tic_index.db python3 tic_lookup.py --build
```

Then use that same env var for all subsequent queries.

The index only needs rebuilding when the source JSON files change.

### Step 3: Query

Common query patterns:

```bash
# Look up rates for a specific CPT code
python3 tic_lookup.py --cpt 27447 --nonzero

# Look up rates for a specific provider (by NPI)
python3 tic_lookup.py --npi 1831551266 --nonzero

# Filter by payer and CPT
python3 tic_lookup.py --payer Aetna --cpt 27447 --nonzero

# Full filter: payer + plan + NPI + CPT
python3 tic_lookup.py --payer Aetna --plan AetnaEPO --npi 1831551266 --cpt 27447

# Summary view (min/max/avg per plan)
python3 tic_lookup.py --cpt 27447 --summary

# Export to CSV for further analysis
python3 tic_lookup.py --cpt 27447 --nonzero --csv results.csv

# List what's available
python3 tic_lookup.py --list-payers
python3 tic_lookup.py --list-plans
python3 tic_lookup.py --list-cpts
```

### Key Concepts

**Billing class matters.** Rates come in two billing classes:
- `institutional` — facility fees (what the hospital/ASC charges)
- `professional` — physician fees (what the surgeon charges)

When comparing facility reimbursement, always filter to `institutional` rates. The
`--nonzero` flag filters out $0 placeholder rates.

**Negotiated rate types:**
- `negotiated` — standard contracted rate
- `derived` — calculated from other rates
- `fee schedule` — based on a fee schedule (e.g., Medicare)
- `percentage` — percentage of billed charges
- `per diem` — daily rate

**Provider identification:** Each provider has an NPI (National Provider Identifier).
Facilities (hospitals, ASCs) are entity type 2. Individual physicians are entity type 1.

## Known Facility Registry

The following Houston-area hospitals and ASCs are pre-registered for quick reference.
When the user asks to compare "top hospitals" or "top ASCs", use these NPIs rather
than searching — they've been verified against the TiC data.

### Hospitals

| Facility | NPI | Notes |
|----------|-----|-------|
| Texas Orthopedic Hospital | 1134166192 | 7401 S Main St, Bellaire/Medical Center. "Orthopedic Hospital Ltd" in NPI registry. |
| Houston Methodist Hospital (TMC) | 1548387418 | 6565 Fannin St. "The Methodist Hospital" in NPI registry. |
| Houston Methodist St. John Hospital | 1952723967 | 18300 Houston Methodist Dr. |
| Memorial Hermann Hospital (TMC) | 1982666111 | 6411 Fannin St. |
| Memorial Hermann Memorial City | 1740233782 | 921 Gessner Rd. |
| Memorial Hermann Greater Heights | 1730132234 | 1635 North Loop W. |
| Baylor St. Luke's Medical Center | 1841690740 | "CHI St. Luke's Health Baylor St. Luke's Medical Center" in registry. |

### Ambulatory Surgery Centers (ASCs)

| Facility | NPI | Notes |
|----------|-----|-------|
| INOV8 Surgical | 1831551266 | "INOV8 Surgical at Memorial City". Has both institutional and professional rates. |
| Kelsey-Seybold Medical Group | 1013915255 | All Kelsey-Seybold ASCs (Berthelsen, Memorial Villages, Springwoods Village, Fort Bend) bill under this single NPI. Professional rates only in current data. |
| Physicians Ambulatory Surgery Center | 1902036049 | Institutional + professional data. |
| Memorial Ambulatory Surgery Center (MASC) | 1750842209 | Institutional + professional data. |
| Houston Surgery Center | 1558782268 | Institutional + professional data. |
| Cy Fair Surgery Center | 1639195217 | Institutional + professional data. |
| Houston Premier Surgery Center | 1548827637 | "Hedwig ASC" in local NPI registry. 8731 Katy Fwy. Institutional data. |
| TOPS Specialty Hospital | 1144203662 | Institutional data only. |
| Woodlands Specialty Hospital | 1184042822 | Institutional + some professional. |
| ROC-ASC | 1053407353 | Institutional + professional data. |
| Heights Surgery Center | 1144334962 | Institutional + professional data. |
| New Vista Health | 1639498454 | Institutional + professional data. |
| MBC Ambulatory Surgery Center | 1710082680 | Institutional data only. |

## Composing with Other Skills

This skill returns structured data. To create deliverables from query results:

- **Presentations**: Query the data here, then use the `pptx` skill to build slides
- **Spreadsheets**: Export to CSV with `--csv`, then use the `xlsx` skill to format
- **Documents**: Query and summarize, then use the `docx` skill for reports

## Troubleshooting

**"Index not found"** — Run `--build` first. If in a sandbox, set `TIC_DB_PATH=/tmp/tic_index.db`.

**"disk I/O error"** — The mounted filesystem doesn't support SQLite WAL. Use `TIC_DB_PATH`
to point to a local filesystem (e.g., `/tmp/`).

**No results for a known facility** — Check that the facility's NPI is in the source JSON
files. The pre-filtered extracts only include providers that appeared in the original
payer TiC files for the selected CPT codes and geographic area.

**Zero-dollar rates** — Many TiC entries include $0 placeholder rates. Use `--nonzero`
to filter these out, or `--summary` which automatically excludes them.
