# Evidence Model — Design Document

**Version:** 0.1.0
**Date:** 2026-09-30

---

## Core Principle

Every agricultural fact in the system must answer: **"Why do we believe this?"**

The evidence model is not metadata bolted onto recommendations. It IS the primary data structure. A recommendation without evidence is not a recommendation — it's a hallucination.

## Entity Relationship

```
Source (who published it)
  │
  └─→ Evidence (specific claim from that source)
        │
        └─→ KnowledgeRecord (structured agricultural fact)
              │
              ├─→ KnowledgeVersion (change history)
              │
              └─→ ConflictingEvidence (when sources disagree)
```

## Source

The institutional publisher of agricultural information.

```
Source {
    id: UUID
    name: String                    -- "ICAR-NBSS&LUP"
    authority_level: AuthorityLevel -- GOVERNMENT, RESEARCH_INSTITUTION, UNIVERSITY, 
                                    -- PEER_REVIEWED_JOURNAL, EXTENSION_SERVICE, 
                                    -- INDUSTRY, NEWS_MEDIA, COMMUNITY
    institution_type: String        -- "Soil Survey"
    url: String                     -- "https://icar-nbsslup.org.in"
    country: String                 -- "IN"
    state: String                   -- "KA" (nullable)
    license_band: LicenseBand      -- GREEN, YELLOW, RED
    license_notes: String
    verified_date: LocalDate        -- when we last confirmed this source is current
    notes: String
}
```

### Authority Levels (ordered by precedence)
1. **GOVERNMENT** — CIB&RC, Census, DES, IMD, CGWB
2. **RESEARCH_INSTITUTION** — ICAR institutes, NBSS&LUP
3. **UNIVERSITY** — UAS Bangalore, KSNUAHS
4. **PEER_REVIEWED_JOURNAL** — Published research
5. **EXTENSION_SERVICE** — KVK, RSK, ADA
6. **INDUSTRY** — KSSC, seed companies
7. **NEWS_MEDIA** — Newspapers (never for agricultural facts, only for events)
8. **COMMUNITY** — OSM, farmer reports (lowest authority, valuable for coverage)

## Evidence

A specific claim extracted from a source document.

```
Evidence {
    id: UUID
    source_id: UUID (FK → Source)
    
    -- Document reference
    document_url: String            -- exact URL or file path
    document_hash: String           -- SHA-256 of downloaded document
    document_title: String          -- "Soils and Land Use of Chitradurga District"
    page_reference: String          -- "Table 3.2, p.45"
    section_reference: String       -- "Chapter: Groundnut"
    
    -- The claim
    claim_text: String              -- verbatim or near-verbatim extracted claim
    claim_type: ClaimType           -- QUANTITATIVE, QUALITATIVE, REGULATORY, PROCEDURAL
    
    -- Geographic applicability
    geographic_applicability: {
        country: String             -- "IN"
        state: String               -- "KA"  
        agro_climatic_zone: String  -- "ZONE_IV"
        district: String            -- "CHITRADURGA"
        taluk: String               -- "MOLAKALMURU"  (often null)
        village_code: String        -- "605160" (rarely populated)
    }
    geographic_resolution: GeographicResolution
    
    -- Observation type
    observation_type: ObservationType
        -- FIELD_OBSERVATION: measured in the field
        -- LABORATORY_ANALYSIS: lab result
        -- SATELLITE_DERIVED: from remote sensing
        -- MODEL_OUTPUT: from a simulation
        -- SURVEY_DATA: from a census/survey
        -- EXPERT_OPINION: professional judgment
    
    -- Temporal
    publication_date: LocalDate
    data_collection_date: LocalDate  -- when the underlying data was collected (often different)
    data_freshness_years: Integer    -- computed: current_year - data_collection_year
    
    -- Conditions under which this evidence applies
    conditions: {
        crop: String                -- "GROUNDNUT" (nullable)
        variety: String             -- "TMV-2" (nullable)
        soil_type: String           -- "ALFISOL" (nullable)
        irrigation_status: String   -- "RAINFED" / "IRRIGATED" (nullable)
        season: String              -- "KHARIF" (nullable)
        target_yield: String        -- (nullable)
    }
    
    -- Verification
    verified: Boolean               -- has an auditor confirmed this?
    verified_by: String
    verification_date: LocalDate
    verification_notes: String
    
    -- Language
    original_language: String       -- "EN", "KN"
    
    created_at: Timestamp
}
```

## KnowledgeRecord

A structured agricultural fact derived from evidence.

```
KnowledgeRecord {
    id: UUID
    
    -- Classification
    category: String                -- "CROP_REQUIREMENT", "NUTRIENT_RDF", "PEST_MANAGEMENT"
    subcategory: String             -- "NPK_RECOMMENDATION", "SOWING_DATE"
    
    -- The structured knowledge
    content: JSONB {
        -- varies by category, examples:
        -- For NUTRIENT_RDF:
        --   { n_kgha: 25, p2o5_kgha: 75, k2o_kgha: 37.5, other: "gypsum 500 kg/ha" }
        -- For SOWING_DATE:
        --   { start_month: 6, end_month: 7, notes: "with onset of monsoon" }
        -- For CROP_SUITABILITY:
        --   { suitable: true, conditions: "red sandy loam, >500mm rainfall" }
    }
    
    -- Conditions for applicability
    conditions: JSONB {
        crop: String
        variety: String
        soil_type: String
        irrigation_status: String
        season: String
        zone: String
        target_yield: String
    }
    
    -- Evidence chain
    evidence_id: UUID (FK → Evidence)       -- primary evidence
    additional_evidence_ids: UUID[]          -- supporting evidence
    
    -- Geographic applicability
    geographic_resolution: GeographicResolution
    
    -- Confidence
    confidence: EvidenceConfidence
        -- VERIFIED_APPLICABLE: confirmed for this specific context
        -- REGIONAL_INFERENCE: zone/district data applied more locally
        -- CONFLICTING_EVIDENCE: other sources disagree
        -- INSUFFICIENT_DATA: gaps in the evidence
        -- EXPERT_REVIEW_REQUIRED: system cannot evaluate
    
    -- Versioning
    version: Integer
    valid_from: LocalDate
    valid_until: LocalDate           -- null = still valid
    superseded_by: UUID              -- points to newer version
    
    created_at: Timestamp
    updated_at: Timestamp
}
```

## KnowledgeVersion

Audit trail for knowledge changes.

```
KnowledgeVersion {
    id: UUID
    knowledge_record_id: UUID (FK → KnowledgeRecord)
    version_number: Integer
    changed_by: String               -- who made this change
    changed_at: Timestamp
    change_reason: String            -- "Updated based on KVK 2025 report"
    previous_content: JSONB          -- snapshot of content before change
    previous_evidence_id: UUID       -- what evidence it was based on before
}
```

## ConflictingEvidence

When two or more sources disagree on the same agricultural fact.

```
ConflictingEvidence {
    id: UUID
    
    -- The conflicting records
    knowledge_record_a_id: UUID (FK → KnowledgeRecord)
    knowledge_record_b_id: UUID (FK → KnowledgeRecord)
    
    -- Conflict analysis
    conflict_type: ConflictType
        -- QUANTITATIVE_DIFFERENCE: same parameter, different values
        -- CONTEXT_DIFFERENCE: valid for different conditions
        -- TEMPORAL_DIFFERENCE: one supersedes the other
        -- METHODOLOGY_DIFFERENCE: different experimental approaches
    
    -- Resolution
    resolution_status: ResolutionStatus
        -- UNRESOLVED: both stored, system cannot pick
        -- RESOLVED_CONTEXT: conditions differ, both valid in context
        -- RESOLVED_SUPERSEDED: newer source replaces older
        -- EXPERT_RESOLVED: agronomist made a determination
    
    resolution_notes: String
    resolved_by: String
    resolved_at: Timestamp
    
    -- What conditions differ between the two records
    conditions_differ: JSONB {
        -- e.g., { "irrigation_status": ["IRRIGATED", "RAINFED"] }
    }
    
    created_at: Timestamp
}
```

## Usage Example: Groundnut Fertilizer Recommendation

```
Source A: "UAS Bangalore Package of Practices"
  authority_level: UNIVERSITY
  license_band: YELLOW

  Evidence A1:
    claim: "Groundnut RDF: 25:75:37.5 NPK + 500 kg/ha gypsum"
    conditions: { crop: "GROUNDNUT", zone: "ZONE_IV" }
    observation_type: EXPERT_OPINION
    geographic_resolution: ZONE

    KnowledgeRecord A1K:
      category: "NUTRIENT_RDF"
      content: { n: 25, p2o5: 75, k2o: 37.5, other: "gypsum 500 kg/ha" }
      conditions: { crop: "GROUNDNUT", irrigation: null, soil: null }
      confidence: REGIONAL_INFERENCE

Source B: "ISSS NARP CDZ Table"
  authority_level: RESEARCH_INSTITUTION

  Evidence B1:
    claim: "Groundnut CDZ rainfed: 25:50:25 NPK"
    conditions: { crop: "GROUNDNUT", zone: "CDZ", irrigation: "RAINFED" }
    
    KnowledgeRecord B1K:
      content: { n: 25, p2o5: 50, k2o: 25 }
      conditions: { crop: "GROUNDNUT", irrigation: "RAINFED" }
      confidence: REGIONAL_INFERENCE

  Evidence B2:
    claim: "Groundnut CDZ irrigated: 25:75:38 + gypsum"
    conditions: { crop: "GROUNDNUT", zone: "CDZ", irrigation: "IRRIGATED" }
    
    KnowledgeRecord B2K:
      content: { n: 25, p2o5: 75, k2o: 38, other: "gypsum" }
      conditions: { crop: "GROUNDNUT", irrigation: "IRRIGATED" }
      confidence: REGIONAL_INFERENCE

ConflictingEvidence:
  record_a: A1K  (25:75:37.5, no irrigation condition)
  record_b: B1K  (25:50:25, rainfed)
  conflict_type: CONTEXT_DIFFERENCE
  resolution_status: RESOLVED_CONTEXT
  conditions_differ: { irrigation_status: [null, "RAINFED"] }
  resolution_notes: "A1K does not specify irrigation; B1K is explicitly rainfed.
                     The difference in P and K is likely due to irrigation context.
                     Both are valid zone-level recommendations."
```

## Query Pattern: "Why did we recommend this?"

```sql
SELECT 
  kr.content,
  kr.conditions,
  kr.confidence,
  e.claim_text,
  e.document_title,
  e.page_reference,
  e.geographic_resolution,
  e.conditions as evidence_conditions,
  s.name as source_name,
  s.authority_level,
  s.license_band
FROM knowledge_record kr
JOIN evidence e ON kr.evidence_id = e.id
JOIN source s ON e.source_id = s.id
WHERE kr.id = :recommendation_knowledge_record_id;
```

## Data Provenance Tags

Every piece of data entering the system is tagged:

| Tag | Meaning | Example |
|-----|---------|---------|
| `FARMER_ENTERED` | Farmer typed or selected this | Crop choice, sowing date |
| `FARM_MEASURED` | Physical measurement at the farm | Soil test result, GPS walk |
| `GOVERNMENT_DATA` | From a government source | Census village data, CIB&RC |
| `SCIENTIFIC_DATASET` | From published research | NBSS soil series, Kumar Naik 2020 |
| `SATELLITE_DERIVED` | Computed from satellite imagery | NDVI, estimated soil moisture |
| `MODEL_DERIVED` | From a computational model | NASA POWER weather, SoilGrids |
| `REGIONAL_INFERENCE` | Zone/district data applied to farm | Zone IV crop calendar |
| `DEMO_ONLY` | Demonstration data, NOT real | Any demo farm or recommendation |
