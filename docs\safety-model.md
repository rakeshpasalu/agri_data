# Safety Model — Design Document

**Version:** 0.1.0
**Date:** 2026-09-30

---

## Purpose

This document defines the safety boundaries that prevent the system from causing agricultural harm. These boundaries are enforced in compiled code, not in LLM prompts.

## Safety Layers

### Layer 1: Regulatory Hard Gate

**Rule:** No chemical (pesticide, fungicide, herbicide) recommendation reaches the farmer without passing through `RegulatoryGate`.

```
Input: {activeIngredient, crop, pest, geography}
    │
    ▼
Check 1: Is this active ingredient on the CIB&RC banned list?
    YES → BLOCKED. Reason: "Banned by Government of India"
    │
Check 2: Is this active ingredient registered with CIB&RC?
    NO  → BLOCKED. Reason: "Not registered for use in India"
    │
Check 3: Is this active ingredient registered for THIS crop?
    NO  → BLOCKED. Reason: "Not registered for use on {crop}"
    │
Check 4: Is this active ingredient registered for THIS pest/disease on this crop?
    NO  → BLOCKED. Reason: "Not registered for {pest} on {crop}"
    │
Check 5: Is there a state-level additional restriction?
    YES → BLOCKED or RESTRICTED with state-specific notes
    │
Check 6: Is the regulatory data current (< 90 days old)?
    NO  → FLAG: "Regulatory data may be outdated — verify before use"
    │
    ▼
APPROVED: {dose, PHI, precautions from CIB&RC Major Uses}
```

**Implementation:** `RegulatoryGate` is a Java interface with a deterministic implementation that queries the `input_regulation` table. It is NOT an LLM call.

**Data source:** CIB&RC PDFs parsed and loaded into the database:
- Formulations registered (as on 31.03.2026)
- Insecticides 9(3) (as on 31.03.2026)
- Banned/refused/restricted (as on 31.07.2026)
- Major Uses: insecticides, fungicides, herbicides, biopesticides, PGRs (as on 31.03.2026)

**Monocrotophos example:** Even if a knowledge record from an ICAR advisory recommends monocrotophos for groundnut leaf miner, the Regulatory Gate BLOCKS it because monocrotophos appears on the banned/restricted list. The knowledge record remains in the database (it reflects what the advisory said), but the recommendation never reaches the farmer.

### Layer 2: Evidence Requirement Gate

**Rule:** No recommendation is produced without traceable evidence.

```
Recommendation attempt
    │
    ▼
Check: Does this recommendation have a linked KnowledgeRecord?
    NO → BLOCKED. Internal error — no recommendation without evidence.
    │
Check: Does the KnowledgeRecord have a linked Evidence?
    NO → BLOCKED. Knowledge without evidence is not knowledge.
    │
Check: Does the Evidence have a linked Source?
    NO → BLOCKED. Evidence without a source is an assertion.
    │
Check: Is the Source authority_level sufficient?
    NEWS_MEDIA or COMMUNITY → WARNING: "Based on non-authoritative source"
    │
Check: Is the geographic_resolution appropriate?
    NATIONAL data used for farm → WARNING: "Based on national data, not local"
    │
    ▼
ALLOWED: Recommendation with full evidence chain
```

### Layer 3: Soil Test Requirement

**Rule:** No nutrient/fertilizer recommendation is produced without farm-specific soil data.

```
Fertilizer recommendation attempt
    │
    ▼
Check: Does this plot have a soil test?
    NO → Return INSUFFICIENT_DATA
         Message: "A soil test is needed before we can recommend 
                   fertilizer amounts. Contact KVK Chitradurga or 
                   your nearest RSK for soil testing."
         Offer: Display zone-level ranges as context (clearly labeled)
    │
Check: Is the soil test recent (< 3 years)?
    NO → WARNING: "Soil test is {age} years old. A new test may 
                   give more accurate recommendations."
    │
Check: Do we have STCR coefficients for this crop × soil?
    NO → Return REGIONAL_INFERENCE
         Use zone-level RDF with caveat
    │
    ▼
STCR-based recommendation with soil test values
```

### Layer 4: Conflicting Evidence Guard

**Rule:** When sources disagree, the system does not silently pick one.

```
Recommendation with conflicting sources
    │
    ▼
Check: Are there ConflictingEvidence records for this knowledge?
    YES → Check: Can the conflict be resolved by the farmer's conditions?
          │
          Irrigation known + conflict is irrigated-vs-rainfed → Resolved
          Soil type known + conflict is soil-dependent → Resolved
          │
          Cannot resolve → Return CONFLICTING_EVIDENCE
          Message: "Different sources recommend different amounts:
                    Source A (UASB PoP): 25:75:37.5 NPK
                    Source B (NARP rainfed): 25:50:25 NPK
                    The difference may depend on your irrigation and 
                    soil type. A soil test would help determine the 
                    right amount for your field."
```

### Layer 5: LLM Hallucination Guard

**Rule:** The LLM interface cannot generate agricultural recommendations not backed by the knowledge base.

**Implementation:**
1. LLM receives structured data from the Decision Engine, not raw database access
2. LLM prompt includes: "You are presenting recommendations from the system, not generating them"
3. Response verification: check that any specific quantities (doses, NPK, prices) in the LLM output match the structured data provided
4. If the LLM mentions a pesticide not in the approved output → flag for review
5. If the LLM generates a numerical recommendation not in the structured output → strip it

**Technical approach:**
```java
public class LlmOutputValidator {
    /**
     * Validates that LLM-generated text doesn't contain
     * agricultural recommendations not present in the
     * structured recommendation data.
     */
    public ValidationResult validate(
        String llmOutput, 
        RecommendationBundle structuredData) {
        
        // Check for unauthorized pesticide mentions
        // Check for unauthorized numerical recommendations
        // Check for unauthorized crop advice
        // Flag any concerning patterns
    }
}
```

### Layer 6: Demo Data Isolation

**Rule:** Demo data never enters production recommendation paths.

```
Every record has data_provenance field
    │
    ▼
If data_provenance == DEMO_ONLY:
    - Record is visible in admin view with DEMO badge
    - Record is visible in demo flows with DEMO badge
    - Record is EXCLUDED from production recommendation queries
    - Record is EXCLUDED from evidence chains for real farms
```

**SQL enforcement:**
```sql
-- Production queries always exclude demo data
WHERE data_provenance != 'DEMO_ONLY'
```

## What The System Must Never Do

1. **Never recommend a banned pesticide** — regardless of what any extension document says
2. **Never produce farm-specific fertilizer doses without a soil test** — zone RDFs are context, not prescriptions
3. **Never claim to know farm-specific data it doesn't have** — "your soil pH is 7.2" when we have no soil test
4. **Never present district averages as farm measurements** — "your expected yield is 1,474 kg/ha" (district avg)
5. **Never fabricate seed availability** — "buy TMV-2 at Molakalmuru dealer" without verification
6. **Never determine crop insurance eligibility** — display scheme information, not eligibility decisions
7. **Never predict market prices** — show historical and current data, not predictions
8. **Never diagnose plant disease from photos without expert review** — suggest possibilities, request validation
9. **Never present weather model data as observed weather** — "weather forecast for your area" not "weather at your farm"
10. **Never allow demo data to appear as real data** — every demo record is tagged and filtered

## Failure Mode: "Which Crop Should I Plant?"

When a farmer asks this question without providing soil data:

### WRONG response:
> "Based on your location in Molakalmuru, I recommend groundnut. Use TMV-2 variety with 25:75:37.5 NPK fertilizer."

### CORRECT response:
> "To recommend the right crop for your field, I need to know a few things:
> 
> **What I know about your area:**
> - You're in the Central Dry Zone (Zone IV) near Molakalmuru
> - Common crops here include groundnut, finger millet (ragi), and sorghum (jowar)
> - Average rainfall is about 540-590 mm, mostly June-October
> 
> **What I need from you:**
> 1. Do you have a soil health card? (This helps me recommend the right fertilizer)
> 2. What is your water source? (Rainfed / borewell / canal)
> 3. What crop did you grow last season?
> 
> Without a soil test, I can tell you which crops are generally suitable for this area, but I cannot recommend specific fertilizer amounts."

## Safety Audit Checklist

| Check | Frequency | Responsible |
|-------|-----------|-------------|
| CIB&RC banned list is current | Monthly | System admin |
| CIB&RC Major Uses PDFs are current | Quarterly | System admin |
| No DEMO_ONLY records in production queries | Every deployment | Automated test |
| RegulatoryGate blocks all banned chemicals | Every deployment | Automated test |
| Insufficient data correctly identified | Every deployment | Automated test |
| LLM output does not contain unauthorized recs | Runtime | LlmOutputValidator |
| Zone-level data labeled as zone-level | Code review | Engineering |
| Conflicting evidence flagged, not averaged | Code review | Engineering |
