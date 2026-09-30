# Architecture Document — Agricultural Intelligence Platform

**Version:** 0.1.0
**Date:** 2026-09-30
**Status:** Foundation

---

## 1. System Purpose

A scientifically traceable agricultural decision-support system whose AI interface can speak to farmers naturally.

**Core principle:** The architecture must make it impossible — or at least difficult — for an LLM hallucination to become a farming recommendation.

## 2. Design Philosophy

### What This System IS:
- A data + knowledge + evidence engine that produces traceable recommendations
- An AI interface that translates between farmer language and agricultural science
- A farm digital twin that records and learns from actual farming activities
- A transparent system that always explains WHY it recommends something

### What This System IS NOT:
- A chatbot that sounds agricultural
- An LLM that generates farming advice from training data
- A recommendation engine that invents precision where none exists

## 3. Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│              Layer 1: Presentation / Interface           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Farmer App   │  │ Admin View   │  │ API Clients  │  │
│  │ (Multilingual│  │ (Internal)   │  │              │  │
│  │  PWA)        │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Layer 2: AI Interface                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  LLM Gateway (Translation / Explanation only)    │   │
│  │  - Understands farmer language (mixed-script)    │   │
│  │  - Translates recommendations to farmer language │   │
│  │  - Asks clarifying questions                     │   │
│  │  - CANNOT override regulatory blocks             │   │
│  │  - CANNOT invent agricultural facts              │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              Layer 3: Decision Engine (Deterministic)    │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │
│  │ Crop   │ │Nutrient│ │ Pest/  │ │ Market │          │
│  │Suitab. │ │ Engine │ │Disease │ │ Engine │          │
│  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘          │
│      │          │          │          │                  │
│  ┌───┴──────────┴──────────┴──────────┘                 │
│  │  Regulatory Safety Gate (HARD BOUNDARY)              │
│  │  Checks EVERY chemical recommendation               │
│  │  CIB&RC registered ∩ NOT banned → ALLOW             │
│  │  Everything else → BLOCK                             │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              Layer 4: Knowledge + Evidence               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Agricultural Knowledge Base                     │   │
│  │  - KnowledgeRecord (with conditions)             │   │
│  │  - Evidence (linked to source documents)         │   │
│  │  - Source (authority, license, freshness)         │   │
│  │  - ConflictingEvidence (stored, not averaged)    │   │
│  │  - KnowledgeVersion (audit trail)                │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              Layer 5: Farm Digital Twin                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Farm → Plot → CropCycle → Activities            │   │
│  │  SoilTest, WaterSource, Observations             │   │
│  │  Expenses, Harvest, Sale                         │   │
│  │  Every field tagged with data_provenance          │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│              Layer 6: Data Providers (Pluggable)         │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │
│  │Weather │ │Market  │ │Satellite│ │Knowledge│         │
│  │Provider│ │Provider│ │Provider │ │Ingestion│         │
│  └────────┘ └────────┘ └────────┘ └────────┘          │
├─────────────────────────────────────────────────────────┤
│              Layer 7: Infrastructure                     │
│  PostgreSQL/PostGIS │ Redis │ S3-compatible │ Kafka     │
└─────────────────────────────────────────────────────────┘
```

## 4. Module Boundaries

The system is built as a **modular monolith** with clear module boundaries designed for later service extraction:

| Module | Responsibility | Can Be Extracted? |
|--------|---------------|-------------------|
| `evidence` | Source, Evidence, KnowledgeRecord management | YES — becomes Knowledge Service |
| `farm` | Farm, Plot, SoilTest, WaterSource | YES — becomes Farm Service |
| `crop` | Crop, Variety, Calendar, Requirements | YES — stays with evidence |
| `cropcycle` | CropCycle, Activities, Harvest, Sales | YES — becomes Farm Diary Service |
| `recommendation` | Suitability, Nutrient, Pest/Disease engines | YES — becomes Decision Service |
| `regulation` | InputProduct, InputRegulation, RegulatoryGate | YES — becomes Safety Service |
| `market` | Market, MarketPrice, MarketDataProvider | YES — becomes Market Service |
| `weather` | WeatherObservation, WeatherProvider | YES — becomes Weather Service |
| `i18n` | Agricultural terms, translations | SHARED — library module |
| `rag` | Document ingestion, embedding, retrieval | YES — becomes RAG Service |
| `ai` | LLM interface, conversation management | YES — becomes AI Service |

## 5. Data Flow

### Recommendation Flow
```
Farmer asks "What should I plant?"
    │
    ▼
AI Interface (LLM)
    │ Maps natural language to structured query
    ▼
Decision Engine receives: {farmId, plotId, season, date}
    │
    ├─→ Check: Does plot have soil test?
    │     NO → Return INSUFFICIENT_DATA ["soil test needed"]
    │     YES → Continue
    │
    ├─→ Check: What is the agro-climatic zone?
    │     Look up farm location → zone mapping
    │
    ├─→ Check: What crops are suitable for zone + season + soil?
    │     Query KnowledgeRecords with conditions matching
    │
    ├─→ Check: What is the water availability?
    │     Rainfed vs irrigated affects crop list
    │
    ├─→ For each candidate crop:
    │     ├─→ Zone suitability (KnowledgeRecord)
    │     ├─→ Soil suitability (soil test vs requirements)
    │     ├─→ Water suitability (crop water need vs availability)
    │     ├─→ Season/calendar fit (planting date vs crop calendar)
    │     ├─→ Previous crop compatibility (if known)
    │     └─→ Evidence confidence for each factor
    │
    ├─→ Compile results with status + reasons + evidence
    │
    ▼
AI Interface (LLM)
    │ Translates structured result to farmer language
    │ Includes: what we know, what we don't, why we recommend
    ▼
Farmer receives recommendation in Kannada/Telugu/Hindi
```

### Evidence Flow
```
Any recommendation
    │
    ▼
"Why did you recommend this?"
    │
    ▼
Recommendation
    → KnowledgeRecord (e.g., "Groundnut suitable Zone IV kharif")
        → Evidence (e.g., "UASB PoP 2023, Chapter: Groundnut")
            → Source (e.g., "UAS Bangalore Package of Practices")
                → Authority: UNIVERSITY
                → License: YELLOW (cite, don't redistribute)
                → Geographic scope: Zone IV, Karnataka
                → Publication date: 2023
                → Conditions: kharif season, red sandy loam
```

## 6. Key Design Decisions

### 6.1 Evidence-First Architecture
Every agricultural knowledge record is stored with its full provenance chain. This is not optional metadata — it's the primary data structure.

### 6.2 Regulatory Hard Gate
Chemical recommendations pass through `RegulatoryGate` BEFORE reaching the user. This gate is in compiled code, not in an LLM prompt. A banned pesticide cannot reach the user regardless of what any LLM, knowledge record, or extension advisory says.

### 6.3 Conflicting Evidence Preserved
When two authoritative sources disagree (e.g., groundnut RDF), both are stored with their conditions. The system does NOT average them. Instead, it identifies which conditions match the farmer's situation. If it cannot resolve the conflict, it returns `CONFLICTING_EVIDENCE` and explains.

### 6.4 Progressive Questioning
The system does not ask 30 questions upfront. It:
1. Gets farm location
2. Determines what it can auto-derive (zone, weather, elevation)
3. Asks for crop or objective
4. Identifies what's missing for THAT specific question
5. Asks for the minimum additional information
6. Clearly states what it still doesn't know

### 6.5 INSUFFICIENT_DATA Is a Valid Response
If the system cannot produce a scientifically defensible recommendation, it says so. This is not a bug — it's the most important feature.

## 7. Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Backend | Java 21 + Spring Boot 3.3 | Enterprise robustness, strong typing, mature ecosystem |
| Database | PostgreSQL 16 + PostGIS | Spatial queries for farm polygons, mature, reliable |
| Migrations | Flyway | Standard, reliable, versioned |
| Cache | Redis | Weather and market price caching |
| Object storage | S3-compatible (MinIO dev) | Farm photos, documents |
| Python services | ML, RAG, satellite | When needed — not in V1 foundation |
| Frontend | TBD (after backend stabilizes) | Offline-first PWA |
| LLM | Provider-agnostic interface | Not coupled to one LLM vendor |

## 8. Security Considerations

- Farmer data (phone, location, land records) is sensitive — PII handling required
- Phone numbers stored as hashes where identification is not needed
- Farm polygons are the farmer's own data — consent required for sharing
- Soil health card data entered by farmer — not scraped from government portals
- Regulatory data is public but must be kept current — stale data is a safety risk

## 9. Deployment Architecture (V1)

Start simple:
- Single application server (Spring Boot)
- Single PostgreSQL instance (with PostGIS)
- Redis for caching
- File storage for photos (local/S3)
- Nginx reverse proxy

Scale when needed, not before.
