-- ============================================================================
-- DEMO DATA — NOT REAL FARM
-- ============================================================================
-- This file contains DEMONSTRATION data only.
-- Every record is tagged with data_provenance = 'DEMO_ONLY'.
-- These records MUST NEVER be used in production recommendation paths.
-- They exist solely to demonstrate the system's recommendation flow.
-- ============================================================================
-- DEMO SCENARIO: A hypothetical farmer near Hosanagalapura, Molakalmuru taluk
-- ============================================================================

-- Source: Phase-0 research (for evidence chain demonstration)
INSERT INTO source (id, name, authority_level, url, publication_date, geographic_scope, license_band, retrieved_at)
VALUES 
  ('a0000001-0000-0000-0000-000000000001', 'DEMO: UAS Bangalore Package of Practices', 'UNIVERSITY', 'https://uasbangalore.edu.in', '2023-01-01', 'Zone IV, Karnataka', 'YELLOW', '2026-09-29'),
  ('a0000001-0000-0000-0000-000000000002', 'DEMO: KSSC Product List', 'INDUSTRY', 'https://ksscl.karnataka.gov.in', '2026-01-01', 'Karnataka', 'GREEN', '2026-09-29'),
  ('a0000001-0000-0000-0000-000000000003', 'DEMO: CIB&RC Banned List', 'GOVERNMENT', 'https://ppqs.gov.in', '2026-07-31', 'India', 'GREEN', '2026-09-29'),
  ('a0000001-0000-0000-0000-000000000004', 'DEMO: Kumar Naik et al. 2020', 'PEER_REVIEWED_JOURNAL', 'https://doi.org/10.22271/chemi.2020.v8.i3ak.9595', '2020-01-01', 'Molakalmuru taluk', 'YELLOW', '2026-09-29'),
  ('a0000001-0000-0000-0000-000000000005', 'DEMO: NASA POWER API', 'GOVERNMENT', 'https://power.larc.nasa.gov', '2026-09-29', 'Global (gridded)', 'GREEN', '2026-09-29');

-- Evidence records
INSERT INTO evidence (id, source_id, document_url, claim_text, geographic_applicability, observation_type, verified, notes)
VALUES 
  ('b0000001-0000-0000-0000-000000000001', 'a0000001-0000-0000-0000-000000000001',
   'DEMO_DOCUMENT', 'Groundnut is a primary kharif crop in Zone IV with sowing from onset of monsoon (June-July)',
   '{"zone": "ZONE_IV", "state": "KA"}', 'EXPERT_OPINION', true,
   'DEMO_ONLY: Extracted from UASB PoP for demonstration'),
  ('b0000001-0000-0000-0000-000000000002', 'a0000001-0000-0000-0000-000000000002',
   'DEMO_DOCUMENT', 'KSSC lists groundnut varieties: TMV-2, GPBD-4, K-6, G-2-52, GKVK-5, KCG-6',
   '{"state": "KA"}', 'SURVEY_DATA', true,
   'DEMO_ONLY: From KSSC website variety listing'),
  ('b0000001-0000-0000-0000-000000000003', 'a0000001-0000-0000-0000-000000000003',
   'DEMO_DOCUMENT', 'Monocrotophos is on the banned/restricted list as of 31.07.2026',
   '{"country": "IN"}', 'SURVEY_DATA', true,
   'DEMO_ONLY: CIB&RC regulatory status'),
  ('b0000001-0000-0000-0000-000000000004', 'a0000001-0000-0000-0000-000000000004',
   'DEMO_DOCUMENT', 'Molakalmuru taluk surface soil: pH 6.00-8.00 (mean 7.16), N 46-238 kg/ha (mean 120)',
   '{"taluk": "MOLAKALMURU", "district": "CHITRADURGA", "state": "KA"}', 'LABORATORY_ANALYSIS', true,
   'DEMO_ONLY: From published paper, n=148 samples');

-- Crop: Groundnut
INSERT INTO crop (id, canonical_name, scientific_name, crop_type, crop_group)
VALUES ('c0000001-0000-0000-0000-000000000001', 'GROUNDNUT', 'Arachis hypogaea', 'OILSEED', 'LEGUMES');

-- Crop name mappings (multilingual)
INSERT INTO crop_name_mapping (id, crop_id, language_code, name, script, is_primary) VALUES
  ('d0000001-0000-0000-0000-000000000001', 'c0000001-0000-0000-0000-000000000001', 'en', 'Groundnut', 'LATIN', true),
  ('d0000001-0000-0000-0000-000000000002', 'c0000001-0000-0000-0000-000000000001', 'kn', 'ಕಡಲೆಕಾಯಿ', 'KANNADA', true),
  ('d0000001-0000-0000-0000-000000000003', 'c0000001-0000-0000-0000-000000000001', 'te', 'వేరుశెనగ', 'TELUGU', true),
  ('d0000001-0000-0000-0000-000000000004', 'c0000001-0000-0000-0000-000000000001', 'hi', 'मूंगफली', 'DEVANAGARI', true);

-- Crop: Finger Millet (Ragi)
INSERT INTO crop (id, canonical_name, scientific_name, crop_type, crop_group)
VALUES ('c0000001-0000-0000-0000-000000000002', 'FINGER_MILLET', 'Eleusine coracana', 'CEREAL', 'MILLETS');

INSERT INTO crop_name_mapping (id, crop_id, language_code, name, script, is_primary) VALUES
  ('d0000001-0000-0000-0000-000000000005', 'c0000001-0000-0000-0000-000000000002', 'en', 'Finger millet', 'LATIN', true),
  ('d0000001-0000-0000-0000-000000000006', 'c0000001-0000-0000-0000-000000000002', 'kn', 'ರಾಗಿ', 'KANNADA', true),
  ('d0000001-0000-0000-0000-000000000007', 'c0000001-0000-0000-0000-000000000002', 'te', 'రాగి', 'TELUGU', true),
  ('d0000001-0000-0000-0000-000000000008', 'c0000001-0000-0000-0000-000000000002', 'hi', 'रागी', 'DEVANAGARI', true);

-- Groundnut varieties (from KSSC — DEMO labeled)
INSERT INTO crop_variety (id, crop_id, variety_name, released_by, duration_days_min, duration_days_max, season, characteristics, source_id) VALUES
  ('e0000001-0000-0000-0000-000000000001', 'c0000001-0000-0000-0000-000000000001', 'TMV-2', 'TNAU', 105, 110, 'KHARIF', '{"type": "Spanish bunch", "note": "DEMO_ONLY"}', 'a0000001-0000-0000-0000-000000000002'),
  ('e0000001-0000-0000-0000-000000000002', 'c0000001-0000-0000-0000-000000000001', 'GPBD-4', 'UASB', 110, 120, 'KHARIF', '{"type": "Spanish bunch", "note": "DEMO_ONLY"}', 'a0000001-0000-0000-0000-000000000002'),
  ('e0000001-0000-0000-0000-000000000003', 'c0000001-0000-0000-0000-000000000001', 'K-6', 'UAS', 105, 115, 'KHARIF', '{"note": "DEMO_ONLY"}', 'a0000001-0000-0000-0000-000000000002');

-- Crop calendar (Zone IV groundnut)
INSERT INTO crop_calendar (id, crop_id, zone, season, sowing_start_month, sowing_end_month, harvest_start_month, harvest_end_month, evidence_id) VALUES
  ('f0000001-0000-0000-0000-000000000001', 'c0000001-0000-0000-0000-000000000001', 'ZONE_IV', 'KHARIF', 6, 7, 10, 11, 'b0000001-0000-0000-0000-000000000001');

-- Regulatory: Monocrotophos is BANNED
INSERT INTO input_product (id, product_name, active_ingredient, formulation_type, manufacturer, cibrc_registration_number) VALUES
  ('g0000001-0000-0000-0000-000000000001', 'DEMO: Monocrotophos 36 SL', 'monocrotophos', '36 SL', 'DEMO_MANUFACTURER', 'DEMO_REG');

INSERT INTO input_regulation (id, input_product_id, regulatory_status, effective_date, applicable_crops, applicable_pests, source_id, notes) VALUES
  ('h0000001-0000-0000-0000-000000000001', 'g0000001-0000-0000-0000-000000000001', 'BANNED', '2026-07-31', '{}', '{}', 'a0000001-0000-0000-0000-000000000003', 'DEMO_ONLY: Monocrotophos is banned/restricted per CIB&RC');

-- Regulatory: Azadirachtin is REGISTERED (biopesticide)
INSERT INTO input_product (id, product_name, active_ingredient, formulation_type, manufacturer, cibrc_registration_number) VALUES
  ('g0000001-0000-0000-0000-000000000002', 'DEMO: Neem-based Azadirachtin 0.03% EC', 'azadirachtin', '0.03% EC', 'DEMO_MANUFACTURER', 'DEMO_REG_AZ');

INSERT INTO input_regulation (id, input_product_id, regulatory_status, effective_date, applicable_crops, applicable_pests, source_id, notes) VALUES
  ('h0000001-0000-0000-0000-000000000002', 'g0000001-0000-0000-0000-000000000002', 'REGISTERED', '2026-03-31', '{GROUNDNUT,COTTON,RICE}', '{LEAF_MINER,APHID}', 'a0000001-0000-0000-0000-000000000003', 'DEMO_ONLY: Biopesticide registered for multiple crops');

-- Nearby markets
INSERT INTO market (id, name, market_type, location, district, state, agmarknet_code) VALUES
  ('i0000001-0000-0000-0000-000000000001', 'DEMO: Challakere APMC', 'APMC', ST_SetSRID(ST_MakePoint(76.651, 14.318), 4326), 'CHITRADURGA', 'KA', 'DEMO_CHK'),
  ('i0000001-0000-0000-0000-000000000002', 'DEMO: Hiriyur APMC', 'APMC', ST_SetSRID(ST_MakePoint(76.616, 13.945), 4326), 'CHITRADURGA', 'KA', 'DEMO_HIR'),
  ('i0000001-0000-0000-0000-000000000003', 'DEMO: Chitradurga APMC', 'APMC', ST_SetSRID(ST_MakePoint(76.395, 14.226), 4326), 'CHITRADURGA', 'KA', 'DEMO_CTD');

-- Agricultural terms (multilingual demo)
INSERT INTO agricultural_term (id, canonical_key, category, english_term) VALUES
  ('j0000001-0000-0000-0000-000000000001', 'SOIL_MOISTURE', 'SOIL', 'Soil moisture'),
  ('j0000001-0000-0000-0000-000000000002', 'SOIL_PH', 'SOIL', 'Soil pH'),
  ('j0000001-0000-0000-0000-000000000003', 'NITROGEN', 'NUTRIENT', 'Nitrogen'),
  ('j0000001-0000-0000-0000-000000000004', 'RAINFALL', 'WEATHER', 'Rainfall'),
  ('j0000001-0000-0000-0000-000000000005', 'SOWING', 'ACTIVITY', 'Sowing');

INSERT INTO agricultural_term_translation (id, term_id, language_code, translated_term, script, romanized, verified) VALUES
  ('k0000001-0000-0000-0000-000000000001', 'j0000001-0000-0000-0000-000000000001', 'kn', 'ಮಣ್ಣಿನ ತೇವಾಂಶ', 'KANNADA', 'mannina tevaansha', true),
  ('k0000001-0000-0000-0000-000000000002', 'j0000001-0000-0000-0000-000000000001', 'te', 'నేల తేమ', 'TELUGU', 'nela tema', true),
  ('k0000001-0000-0000-0000-000000000003', 'j0000001-0000-0000-0000-000000000001', 'hi', 'मिट्टी की नमी', 'DEVANAGARI', 'mitti ki nami', true),
  ('k0000001-0000-0000-0000-000000000004', 'j0000001-0000-0000-0000-000000000002', 'kn', 'ಮಣ್ಣಿನ pH', 'KANNADA', 'mannina pH', true),
  ('k0000001-0000-0000-0000-000000000005', 'j0000001-0000-0000-0000-000000000003', 'kn', 'ಸಾರಜನಕ', 'KANNADA', 'saarajanaka', true),
  ('k0000001-0000-0000-0000-000000000006', 'j0000001-0000-0000-0000-000000000004', 'kn', 'ಮಳೆ', 'KANNADA', 'male', true),
  ('k0000001-0000-0000-0000-000000000007', 'j0000001-0000-0000-0000-000000000005', 'kn', 'ಬಿತ್ತನೆ', 'KANNADA', 'bittane', true);

-- ============================================================================
-- END OF DEMO DATA
-- Every record above is for DEMONSTRATION PURPOSES ONLY.
-- These UUIDs are prefixed with recognizable patterns (a0000001, b0000001, etc.)
-- to make them easily identifiable as demo data.
-- ============================================================================
