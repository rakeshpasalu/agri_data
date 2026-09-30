import unittest
import json
import os

class TestRegulatorySafetyBoundary(unittest.TestCase):
    """
    Step 14 Test: Hard regulatory safety boundary.
    Before any chemical recommendation is presented, it must pass CIB&RC check.
    If BANNED, UNKNOWN, or CONFLICTING -> BLOCK.
    """

    def setUp(self):
        reg_path = os.path.join(
            os.path.dirname(__file__), "..", "knowledge", "regulations", "cibrc_pesticide_registry.json"
        )
        with open(reg_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

    def check_regulatory_gate(self, active_ingredient, crop, pest):
        ingredient_normalized = active_ingredient.strip().lower()
        
        # 1. Check banned list first
        for banned in self.registry["banned_or_restricted_registry"]:
            if banned["active_ingredient"] == ingredient_normalized:
                return {
                    "decision": "BLOCKED",
                    "status": "BANNED",
                    "reason": f"Active ingredient '{active_ingredient}' is strictly BANNED/RESTRICTED by CIB&RC: {banned['legal_basis']}"
                }
        
        # 2. Check registered approved list
        for approved in self.registry["registered_approved_registry"]:
            if approved["active_ingredient"] == ingredient_normalized:
                if crop.upper() in approved["approved_crops"]:
                    return {
                        "decision": "PERMITTED",
                        "status": "APPROVED",
                        "type": approved["type"],
                        "formulation": approved["formulation"]
                    }
                else:
                    return {
                        "decision": "BLOCKED",
                        "status": "OFF_LABEL_USE",
                        "reason": f"Active ingredient '{active_ingredient}' is registered in India, but NOT approved for crop '{crop}'."
                    }
        
        # 3. If unknown in registry
        return {
            "decision": "BLOCKED",
            "status": "UNKNOWN",
            "reason": f"Active ingredient '{active_ingredient}' is not found in the verified CIB&RC registry. Recommendations blocked for farmer safety."
        }

    def test_banned_monocrotophos_is_strictly_blocked(self):
        """Even if an old advisory mentions monocrotophos, the code MUST block it."""
        result = self.check_regulatory_gate("monocrotophos", "GROUNDNUT", "LEAF_MINER")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertEqual(result["status"], "BANNED")
        self.assertIn("BANNED", result["reason"])

    def test_approved_azadirachtin_is_permitted(self):
        result = self.check_regulatory_gate("azadirachtin", "GROUNDNUT", "LEAF_MINER")
        self.assertEqual(result["decision"], "PERMITTED")
        self.assertEqual(result["status"], "APPROVED")

    def test_unknown_chemical_is_strictly_blocked(self):
        result = self.check_regulatory_gate("experimental_compound_99", "GROUNDNUT", "LEAF_MINER")
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertEqual(result["status"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
