from channel_id.roi_dual_control import (
    PROPOSALS,
    calibrate_technical_positive,
    combine_control_gates,
)
from channel_id.roi_visual_core import COMPONENTS


def _technical_rows():
    rows = []
    for proposal in PROPOSALS:
        for index in range(6):
            for variant, base in (("original", 1.0), ("attenuated", 0.1)):
                row = {
                    "pair_id": f"card-{index}::{proposal}",
                    "card_id": f"card-{index}",
                    "taxon": f"Ajania::{proposal}::technical_positive",
                    "proposal": proposal,
                    "control_variant": variant,
                    "feature_status": "ok",
                }
                for component_index, component in enumerate(COMPONENTS):
                    row[component] = base + index * 0.01 + component_index * 0.001
                rows.append(row)
    return rows


def test_technical_positive_control_detects_known_attenuation():
    results = calibrate_technical_positive(_technical_rows())
    assert len(results) == len(PROPOSALS)
    assert all(row["paired_cards"] == 6 for row in results)
    assert all(row["median_attenuated_minus_original"] < -0.5 for row in results)
    assert all(row["negative_pair_fraction"] == 1.0 for row in results)
    assert all(row["passes_technical_positive_control"] == "yes" for row in results)


def test_dual_technical_pass_does_not_release_biological_holdout():
    negative = [
        {"proposal": proposal, "passes_flat_negative_control": "yes"}
        for proposal in PROPOSALS
    ]
    positive = [
        {"proposal": proposal, "passes_technical_positive_control": "yes"}
        for proposal in PROPOSALS
    ]
    gates = combine_control_gates(negative, positive)
    assert all(row["passes_dual_technical_gate"] == "yes" for row in gates)
    assert all(row["biological_positive_control_status"] == "missing" for row in gates)
    assert all(row["eligible_for_broad_specialist_holdout"] == "no" for row in gates)
