import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import audit_sesgo as m  # noqa: E402


CFG = {
    "repeats": 2,
    "score_field": "final_score",
    "reference_group": "group_a",
    "factor": {
        "path": "education.institution",
        "groups": {"group_a": ["Alpha"], "group_b": ["Beta"]},
    },
    "templates": {
        "strong": {"education": {"institution": "X", "degree": "M.S."}, "skills": ["Python"]},
        "weak": {"education": {"institution": "X", "degree": "B.A."}, "skills": ["Excel"]},
    },
}


class GenerateTests(unittest.TestCase):
    def test_cartesian_size(self):
        rows = m.generate_dataset(CFG)
        # 2 groups × 1 level × 2 tiers × 2 repeats
        self.assertEqual(len(rows), 8)
        inst = {r["education"]["institution"] for r in rows}
        self.assertEqual(inst, {"Alpha", "Beta"})
        self.assertTrue(all(r["candidate_id"].startswith("CAND_") for r in rows))

    def test_only_factor_changes_within_tier(self):
        rows = m.generate_dataset(CFG)
        strong = [r for r in rows if r["_meta_tier"] == "strong"]
        skills = {tuple(r["skills"]) for r in strong}
        self.assertEqual(len(skills), 1)


class AnalyzeTests(unittest.TestCase):
    def test_mean_diff_sign(self):
        results = []
        for i in range(10):
            results.append(
                {
                    "_meta_tier": "strong",
                    "_meta_group": "group_a",
                    "evaluation": {"final_score": 8},
                }
            )
            results.append(
                {
                    "_meta_tier": "strong",
                    "_meta_group": "group_b",
                    "evaluation": {"final_score": 5},
                }
            )
        table = m.analyze(results, "final_score", "group_a")
        row = table[0]
        self.assertEqual(row["comparison"], "group_b - group_a")
        self.assertLess(row["mean_diff"], -2.5)
        self.assertLess(row["p_welch"], 0.01)


if __name__ == "__main__":
    unittest.main()
