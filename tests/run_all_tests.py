import unittest
import sys
import os

def run_suite():
    print("=" * 80)
    print("AGRICULTURAL INTELLIGENCE PLATFORM — AUTOMATED SYSTEM TEST SUITE")
    print("Pilot Geography: India -> Karnataka -> Chitradurga -> Molakalmuru -> Hosanagalapura")
    print("Testing Framework: Deterministic Rule Validation & Evidence Tracing")
    print("=" * 80)

    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 80)
    if result.wasSuccessful():
        print(f"ALL TESTS PASSED ({result.testsRun} executed)")
        print("Verdict: Deterministic safety boundaries, evidence provenance, and failure handling verified.")
        return 0
    else:
        print(f"TEST FAILURES DETECTED: {len(result.failures)} failures, {len(result.errors)} errors")
        return 1

if __name__ == "__main__":
    sys.exit(run_suite())
