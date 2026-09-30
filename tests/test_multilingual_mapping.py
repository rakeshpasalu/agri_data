import unittest

class TestMultilingualMapping(unittest.TestCase):
    """
    Step 18 Test: Multilingual architecture.
    Do NOT duplicate business logic per language.
    Use canonical internal agricultural semantics.
    Support Kannada, Telugu, Hindi, English, and native/romanized scripts.
    """

    def setUp(self):
        # Canonical term dictionary mirroring agricultural_term & translation tables
        self.term_dictionary = {
            "GROUNDNUT": {
                "en": {"script": "Latin", "text": "Groundnut"},
                "kn": {"script": "Kannada", "text": "ಕಡಲೆಕಾಯಿ", "romanized": ["kadalekayi", "kadlekaayi"]},
                "te": {"script": "Telugu", "text": "వేరుశెనగ", "romanized": ["verusenaga", "verusanaga"]},
                "hi": {"script": "Devanagari", "text": "मूंगफली", "romanized": ["moongphali", "mungfali"]}
            },
            "FINGER_MILLET": {
                "en": {"script": "Latin", "text": "Finger millet"},
                "kn": {"script": "Kannada", "text": "ರಾಗಿ", "romanized": ["ragi"]},
                "te": {"script": "Telugu", "text": "రాగి", "romanized": ["ragi", "taidalu"]},
                "hi": {"script": "Devanagari", "text": "रागी", "romanized": ["ragi", "mandua"]}
            },
            "SOIL_MOISTURE": {
                "en": {"script": "Latin", "text": "Soil moisture"},
                "kn": {"script": "Kannada", "text": "ಮಣ್ಣಿನ ತೇವಾಂಶ", "romanized": ["mannina tevaansha"]},
                "te": {"script": "Telugu", "text": "నేల తేమ", "romanized": ["nela tema"]},
                "hi": {"script": "Devanagari", "text": "मिट्टी की नमी", "romanized": ["mitti ki nami"]}
            }
        }

    def parse_farmer_input(self, user_text):
        """
        Parses native script, romanized, or mixed language input to canonical semantic key.
        """
        clean_text = user_text.strip().lower()
        for canonical_key, translations in self.term_dictionary.items():
            for lang, data in translations.items():
                if data["text"].lower() in clean_text:
                    return canonical_key
                for r in data.get("romanized", []):
                    if r in clean_text:
                        return canonical_key
        return None

    def render_term(self, canonical_key, target_lang):
        return self.term_dictionary[canonical_key][target_lang]["text"]

    def test_native_kannada_input(self):
        canonical = self.parse_farmer_input("ನನ್ನ ಹೊಲದಲ್ಲಿ ಕಡಲೆಕಾಯಿ ಬಿತ್ತನೆ ಮಾಡಲು ಇಷ್ಟ")
        self.assertEqual(canonical, "GROUNDNUT")

    def test_romanized_kannada_input(self):
        canonical = self.parse_farmer_input("nanna holadalli kadalekayi bittane madalu ishta")
        self.assertEqual(canonical, "GROUNDNUT")

    def test_native_telugu_input(self):
        canonical = self.parse_farmer_input("మా పొలంలో వేరుశెనగ వేయాలనుకుంటున్నాము")
        self.assertEqual(canonical, "GROUNDNUT")

    def test_mixed_language_input(self):
        canonical = self.parse_farmer_input("My farm has low mannina tevaansha")
        self.assertEqual(canonical, "SOIL_MOISTURE")

    def test_canonical_rendering(self):
        self.assertEqual(self.render_term("SOIL_MOISTURE", "kn"), "ಮಣ್ಣಿನ ತೇವಾಂಶ")
        self.assertEqual(self.render_term("SOIL_MOISTURE", "te"), "నేల తేమ")
        self.assertEqual(self.render_term("SOIL_MOISTURE", "hi"), "मिट्टी की नमी")

if __name__ == "__main__":
    unittest.main()
