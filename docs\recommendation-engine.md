# Recommendation Engine — Design Document

**Version:** 0.1.0
**Date:** 2026-09-30

---

## Core Architecture

The recommendation engine is **deterministic, rule-based, and evidence-linked**. It does NOT use machine learning in V1. Every output must be traceable to specific knowledge records with documented evidence.

## Engine Components

### 1. Crop Suitability Engine

**Purpose:** Given a farm, plot, crop, and planting date, determine if the crop is suitable.

**Input:**
```
{
  farmId: UUID,
  plotId: UUID,
  cropCanonicalName: "GROUNDNUT",
  plantingDate: "2026-07-01",
  season: "KHARIF"
}
```

**Output:**
```
{
  crop: "GROUNDNUT",
  status: "CONDITIONALLY_SUITABLE",  // or SUITABLE, UNSUITABLE, INSUFFICIENT_DATA
  reasons: [
    { factor: "ZONE_MATCH", detail: "Groundnut is a primary Zone IV kharif crop", 
      evidence: "UASB PoP Chapter Groundnut" },
    { factor: "SOIL_PH_MATCH", detail: "Soil pH 7.2 is within suitable range 6.0-8.0",
      evidence: "Kumar Naik et al. 2020, Molakalmuru taluk ranges" },
    { factor: "WATER_WARNING", detail: "Plot is rainfed; groundnut needs 500-700mm in season",
      evidence: "UASB PoP" }
  ],
  missingInformation: [
    "No specific variety selected — variety affects duration and water needs"
  ],
  evidence: [
    { source: "UAS Bangalore PoP 2023", section: "Groundnut", confidence: "REGIONAL_INFERENCE" },
    { source: "NBSS&LUP Chitradurga", section: "Soil suitability", confidence: "REGIONAL_INFERENCE" }
  ]
}
```

**Decision Logic:**
1. **Check soil test availability** → No soil test = INSUFFICIENT_DATA
2. **Check zone suitability** → Crop not in zone calendar = UNSUITABLE
3. **Check planting date** → Outside sowing window = UNSUITABLE or CONDITIONALLY_SUITABLE
4. **Check soil compatibility** → pH, texture, depth against crop requirements
5. **Check water availability** → Rainfed vs irrigated against crop water needs
6. **Check previous crop** → Rotation compatibility (if data available)
7. **Aggregate** → All checks pass = SUITABLE; warnings = CONDITIONALLY_SUITABLE; fail = UNSUITABLE

### 2. Variety Selection Engine

**Purpose:** Given a suitable crop, recommend documented varieties.

**Rules:**
- Only list varieties from KSSC catalogue or UASB/ICAR releases for Zone IV
- Separate "scientifically suitable" from "currently available for purchase"
- Never claim availability without verified stock data
- Link each variety to its source (KSSC page, AICRP trial, PoP chapter)

### 3. Nutrient Engine

**Purpose:** Provide fertilizer guidance based on soil test + crop + evidence.

**CRITICAL RULES:**
- Without soil test → NO specific NPK recommendation (only zone-level ranges as context)
- With soil test → Apply STCR if coefficients available; else zone RDF with conditions stated
- When conflicting RDFs exist → Show both with their conditions
- Always link to evidence

### 4. Pest/Disease Engine

**Purpose:** Provide pest/disease information and management options.

**Architecture:**
```
Farmer observation (text/photo)
  → Possible diagnosis (knowledge base match, NOT LLM invention)
  → Confidence level (based on symptom match quality)
  → If low confidence → request additional information / photos
  → If reasonable match → show management options
  → Management options pass through RegulatoryGate
  → Only approved interventions reach farmer
```

**The system MUST NOT:**
- Let the LLM invent a pest diagnosis
- Recommend any chemical not in the CIB&RC approved list
- Skip the RegulatoryGate check

### 5. Market Engine

**Purpose:** Show nearby market prices for the farmer's crops.

**Architecture:**
```
Farmer's crop
  → Map to AGMARKNET commodity name
  → Query nearby markets (Challakere, Hiriyur, Chitradurga)
  → Show: latest modal price, min/max, trend
  → Show: distance to each market (OSM routing)
  → DO NOT predict future prices
  → If farmer provides transport cost → calculate net realization
```

### 6. Weather Engine

**Purpose:** Provide weather context for farming decisions.

**Architecture:**
```
Farm location
  → Historical climatology (NASA POWER)
  → Current forecast (Open-Meteo with commercial license)
  → Rainfall vs normal comparison
  → ET0 calculation (FAO-56)
  → NEVER present as "your farm's weather" — always "weather model at your coordinates"
```

## The "I Don't Know" Protocol

The engine has a formal protocol for when it lacks sufficient information:

```
If INSUFFICIENT_DATA:
  1. State what information is missing
  2. Explain why that information matters
  3. Suggest how to obtain it
  4. Offer what CAN be said (zone-level context, clearly labeled)
  5. Never fabricate precision to fill the gap
```

**Example:**
```
"To recommend the right fertilizer for your groundnut crop, I need your soil 
health card results. Without a soil test, I can tell you that groundnut in 
this area typically needs nitrogen (25 kg/ha), phosphorus (50-75 kg/ha), 
and potassium (25-38 kg/ha) — but the exact amounts depend on your soil.

You can get a soil test at:
- KVK Chitradurga (Hiriyur): 08193-200081
- Your nearest Raitha Samparka Kendra

These zone-level ranges are from UAS Bangalore Package of Practices and 
ISSS NARP Central Dry Zone recommendations."
```
