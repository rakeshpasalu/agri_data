import unittest
import json
import os

class TestConflictingEvidenceHandling(unittest.TestCase):
    """
    Step 7 Test: Handle conflicting agricultural information.
    Do NOT merge conflicting recommendations into an invented average.
    Determine whether difference comes from: soil, rainfed vs irrigated, zone, etc.
    If conflict cannot be resolved: store both, mark CONFLICTING_EVIDENCE, require additional information.
    """

    def setUp(self):
        crop_path = os.path.join(
            os.path.dirname(__file__), "..", "knowledge", "crops", "groundnut.json"
        )
        with open(crop_path, "r", encoding="utf-8") as f:
            self.groundnut = json.load(f)

    def evaluate_nutrient_dose(self, plot_context):
        conflict_data = self.groundnut["nutrient_evidence_conflict"]
        records = conflict_data["records"]

        irrigation = plot_context.get("irrigation_status") # "RAINFED" or "IRRIGATED"
        has_soil_test = plot_context.get("has_soil_test", False)

        if not has_soil_test:
            return {
                "status": "INSUFFICIENT_DATA",
                "message": "Cannot recommend specific fertilizer without soil test."
            }

        # Check if irrigation resolves the conflict
        if irrigation == "RAINFED":
            # Select the rainfed record
            selected = [r for r in records if "rainfed" in r["condition"].lower()][0]
            return {
                "status": "RESOLVED_BY_CONTEXT",
                "context_resolved": "RAINFED",
                "recommended_rdf": selected["npk_kgha"],
                "source": selected["source"],
                "authority": selected["authority"],
                "conflict_acknowledged": True,
                "notes": "Rainfed dryland Alfisol baseline applied. Irrigated recommendation (75kg P2O5) was excluded due to lack of irrigation."
            }
        elif irrigation == "IRRIGATED":
            selected = [r for r in records if "irrigated" in r["condition"].lower()][0]
            return {
                "status": "RESOLVED_BY_CONTEXT",
                "context_resolved": "IRRIGATED",
                "recommended_rdf": selected["npk_kgha"],
                "source": selected["source"],
                "authority": selected["authority"],
                "secondary_nutrients": selected["secondary_nutrients"],
                "conflict_acknowledged": True
            }
        else:
            # Cannot resolve -> return both without averaging
            return {
                "status": "CONFLICTING_EVIDENCE",
                "conflicting_records": records,
                "resolution_policy": "NO_AVERAGING",
                "message": "Two authoritative sources recommend different doses. System refuses to calculate an artificial average (e.g. 25:62.5:31.25). Please specify whether plot is rainfed or irrigated."
            }

    def test_conflict_not_averaged_when_irrigation_unknown(self):
        result = self.evaluate_nutrient_dose({"has_soil_test": True, "irrigation_status": None})
        self.assertEqual(result["status"], "CONFLICTING_EVIDENCE")
        self.assertEqual(result["resolution_policy"], "NO_AVERAGING")
        # Ensure system did not produce an invented average
        self.assertNotIn("recommended_rdf", result)
        self.assertEqual(len(result["conflicting_records"]), 2)

    def test_conflict_resolved_honestly_by_rainfed_context(self):
        result = self.evaluate_nutrient_dose({"has_soil_test": True, "irrigation_status": "RAINFED"})
        self.assertEqual(result["status"], "RESOLVED_BY_CONTEXT")
        self.assertEqual(result["recommended_rdf"], {"n": 25, "p2o5": 50, "k2o": 25})
        self.assertTrue(result["conflict_acknowledged"])

if __name__ == "__main__":
    unittest.main()
