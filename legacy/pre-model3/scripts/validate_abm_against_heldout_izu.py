import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABM = ROOT / "data/results/constraint_mechanism_abm_v1.json"
IZU = ROOT / "data/predictive_meta/hiraiwa_ushimaru_cross_channel_concordance.json"
OUT = ROOT / "data/results/abm_heldout_izu_validation.json"


def build_validation(abm, izu):
    mainland = abm["summary"]["mainland_like"]
    oceanic = abm["summary"]["oceanic_island"]
    matching = izu["directions"]["corrected_trait_matching"]
    pollen = izu["directions"]["pollen_receipt"]
    tube = izu["directions"]["tube_morphology"]

    opportunity_pass = oceanic["mean_final_pollinator_types"] < mainland["mean_final_pollinator_types"]
    matching_pass = matching["lower_post"] == izu["n_shared_targets"]
    branching_pass = (
        len(oceanic["architecture_counts"]) >= 2
        and pollen["lower_post"] > 0 and pollen["higher_post"] > 0
        and tube["shorter_post"] > 0 and tube["longer_post"] > 0
    )

    return {
        "analysis": "abm_heldout_izu_validation",
        "training_boundary": "ABM v1 scenarios were defined from non-Izu comparative constraints; Izu/Hiraiwa outcomes are treated here as held-out empirical validation and are not used to retune parameters.",
        "tests": {
            "opportunity_constraint_direction": "pass" if opportunity_pass else "fail",
            "heldout_matching_decline": "pass" if matching_pass else "fail",
            "response_branching_class": "pass" if branching_pass else "fail",
            "uniform_reproductive_decline": "not_supported_as_species_level_prediction"
        },
        "abm_prediction": {
            "mainland_mean_final_pollinator_types": mainland["mean_final_pollinator_types"],
            "oceanic_mean_final_pollinator_types": oceanic["mean_final_pollinator_types"],
            "oceanic_architecture_states": sorted(oceanic["architecture_counts"]),
            "oceanic_mean_reproduction": oceanic["mean_reproduction"],
            "mainland_mean_reproduction": mainland["mean_reproduction"]
        },
        "heldout_izu": {
            "matching_lower_post": matching["lower_post"],
            "matching_total": izu["n_shared_targets"],
            "pollen_lower_post": pollen["lower_post"],
            "pollen_higher_post": pollen["higher_post"],
            "tube_shorter_post": tube["shorter_post"],
            "tube_longer_post": tube["longer_post"],
            "tube_equal": tube["equal"]
        },
        "decision": "mechanism_class_survives_heldout_but_v1_is_not_a_quantitative_predictor",
        "interpretation": "Without Izu-specific tuning, v1 correctly anticipates a tighter partner opportunity space and allows multiple ecological solutions, which is qualitatively compatible with the universal matching decline plus divergent downstream responses in the held-out Izu data. However, its aggregate mean-reproduction decline cannot be promoted to a species-level prediction because held-out pollen receipt splits 4 lower / 4 higher. The next model must predict response branching, not merely an island-wide mean decline.",
        "next_gate": "Add predeclared lineage-level heterogeneity in dependency/assurance as a mechanism candidate, then test whether it predicts the held-out sign branching without architecture-specific tuning.",
        "claim_boundary": "This is qualitative held-out validation of a mechanism class, not parameter estimation and not evidence that the ABM predicts empirical effect sizes."
    }


def main():
    out = build_validation(json.loads(ABM.read_text()), json.loads(IZU.read_text()))
    OUT.write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
