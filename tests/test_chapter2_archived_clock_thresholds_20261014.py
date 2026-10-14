"""Pure array-contract tests; NO biological simulation and no new pilot paths."""
import unittest

import numpy as np

from scripts.audit_chapter2_archived_clock_thresholds_20261014 import (
    CLASSES, THRESHOLDS, original_clock, summarize,
)


class TestArchivedQ2Thresholds(unittest.TestCase):
    @staticmethod
    def make_arrays():
        census = np.full(201, 48, dtype=np.int64)
        means = np.zeros((201, 3), dtype=np.float64)
        means[5:,2] = 0.07    # A first reaches 0.05 at t5, not 0.075.
        means[12:,1] = -0.06  # I first reaches 0.05 at t12.
        return means, census

    def test_thresholds_and_six_class(self):
        means, census = self.make_arrays()
        self.assertEqual(original_clock(means,census,0.05),
                         {"A":5,"I":12,"category":"assurance_first"})
        self.assertEqual(original_clock(means,census,0.075)["A"],None)
        self.assertEqual(original_clock(means,census,0.1)["category"],"neither")
        self.assertEqual(original_clock(means,census,0.025)["category"],"assurance_first")
        means[10:,1] = -0.06
        self.assertEqual(original_clock(means,census,0.05)["category"],"near_simultaneous")
        self.assertEqual(len(THRESHOLDS), 4)
        self.assertEqual(len(CLASSES), 6)

    def test_20_consecutive_required_and_right_censor(self):
        means,census = self.make_arrays()
        means[5:24,2] = 0.08
        means[24:,2] = 0.0
        self.assertIsNone(original_clock(means,census,0.05)["A"])
        means[:,2] = 0
        means[181:,2] = 0.07
        self.assertEqual(original_clock(means,census,0.05)["A"],181)
        means[:,2] = 0
        means[182:,2] = 0.07
        self.assertIsNone(original_clock(means,census,0.05)["A"])

    def test_fail_closed_bad_population_and_extinction(self):
        means,census = self.make_arrays()
        census[20:] = 0
        means[20:] = np.nan
        self.assertIsNone(original_clock(means,census,0.05)["I"])
        census[100] = 1
        means[100] = 0.0  # isolate the return-after-extinction contract from NaN validation
        with self.assertRaisesRegex(ValueError,"recolonize"):
            original_clock(means,census,0.05)
        means,census = self.make_arrays()
        census[0] = 47
        with self.assertRaisesRegex(ValueError,"occupied population"):
            original_clock(means,census,0.05)

    def test_unregistered_threshold_is_rejected(self):
        means,census = self.make_arrays()
        with self.assertRaises(ValueError):
            original_clock(means,census,0.20)

    def test_missing_raw_history_fails(self):
        with self.assertRaisesRegex(ValueError,"All 1,536"):
            summarize([],{})


if __name__=="__main__":
    unittest.main()
