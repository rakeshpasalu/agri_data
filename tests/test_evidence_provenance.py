import unittest
import json
import os

class TestEvidenceProvenance(unittest.TestCase):
    """
    Step 6 Test: Evidence is first-class data.
    Every recommendation must have full provenance:
    Recommendation -> KnowledgeRecord -> Source -> Document -> Publication Date -> License Band -> Conditions
    The system must always be able to answer: 'Why did we recommend this?'
    """

    def setUp(self):
        crops_dir = os.path.join(os.path.dirname(__file__), "..", "knowledge", "crops")
        with open(os.path.join(crops_dir, "groundnut.json"), "r", encoding="utf-8") as f:
            self.groundnut = json.load(f)
        with open(os.path.join(crops_dir, "finger_millet.json"), "r", encoding="utf-8") as f:
            self.ragi = json.load(f)

    def test_groundnut_has_traceable_sources(self):
        sources = self.groundnut["crop"]["verified_sources"]
        self.assertTrue(len(sources) >= 3)
        self.assertTrue(any("UAS Bangalore" in s for s in sources))
        self.assertTrue(any("KSSC" in s for s in sources))

    def test_finger_millet_has_traceable_sources(self):
        sources = self.ragi["crop"]["verified_sources"]
        self.assertTrue(len(sources) >= 3)
        self.assertTrue(any("UAS Bangalore" in s for s in sources))

    def test_varieties_explicitly_separate_suitability_from_availability(self):
        """Step 11 Test: Separate scientifically suitable from currently available for purchase."""
        for v in self.groundnut["varieties"]:
            self.assertTrue(v["kssc_catalogued"])
            # System must NOT claim unverified local stock is available
            self.assertFalse(v["local_dealer_availability_verified"])

        for v in self.ragi["varieties"]:
            self.assertTrue(v["kssc_catalogued"])
            self.assertFalse(v["local_dealer_availability_verified"])

if __name__ == "__main__":
    unittest.main()
