import unittest, json, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils import clf, reg


class AnalysisChecks(unittest.TestCase):
    def test_metrics_and_input_invariants(self):
        m = json.loads((ROOT / "results/metrics.json").read_text())
        self.assertGreaterEqual(
            m["weekly_coverage"]["headcount"], max(m["weekly_coverage"]["demand"])
        )
        self.assertTrue(
            all(
                a >= b
                for a, b in zip(
                    m["weekly_coverage"]["coverage"], m["weekly_coverage"]["demand"]
                )
            )
        )
        self.assertEqual(m["weekly_coverage"]["mip_gap"], 0)

    def test_metric_semantics(self):
        m = clf([0, 0, 1, 1], [0, 1, 1, 0], [0.1, 0.8, 0.9, 0.2])
        self.assertEqual(m["recall"], 0.5)
        self.assertEqual(m["confusion"], [[1, 1], [1, 1]])
        self.assertEqual(reg([1, 2, 3], [1, 2, 3])["rmse"], 0)


if __name__ == "__main__":
    unittest.main()
