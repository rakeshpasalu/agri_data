# End-to-End Demonstration: Hypothetical Farm near Hosanagalapura

> [!CAUTION]
> **THIS IS A DEMONSTRATION — NOT A REAL FARM**
> 
> Every piece of data below is either from audited public sources (labeled) or
> hypothetical (labeled DEMO). No real farmer's data was used. No real
> agricultural recommendation should be derived from this demonstration.

---

## Demo Farm Profile

| Field | Value | Source |
|-------|-------|--------|
| **Farm name** | DEMO Farm Alpha | DEMO_ONLY |
| **Location** | ~14.887°N, 76.842°E | Estimated from OSM neighbor (Phase-0 research) |
| **Village** | Hosanagalapura (605160) | Census 2011 (GOVERNMENT_DATA) |
| **Taluk** | Molakalmuru | Census 2011 |
| **District** | Chitradurga | Census 2011 |
| **Agro-climatic zone** | Central Dry Zone (Zone IV) | Karnataka classification (GOVERNMENT_DATA) |
| **Area** | 2.5 hectares | DEMO_ONLY — hypothetical |
| **Soil type** | Red sandy loam (gravelly) | DEMO_ONLY — based on PMKSY DIP taluk data |
| **Irrigation** | Rainfed | DEMO_ONLY — most Molakalmuru is rainfed |
| **Previous crop** | Sorghum (Jowar) | DEMO_ONLY |
| **Farmer language** | Kannada | DEMO_ONLY |

## Step 1: Farm Location → Automatic Data

Once the farmer places their farm at approximately 14.887°N, 76.842°E, the system automatically obtains:

### Climate Baseline (NASA POWER — REAL DATA, API verified)
| Parameter | Value | Note |
|-----------|-------|------|
| Elevation | 500.48 m | NASA POWER grid, not a survey point |
| Annual rainfall | ~588 mm/year | MERRA-2 reanalysis, NOT a rain gauge |
| Wettest month | September (4.01 mm/day) | |
| Driest months | January (0.07 mm/day) | |
| Mean temperature | 26.5°C | |
| Hottest month max | 43.11°C (May climatology) | |
| Annual RH | 59.8% | |
| Solar radiation | 20.22 MJ/m²/day | |

**System note to farmer:** *"Weather data is from a weather model at your coordinates, not from a weather station in your village."*

### Zone Information (GOVERNMENT_DATA)
- Zone IV Central Dry Zone
- Primary crops: ragi, jowar, groundnut, pulses, oilseeds
- Rainfall range: 453–718 mm
- Soils: red sandy loams, gravelly red clay

## Step 2: Missing Information Identified

The system identifies what it DOES NOT know:

```
MISSING INFORMATION:
1. ❌ Soil test (pH, N, P, K, micronutrients)
   → "Without a soil test, I cannot recommend specific fertilizer amounts."
   → "Contact KVK Chitradurga: 08193-200081 or your nearest RSK"

2. ❌ Farm boundary (polygon)
   → "Drawing your farm boundary would allow satellite vegetation monitoring"

3. ❌ Water source details
   → "Is your farm rainfed or do you have a borewell/well?"

4. ❌ Current crop
   → "What are you planning to grow this season?"
```

## Step 3: Farmer Provides Information

Farmer says (in Kannada): *"ನಾನು ಈ ಖಾರಿಫ್ ಕಡಲೆಕಾಯಿ ಬೆಳೆಯಲು ಬಯಸುತ್ತೇನೆ"*
("I want to grow groundnut this kharif")

System maps: ಕಡಲೆಕಾಯಿ → GROUNDNUT, ಖಾರಿಫ್ → KHARIF

## Step 4: Crop Suitability Evaluation

### With Soil Test (DEMO scenario where farmer has SHC):

**DEMO Soil Test Values** (hypothetical, within Molakalmuru taluk ranges):
| Parameter | Value | Molakalmuru Range (Kumar Naik 2020) | Status |
|-----------|-------|--------------------------------------|--------|
| pH | 7.2 | 6.00–8.00 | ✅ Within range |
| EC | 0.32 dS/m | 0.13–0.80 | ✅ Within range |
| OC | 0.45% | 0.19–1.00% | ⚠️ Low-medium |
| N | 135 kg/ha | 46–238 | ✅ Within range |
| P | 38.5 kg/ha | 22.4–64.4 | ✅ Within range |
| K | 245 kg/ha | 134–685 | ✅ Within range |
| Zn | 0.52 ppm | 0.31–1.18 | ⚠️ Marginal |

**System Evaluation:**
```json
{
  "crop": "GROUNDNUT",
  "status": "CONDITIONALLY_SUITABLE",
  "reasons": [
    {
      "factor": "ZONE_MATCH",
      "status": "PASS",
      "detail": "Groundnut is a primary Zone IV kharif crop",
      "evidence": "UAS Bangalore Package of Practices, Chapter: Groundnut",
      "confidence": "REGIONAL_INFERENCE"
    },
    {
      "factor": "PLANTING_DATE",
      "status": "PASS",
      "detail": "July sowing is within the recommended June-July window",
      "evidence": "UAS Bangalore PoP sowing calendar for Zone IV",
      "confidence": "REGIONAL_INFERENCE"
    },
    {
      "factor": "SOIL_PH",
      "status": "PASS",
      "detail": "pH 7.2 is within suitable range for groundnut (6.0-8.0)",
      "evidence": "DEMO soil test + Kumar Naik et al. 2020 ranges"
    },
    {
      "factor": "WATER_AVAILABILITY",
      "status": "WARNING",
      "detail": "Farm is rainfed. Groundnut needs 500-700mm during growing season. Average rainfall at this location is ~588 mm/year with most falling Jun-Oct. Adequate in normal years; drought risk exists.",
      "evidence": "NASA POWER climatology + Zone IV classification as 'very high drought hazard'"
    },
    {
      "factor": "ZINC_STATUS",
      "status": "WARNING",
      "detail": "Zinc at 0.52 ppm is marginal. IISS e-Atlas shows 41% of Molakalmuru area is zinc-deficient.",
      "evidence": "DEMO soil test + IISS e-Atlas taluk data"
    }
  ],
  "missing_information": [
    "Specific variety not selected — variety affects duration and drought tolerance",
    "Previous crop details would help assess rotation benefits"
  ],
  "evidence_chain": [
    {
      "source": "UAS Bangalore Package of Practices 2023",
      "authority": "UNIVERSITY",
      "geographic_scope": "Zone IV, Karnataka",
      "license": "YELLOW"
    },
    {
      "source": "Kumar Naik et al. 2020, Int. J. Chem. Studies",
      "authority": "PEER_REVIEWED_JOURNAL",
      "geographic_scope": "Molakalmuru taluk",
      "license": "YELLOW"
    },
    {
      "source": "NASA POWER API (climatology 2001-2020)",
      "authority": "GOVERNMENT",
      "geographic_scope": "Gridded point at 14.887, 76.842",
      "license": "GREEN"
    }
  ]
}
```

### Without Soil Test:

```json
{
  "crop": "GROUNDNUT",
  "status": "INSUFFICIENT_DATA",
  "reasons": [
    {
      "factor": "ZONE_MATCH",
      "status": "PASS",
      "detail": "Groundnut is suitable for Zone IV"
    }
  ],
  "missing_information": [
    "CRITICAL: No soil test data available for this plot",
    "Without soil analysis, we cannot evaluate soil suitability or recommend fertilizer",
    "Contact KVK Chitradurga (08193-200081) or nearest RSK for soil testing"
  ],
  "context": "Groundnut is commonly grown in Molakalmuru area. Zone IV PoP recommends it as a kharif crop. However, specific suitability for YOUR field requires a soil test."
}
```

## Step 5: Variety Options (if crop is suitable)

```
DOCUMENTED VARIETIES FOR GROUNDNUT IN KARNATAKA:
(Source: KSSC product list, ksscl.karnataka.gov.in)

1. TMV-2 — Spanish bunch, ~105-110 days
2. GPBD-4 — Spanish bunch, ~110-120 days
3. K-6 — ~105-115 days
4. G-2-52
5. GKVK-5
6. KCG-6

⚠️ AVAILABILITY NOT VERIFIED
These varieties are in the KSSC state catalogue. We cannot confirm
they are currently in stock at any dealer near Molakalmuru.
KSSC Chitradurga centre: Kanaka Circle, Holalkere road, Chitradurga 577501.

No Molakalmuru KSSC sale point was found in the centres list.
```

## Step 6: Fertilizer Guidance

### With soil test:
```
NUTRIENT CONTEXT (not a prescription without STCR):

Zone IV recommendations for groundnut vary by source:
- UASB PoP: N 25 : P₂O₅ 75 : K₂O 37.5 kg/ha + 500 kg/ha gypsum
- NARP/CDZ (rainfed): N 25 : P₂O₅ 50 : K₂O 25 kg/ha

⚠️ CONFLICTING EVIDENCE: These sources recommend different P and K amounts.
The difference likely relates to irrigation status and soil calcium.
Your farm is rainfed — the lower P/K recommendation (25:50:25) may be
more appropriate, but this should be confirmed with a soil-test-based
recommendation (STCR) from KVK.

Your zinc is marginal (0.52 ppm). Consider zinc sulfate application
based on KVK/RSK guidance — do not apply without consulting extension.
```

### Without soil test:
```
❌ FERTILIZER RECOMMENDATION BLOCKED

A soil test is required before we can recommend fertilizer amounts.
Applying generic zone-level doses without knowing your soil's current
nutrient status may waste money or harm your crop.

WHAT YOU CAN DO:
1. Get a Soil Health Card from KVK Chitradurga or RSK
2. If you have an existing SHC, enter the values in the app
3. Photograph your SHC card and upload it
```

## Step 7: Regulatory Safety Check (Always Active)

```
REGULATORY CHECK (CIB&RC as on 31.07.2026):

If an older advisory recommends monocrotophos for groundnut leaf miner:
  ❌ BLOCKED — Monocrotophos is BANNED/RESTRICTED
  Source: CIB&RC banned list, ppqs.gov.in, effective as on 31.07.2026
  
  ALTERNATIVE: Consult KVK Chitradurga for approved alternatives.
  Neem-based products (azadirachtin) are registered biopesticides.
  
  ⚠️ We do not recommend specific pesticide products or doses in V1.
  This requires a professional pest diagnosis and legal cross-check.
```

## Step 8: Market Context

```
NEARBY WHOLESALE MARKETS:
(Source: AGMARKNET via data.gov.in, GODL-India license)

Market             | Distance* | Status
Challakere APMC    | ~40 km    | Groundnut trading confirmed in research
Hiriyur APMC       | ~50 km    | Groundnut/sunflower trading
Chitradurga APMC   | ~70 km    | District HQ market

* Distances are approximate. Actual road distance may differ.

⚠️ PRICES NOT SHOWN: AGMARKNET API connectivity was not confirmed
from this environment. When live, the system will show:
- Latest modal price (₹/quintal)
- Min/max price range
- Recent trend

MSP for groundnut (GoI 2026-27): Check current CACP notification.
Transport cost: Enter your actual transport cost for net realization.
```

## What This Demo Proves

1. ✅ **Evidence traceability**: Every claim links to a specific source with authority level
2. ✅ **Geographic honesty**: Zone-level data is labeled as zone-level, not farm-level
3. ✅ **Insufficient data handling**: System refuses to fabricate when soil test is missing
4. ✅ **Regulatory safety**: Banned chemicals are blocked regardless of advisory recommendations
5. ✅ **Conflicting evidence**: Fertilizer RDF conflict is shown, not hidden
6. ✅ **Multilingual mapping**: Kannada input maps to canonical crop names
7. ✅ **Variety honesty**: Listed from KSSC but availability NOT claimed
8. ✅ **Market transparency**: Sources cited, distances approximate, prices pending API
