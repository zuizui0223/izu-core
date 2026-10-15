"""Read-only admission of exact, nonexchangeable main Figure 3 source JSONs.

This checks the *committed plotted summaries* and original-source pointers,
not original raw archive bytes or a cross-host Zenodo deposit.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURE = ROOT / "scripts/figure_model3_genetic_realization.py"
BUILDER = ROOT / "scripts/build_chapter2_unified_el_submission_bundle.py"
NOTE = ROOT / "docs/deposit/CHAPTER2_MAIN_FIGURE3_SOURCE_TO_DOI_AUDIT_20261015.md"

SOURCE_BLOBS = {
    "scripts/figure_model3_genetic_realization.py": "3ec839b47cc3a513c0cbf808fdef352b0959ca23",
    "data/results/model3_ch2_bridge_summary_20260927/summary.json": "a0fdb9ccba5c2f9c3e564c3e4a1b205ab8693322",
    "data/results/model3_mutation_memory_20261004.json": "d61a862daf9679c9ccbf3f76ecdac2b2e4b9bfdc",
    "data/results/model3_mutation_variability_20261005.json": "48b0c8730669980192b73163f68ff26e67a18854",
}


def _blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_figure3_sources_are_exact_pinned_three_jsons_not_atom_original_mutation():
    for path, expected in SOURCE_BLOBS.items():
        assert _blob(ROOT / path) == expected, path
    figure = FIGURE.read_text(encoding="utf-8")
    assert figure.count("ROOT/'data/results/model3_ch2_bridge_summary_20260927/summary.json'") == 1
    assert figure.count("ROOT/'data/results/model3_mutation_memory_20261004.json'") == 1
    assert figure.count("ROOT/'data/results/model3_mutation_variability_20261005.json'") == 1
    assert "completed_atom_abm_20261011.zip" not in figure
    reviewer = BUILDER.read_text(encoding="utf-8")
    assert '"Figure3.pdf":ROOT/"outputs/figures/model3_genetic_realization_20261005/genetic_realization.pdf"' in reviewer
    assert '"SupplementaryFigureS1.pdf":ROOT/"outputs/figures/model3_trait_pollen_20261005/trait_pollen_snapshot400.pdf"' in reviewer


def test_panel_a_zero_mutation_bridge_four_conditions_128_history_units():
    bridge = _read("data/results/model3_ch2_bridge_summary_20260927/summary.json")
    assert bridge["status"] == "complete_audited_summary"
    pair = bridge["campaigns"]["main"]["pairs"]
    conditions = ("natural", "richness_matched", "visitor_pool", "large_plants")
    assert set(conditions) == set(pair)
    points = []
    for cond in conditions:
        for kind in ("individual", "density"):
            row = pair[cond][kind]
            assert row["n_histories"] == 128
            lo, hi = row["mean_ci"]
            assert lo <= row["mean"] <= hi
            points.append(row["mean"])
    assert len(points) == 8
    assert pair["natural"]["individual"]["mean"] == -0.1446356879340278
    assert pair["natural"]["density"]["mean"] == -0.45098306258395304
    assert pair["richness_matched"]["individual"]["mean"] == 0.0333226521809896
    assert pair["richness_matched"]["density"]["mean"] == 0.033757340770689925
    assert bridge["campaigns"]["main"]["analysis_contract"]["mean_interval"].startswith("1999 bootstrap")


def test_panels_b_c_distinct_one_locus_eight_conditional_repeats():
    memory = _read("data/results/model3_mutation_memory_20261004.json")
    spread = _read("data/results/model3_mutation_variability_20261005.json")
    assert memory["status"] == "completed_diagnostic_not_attractor_test"
    assert spread["status"] == "raw_archive_verified"
    assert spread["raw_cases"] == 64
    assert len(spread["raw_hashes"]) == 64
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in spread["raw_hashes"].values())
    assert memory["archive_sha256"] == spread["archive_sha256"] == (
        "1bb184ed451f4dec1eadd20562cdc9adb3e3b6f615b94646d024154633b7ad79"
    )
    assert spread["max_difference_from_existing_means"] == 0
    assert spread["bootstrap"]["unit"] == "demographic repeat"
    assert spread["bootstrap"]["resamples"] == 5000
    panels = []
    for capacity in (48, 192):
        for rate in (0, .01):
            states = [r for r in memory["abm"] if (
                r["capacity"] == capacity
                and r["mutation_rate"] == rate
                and r["common_environment_periods"] == 800
            )]
            assert len(states) == 1
            record = states[0]
            assert record["occupied_pairs"] == record["n_pairs"] == 8
            for i, past in enumerate(("present", "absent")):
                for measure, key in (("allele_count", "mean_allele_counts"),
                                     ("last100_change", "last100_mean_change")):
                    matching = [r for r in spread["rows"] if (
                        r["capacity"] == capacity and r["mutation_rate"] == rate
                        and r["past"] == past and r["measure"] == measure
                    )]
                    assert len(matching) == 1
                    one = matching[0]
                    assert one["occupied_repeats"] == len(one["repeats"]) == 8
                    assert abs(one["mean"] - record[key][i]) < 1e-13
                    lo, hi = one["descriptive_bootstrap_95"]
                    assert lo <= one["mean"] <= hi
                    panels.append(one)
    assert len(panels) == len(spread["rows"]) == 16
    # 8 A points + 16 B/C observations, with different source experiments.
    assert 8 + len(panels) == 24


def test_deposit_claim_limit_and_distinct_atom_data_source():
    note = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "SOURCE-MAPPED / NOT FULL NATIVE-RAW ADMITTED / NO EXTERNAL DOI",
        "two original fixed environmental histories",
        "64 raw case SHA-256 strings",
        "NOT a direct source of plotted Figure 3",
        "3/32 and 2/32",
        "not a new biological simulation",
        "do not",
    ):
        assert phrase.lower() in note.lower(), phrase
