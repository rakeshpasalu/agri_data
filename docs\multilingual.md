# Multilingual Architecture — Design Document

**Version:** 0.1.0
**Date:** 2026-09-30

---

## Core Principle

**Do NOT duplicate business logic per language.** Use canonical internal agricultural semantics. The multilingual layer is a rendering concern, not a knowledge concern.

## Internal Representation

All agricultural knowledge, rules, and recommendations operate on **canonical English/scientific keys**:

```
SOIL_MOISTURE         (not ಮಣ್ಣಿನ ತೇವಾಂಶ or नमी)
GROUNDNUT             (not ಕಡಲೆಕಾಯಿ or मूंगफली)
LATE_LEAF_SPOT         (not ತಡವಾದ ಎಲೆ ಚುಕ್ಕೆ)
NITROGEN_DEFICIENCY    (not ಸಾರಜನಕ ಕೊರತೆ)
```

## Target Languages (Phased)

### Phase 1 (Pilot)
| Language | Script | ISO 639-1 | Rationale |
|----------|--------|-----------|-----------|
| Kannada | ಕನ್ನಡ | kn | State language, majority local |
| Telugu | తెలుగు | te | Widely spoken in Molakalmuru (border taluk) |
| English | Latin | en | Administrative, extension documents |

### Phase 2
| Language | Script | ISO 639-1 |
|----------|--------|-----------|
| Hindi | देवनागरी | hi |
| Marathi | देवनागरी | mr |

### Phase 3 (All major Indian)
| Language | Script | ISO 639-1 |
|----------|--------|-----------|
| Tamil | தமிழ் | ta |
| Malayalam | മലയാളം | ml |
| Bengali | বাংলা | bn |
| Gujarati | ગુજરાતી | gu |
| Punjabi | ਗੁਰਮੁਖੀ | pa |
| Odia | ଓଡ଼ିଆ | or |
| Assamese | অসমীয়া | as |
| Urdu | اردو | ur |

### Phase 4
| Language | Script | ISO 639-1 |
|----------|--------|-----------|
| Simplified Chinese | 简体中文 | zh-CN |

## Agricultural Term Mapping

### Schema
```sql
agricultural_term (
    canonical_key: "SOIL_MOISTURE"
    category: "SOIL"
    english_term: "Soil moisture"
)

agricultural_term_translation (
    term_id: → SOIL_MOISTURE
    language_code: "kn"
    translated_term: "ಮಣ್ಣಿನ ತೇವಾಂಶ"
    script: "KANNADA"
    romanized: "mannina tevaansha"
    verified: true
)
```

### Term Categories
- **SOIL**: pH, moisture, organic carbon, nutrients, texture, depth
- **CROP**: crop names, growth stages, planting, harvesting
- **PEST**: pest names, symptoms, damage types
- **DISEASE**: disease names, symptoms, causal agents
- **WEATHER**: rainfall, temperature, humidity, wind
- **MARKET**: price, quantity, quality grade, commission
- **INPUT**: fertilizer types, pesticide types, seed
- **FARM**: plot, survey number, area, irrigation
- **ADVISORY**: sow, harvest, apply, spray, irrigate

### Term Sources (for Kannada)
1. **UASB PoP Kannada chapters** — authentic agricultural Kannada
2. **KVK Chitradurga reports** — extension Kannada
3. **KSDA scheme GOs** — administrative Kannada
4. **AI4Bharat Indic-Glossaries** — agricultural domain (~4,807 terms total)
5. **Manual curation** — validated by extension workers

### What We Do NOT Do
- Use generic MT for pest names (translation of "late blight" word-by-word ≠ agricultural term)
- Copy Bharat Jargons / KissanAI glossaries (RED license)
- Assume Kannada terms are the same in all Karnataka districts (dialect variation exists)

## Input Handling

Farmers may input in:
1. **Native script**: ಕಡಲೆಕಾಯಿ
2. **Romanized**: kadalekayi, kadlekaayi, groundnut
3. **Mixed language**: "My groundnut ಬೆಳೆ has ಹಳದಿ leaf"
4. **Hindi/Telugu with Kannada**: common in border areas
5. **Voice**: speech-to-text (ASR) → Bhashini/IndicTrans2
6. **OCR**: photographed documents (SHC, bills)

### Processing Pipeline
```
Raw input (any language/script/mixed)
  │
  ├─→ Script detection (Kannada, Telugu, Devanagari, Latin)
  │
  ├─→ Romanized → script normalization (kadalekayi → ಕಡಲೆಕಾಯಿ)
  │
  ├─→ Token-level language identification (for mixed input)
  │
  ├─→ Agricultural term recognition (against term table)
  │
  ├─→ LLM entity extraction (for free-form descriptions)
  │
  ├─→ Map to canonical keys
  │
  ▼
Canonical representation for business logic
```

## Output Rendering

```
Business logic result (canonical):
  { crop: "GROUNDNUT", status: "SUITABLE", evidence: [...] }
  │
  ├─→ Look up farmer's preferred_language
  │
  ├─→ Render agricultural terms from translation table
  │
  ├─→ LLM generates natural language explanation in target language
  │
  ├─→ Post-processing: verify no untranslated technical terms
  │
  ▼
Farmer sees:
  "ನಿಮ್ಮ ಭೂಮಿಗೆ ಕಡಲೆಕಾಯಿ ಬೆಳೆ ಸೂಕ್ತ..."
  (Your land is suitable for groundnut crop...)
```

## Text-to-Speech / Speech-to-Text

### ASR (Farmer → System)
- **Primary**: Bhashini ASR models for Kannada/Telugu/Hindi
- **License**: YELLOW — requires Bhashini onboarding
- **Fallback**: Google Cloud Speech-to-Text (Kannada support exists)

### TTS (System → Farmer)
- **Primary**: Bhashini TTS or Google Cloud TTS
- **Use case**: Voice readout of recommendations for low-literacy farmers
- **Critical**: Agricultural terms must be pronounced correctly (not generic TTS)

## OCR (Photos → Data)
- **SHC card photos**: Extract soil test values from photographed Soil Health Cards
- **Bill photos**: Extract input product names, quantities, costs
- **Technology**: Google Cloud Vision or Tesseract with Indic script support
- **Challenge**: Kannada OCR accuracy for printed vs handwritten
