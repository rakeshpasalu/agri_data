# Data Gaps — Operational Summary

**Version:** 0.1.0
**Date:** 2026-09-30

---

> [!IMPORTANT]
> This document summarizes what data the system HAS versus what it NEEDS.
> See `research/audit/03-data-gaps.md` for the detailed gap analysis with resolution paths.

## What We HAVE (can build V1 with)

| Data | Source | Quality | Notes |
|------|--------|---------|-------|
| Village identity | Census 2011 | HIGH | Code 605160, uninhabited, 179.14 ha |
| Approximate coordinates | OSM + offset | MODERATE | ±2 km, adequate for gridded data |
| Climate baseline | NASA POWER API | HIGH | 20-year climatology, JSON, free |
| Weather forecast | Open-Meteo / commercial | HIGH | Requires commercial license |
| Zone IV crop knowledge | UASB PoP, KVK, ICAR | HIGH | Authoritative but not farm-specific |
| Variety catalogue | KSSC, AICRP | MODERATE | State level, not local stock |
| Pesticide legality | CIB&RC pdfs | VERY HIGH | The regulatory safety foundation |
| Wholesale market prices | AGMARKNET/GODL | HIGH | Challakere/Hiriyur/Chitradurga APMCs |
| Satellite imagery | Sentinel-2 (Copernicus) | HIGH | Requires farm polygon to be useful |
| Elevation/terrain | SRTM/Copernicus DEM | HIGH | 30 m resolution, free |
| Government schemes | raitamitra, pmfby | MODERATE | Existence info, not eligibility |
| Taluk soil ranges | Kumar Naik 2020 | MODERATE | n=148, not village-specific |
| District soil series | NBSS&LUP | HIGH | Legacy but authoritative |

## What We LACK (blocks specific features)

| Missing Data | Blocked Feature | How to Obtain |
|-------------|----------------|---------------|
| Farm soil test (NPK, pH, etc.) | Fertilizer recommendation | Farmer enters SHC data |
| Farm polygon | Field-level satellite analysis | Farmer draws or GPS walks |
| Village crop census | Village-specific crop advice | Farmer enrollment |
| Current pest incidence | Location-specific pest alerts | Farmer observations |
| Local seed dealer inventory | "Buy this variety" feature | Dealer partnership |
| Molakalmuru APMC feed | Local market prices | data.gov.in API query |
| Transport cost matrix | Net realization calculator | Farmer-entered cost |
| State pesticide restrictions | Karnataka-specific blocks | KSDA engagement |

## V1 Scope Decision

Given the data availability, V1 can credibly provide:

✅ **Information layer**: Weather, satellite greenness, nearby mandi prices, cited zone-level crop knowledge

✅ **Farm diary**: Record crops, activities, expenses, observations, harvest, sales

✅ **Transparent suitability**: "Is groundnut suitable for Zone IV kharif on rainfed red soil?" — YES, with evidence

⚠️ **Conditional features** (require farmer input): Soil-test-based nutrient guidance, variety-specific advice

❌ **NOT in V1**: Autonomous crop recommendation, fertilizer prescription without soil test, pesticide recommendation engine, yield prediction, price prediction, AI disease diagnosis

## Pilot Crops (Based on Evidence Depth)

| Crop | Evidence Depth | Rationale |
|------|---------------|-----------|
| **Groundnut** | DEEP | Zone IV primary crop; UASB PoP + KSSC varieties + AICRP trials + market data |
| **Finger Millet (Ragi)** | DEEP | Zone IV staple; multiple varieties; blast-tolerant options documented |
| **Sorghum (Jowar)** | MODERATE | Historical dominance in Molakalmuru; CSH hybrids documented |
| **Pigeonpea (Redgram)** | MODERATE | Common intercrop; BRG varieties documented |

Only groundnut and finger millet have sufficient evidence depth for V1 crop suitability evaluation. Others can be added as knowledge records are structured.
