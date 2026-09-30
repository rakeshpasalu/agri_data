# Bhumi local pilot: integration status

**Checked:** 2026-09-30  
**Status:** work in progress; not ready to use for farm investment decisions.

## Connected and verified locally

- `GET /api/market/prices` delegates to the AGMARKNET service. With no `DATA_GOV_IN_API_KEY` and no authenticated cache, a live request returns `setup_required` and an empty `records` list. It does not invent prices. The source is a daily wholesale-price dataset, not a tick feed or a future price forecast. [Official resource](https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi).
- `GET /api/cadastral/bhoomi` provides a manual link to the [Karnataka Bhoomi RTC/Pahani portal](https://landrecords.karnataka.gov.in/service2/RTC.aspx). Survey 3 / Hissa 2 and 4 are carried as farmer-provided, unverified identifiers. No owner, acreage, boundary, or RTC result is fetched or inferred.
- Chitradurga is the district scope and Molakalmuru is listed as one of its taluks by the [Government of Karnataka district administration](https://chitradurga.nic.in/en/tehsil/). Hosanagalapura's Census 2011 code is a statistical identifier, not a Bhoomi revenue code.

The server runs locally with:

```powershell
python backend/app_server.py
```

## Mandi key setup

The data.gov.in key stays on the server. Set it in the same PowerShell window before starting the app:

```powershell
$env:DATA_GOV_IN_API_KEY = "your_data_gov_in_key"
python backend/app_server.py
```

The current operator has no key, so no Chitradurga mandi price is available. After a verified fetch, the service caches official rows for 24 hours. An older cache is labelled stale and keeps its original reported date. A modal wholesale observation is not a guaranteed farm-gate offer or net realization.

## Still in progress; do not rely on these outputs

- The crop engine still uses a fixed `CROPS_SPECIFICATION` list and synthetic soil/economics calculations. It can display crop, yield, fertilizer, ROI, or net-return values that have not been established for this farm.
- The farmer profile and UI still contain placeholder contact identity, fixed acreage/coordinates, unmeasured soil and irrigation claims, and fixed crop yield/profit text. The farmer only confirmed Survey 3, Hissa 2 and 4; those identifiers themselves remain unverified against RTC.
- The weather handler still has a procedural fallback if its upstream forecast cannot be fetched. That fallback must be removed before describing every displayed forecast as live.
- KSSCL inventory, certified lot numbers, local dealers, and current seed prices for Molakalmuru have not been verified. UAS/ICAR variety catalogues establish variety identities, not local availability or performance. Treat Dolly and Naavi as source-backed leads only; see the source notes in `knowledge/crops/catalog.json`.
- No evidence-backed seasonal market-price forecast, farm-specific cost model, validated local sowing calendar, soil test, water-volume record, or buyer quote is connected yet.

AGMARKNET daily records are useful for price discovery when available, but they are observations. Historical movement becomes useful only after dated source rows have accumulated; it must not be presented as a forecast.
