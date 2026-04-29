# CMS Transparency in Coverage — In-Network File Schema

Reference for the JSON structure of CMS TiC In-Network rate files (schema v2.0).
Read this if you need to understand the raw data format or modify the indexer.

## Top-Level Structure

```json
{
  "reporting_entity_name": "Payer Name",
  "reporting_entity_type": "health insurance issuer",
  "last_updated_on": "2024-01-01",
  "version": "2.0.0",
  "provider_references": [ ... ],
  "in_network": [ ... ]
}
```

## Provider References (Root-Level)

Most files use a root-level `provider_references` array. Each entry has a numeric
`provider_group_id` that is referenced by integer from `negotiated_rates` entries.

```json
{
  "provider_group_id": 1,
  "provider_groups": [
    {
      "npi": [1234567890, 9876543210],
      "tin": { "type": "ein", "value": "12-3456789" }
    }
  ]
}
```

## In-Network Items

Each item in the `in_network` array represents a billing code with its negotiated rates:

```json
{
  "negotiation_arrangement": "ffs",
  "name": "Total Knee Arthroplasty",
  "billing_code_type": "CPT",
  "billing_code_type_version": "2024",
  "billing_code": "27447",
  "description": "Arthroplasty knee condyle and plateau medial and lateral compartments",
  "negotiated_rates": [
    {
      "provider_references": [1, 2, 3],
      "negotiated_prices": [
        {
          "negotiated_type": "negotiated",
          "negotiated_rate": 15000.00,
          "expiration_date": "9999-12-31",
          "service_code": ["11", "22"],
          "billing_class": "institutional",
          "billing_code_modifier": []
        }
      ]
    }
  ]
}
```

## Two Provider Reference Patterns

The indexer handles both patterns found in practice:

1. **Root-level references** (most files): `negotiated_rates[].provider_references`
   contains integer IDs that point to the root `provider_references` array.

2. **Inline provider_groups** (some files, e.g., Cigna HMO): `negotiated_rates[]`
   contains `provider_groups` directly with `npi` arrays and `tin` objects, and
   `provider_references` at root level is empty or absent.

## Key Fields for Analysis

| Field | Values | Significance |
|-------|--------|-------------|
| `billing_class` | `institutional`, `professional` | Facility vs. physician fee |
| `negotiated_type` | `negotiated`, `derived`, `fee schedule`, `percentage`, `per diem` | Rate basis |
| `billing_code_type` | `CPT`, `HCPCS`, `MS-DRG`, `NDC` | Code system |
| `service_code` | `11` (office), `21` (inpatient), `22` (outpatient), `24` (ASC) | Place of service |
| `negotiation_arrangement` | `ffs` (fee-for-service), `bundle`, `cap` (capitation) | Payment model |