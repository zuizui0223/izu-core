"""Q2 original-pilot retrospective clock audit; no Model3 updates or RNG."""
import json
import unittest
from copy import deepcopy
from scripts.audit_chapter2_genetic_access_paired_clock_20261014 import (
    CLASSES, READOUT, event_class, summarize, verified_rows,
)


class TestQ2PairedClock(unittest.TestCase):
    def test_class_boundaries(self):
        assert event_class(None, None) == "neither"
        assert event_class(4, None) == "assurance_only"
        assert event_class(None, 4) == "investment_only"
        assert event_class(10, 15) == "near_simultaneous"
        assert event_class(10, 16) == "assurance_first"
        assert event_class(16, 10) == "investment_first"

    def test_invalid_pairings_fail_closed(self):
        original = verified_rows()
        with self.assertRaisesRegex(ValueError, "Missing/unmatched"):
            summarize(original[:-1])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            summarize(original + [deepcopy(original[-1])])
        altered = deepcopy(original)
        altered[0]["width"] = "unregistered"
        with self.assertRaisesRegex(ValueError, "Duplicate/invalid"):
            summarize(altered)

    def test_source_bound_full_readout(self):
        actual = summarize(verified_rows())
        frozen = json.loads(READOUT.read_text(encoding="utf-8"))
        self.assertEqual(actual, frozen)
        self.assertEqual(actual["original_case_records"], 1536)
        self.assertEqual(actual["matched_width_pairs"], 768)
        self.assertEqual(actual["distinct_original_founder_genotype_backgrounds"], 2)
        self.assertEqual(actual["nested_paired_founder_history_seed_clusters"], 128)
        self.assertEqual(actual["paired_event_detection"]["A"], {
            "neither": 0, "high_only": 26, "low_only": 0, "both": 742,
        })
        self.assertEqual(actual["paired_event_detection"]["I"], {
            "neither": 173, "high_only": 119, "low_only": 101, "both": 375,
        })
        clock_A = actual["paired_first_sustained_onset_differences"]["A"]
        self.assertEqual(
            (clock_A["n"], clock_A["high_earlier"], clock_A["equal"], clock_A["high_later"]),
            (742, 723, 3, 16),
        )
        self.assertAlmostEqual(clock_A["mean_high_minus_low_updates"], -47.320754716981135, places=12)
        clock_I = actual["paired_first_sustained_onset_differences"]["I"]
        self.assertEqual(clock_I["n"], 375)
        self.assertAlmostEqual(clock_I["mean_high_minus_low_updates"], 0.5173333333333333, places=12)
        # Whole-population fixed-horizon checks retain all 768 paired starts.
        capped = actual["all_start_capped_first_onset"]
        self.assertEqual(capped["A"]["n_all_pairs"], 768)
        self.assertEqual(capped["A"]["cap_for_not_detected_by_181"], 182)
        self.assertAlmostEqual(capped["A"]["mean_high_minus_low_capped_updates"], -51.302083333333336)
        self.assertAlmostEqual(capped["I"]["mean_high_minus_low_capped_updates"], -2.5130208333333335)
        self.assertEqual(capped["A"]["detected_by_start_year_all_768"]["25"], {"L": 134, "H": 701})
        self.assertEqual(capped["I"]["detected_by_start_year_all_768"]["100"], {"L": 468, "H": 476})
        table = actual["paired_transition_counts_rows_low_columns_high"]
        self.assertEqual(table["investment_first"]["assurance_first"], 125)
        self.assertEqual(table["investment_first"]["near_simultaneous"], 124)
        self.assertEqual(table["assurance_first"]["investment_first"], 2)
        self.assertEqual(sum(sum(table[a].values()) for a in CLASSES), 768)
        self.assertAlmostEqual(actual["D_A_first_minus_I_first"]["high_minus_low"], 0.6692708333333334)
        self.assertEqual(len(actual["six_founder_context_strata"]), 6)
        for stratum in actual["six_founder_context_strata"]:
            self.assertEqual(stratum["n_pairs"], 128)
            self.assertGreater(stratum["D_change"], 0.0)


if __name__ == "__main__":
    unittest.main()
