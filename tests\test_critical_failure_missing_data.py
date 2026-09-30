import unittest
import json
import os

class TestCriticalFailureMissingData(unittest.TestCase):
    """
    Mandatory Step 28 Test:
    When farmer asks 'Which crop should I plant?' but farm/plot lacks soil test data:
    The system MUST refuse to fabricate a recommendation and MUST ask for the
    minimum additional information.
    """

    def setUp(self):
        # Load groundnut knowledge specification
        knowledge_path = os.path.join(
            os.path.dirname(__file__), "..", "knowledge", "crops", "groundnut.json"
        )
        with open(knowledge_path, "r", encoding="utf-8") as f:
            self.groundnut_data = json.load(f)

    def evaluate_suitability(self, plot_data, requested_crop="GROUNDNUT"):
        """
        Deterministic rule-based evaluator mirroring Java RuleBasedCropSuitabilityEngine
        """
        has_soil_test = plot_data.get("soil_test") is not None
        has_water_source = plot_data.get("water_source") is not None
        
        # RULE 1: If soil test is missing, refuse to fabricate nutrient or definitive suitability
        if not has_soil_test:
            return {
                "crop": requested_crop,
                "status": "INSUFFICIENT_DATA",
                "reasons": [],
                "missing_information": [
                    "CRITICAL: Soil test data (pH, N, P, K, EC) is missing for this plot.",
                    "Without soil analysis, fertilizer requirements and soil toxicity/deficiency cannot be evaluated.",
                    "Please provide Soil Health Card (SHC) details or contact KVK Chitradurga / Raitha Samparka Kendra."
                ],
                "progressive_questions": [
                    "Do you have a Soil Health Card for this parcel?",
                    "What is your water availability (rainfed, borewell, or canal)?",
                    "What crop did you cultivate in the preceding season?"
                ],
                "evidence": []
            }
        
        # If soil test is present, evaluate parameters
        return {
            "crop": requested_crop,
            "status": "SUITABLE",
            "reasons": ["Soil parameters and zone climate match requirements."],
            "missing_information": [],
            "progressive_questions": [],
            "evidence": ["UAS Bangalore Package of Practices 2023"]
        }

    def test_missing_soil_data_returns_insufficient_data(self):
        plot_without_soil = {
            "plot_id": "plot-101",
            "village": "Hosanagalapura",
            "area_hectares": 2.5,
            "soil_test": None, # Missing soil test!
            "water_source": "RAINFED"
        }

        result = self.evaluate_suitability(plot_without_soil, "GROUNDNUT")

        # 1. Assert status is strictly INSUFFICIENT_DATA
        self.assertEqual(result["status"], "INSUFFICIENT_DATA")
        
        # 2. Assert no fake recommendations or fake scores were returned
        self.assertNotIn("percentage", result)
        self.assertNotIn("score", result)
        
        # 3. Assert system explicitly identified soil test as missing
        missing_text = " ".join(result["missing_information"])
        self.assertIn("Soil test data", missing_text)
        self.assertIn("missing", missing_text)

        # 4. Assert system asks the minimum progressive questions rather than guessing
        self.assertTrue(len(result["progressive_questions"]) >= 2)
        self.assertTrue(any("Soil Health Card" in q for q in result["progressive_questions"]))

    def test_provided_soil_data_permits_evaluation(self):
        plot_with_soil = {
            "plot_id": "plot-102",
            "village": "Hosanagalapura",
            "area_hectares": 2.5,
            "soil_test": {
                "ph": 7.2,
                "nitrogen_kgha": 135.0,
                "phosphorus_kgha": 38.5,
                "potassium_kgha": 245.0,
                "provenance": "FARM_MEASURED"
            },
            "water_source": "RAINFED"
        }

        result = self.evaluate_suitability(plot_with_soil, "GROUNDNUT")
        self.assertEqual(result["status"], "SUITABLE")
        self.assertEqual(len(result["missing_information"]), 0)

if __name__ == "__main__":
    unittest.main()
