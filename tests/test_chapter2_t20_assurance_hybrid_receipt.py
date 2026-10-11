"""Read-only regression on archived assurance-locus mosaic, no new cohorts."""
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_t20_transplant_familywise import familywise_interval


RECEIPT=Path("data/results/chapter2_t20_assurance_locus_hybrid_receipt_20261010.json")


def test_locus_hybrid_replays_original_complete_source_and_shapley_identity():
    d=json.loads(RECEIPT.read_text())
    assert d["source_history_count"]==64
    assert d["t20_both_alive"]==50
    assert d["future_trajectories"]==400
    assert d["new_ecological_visitor_histories_created"]==0
    assert d["cells"]["K8"]=={
        "neutral_all":15,"selected_assurance_only":32,
        "selected_nonassurance_only":18,"selected_all":36}
    assert d["cells"]["K48"]=={
        "neutral_all":41,"selected_assurance_only":48,
        "selected_nonassurance_only":43,"selected_all":49}
    for name,x in d["locus_shapley_descriptive"].items():
        assert np.isclose(
            x["assurance_locus"]+x["matching_and_investment_loci"],
            x["full_three_locus"],rtol=0,atol=1e-12)
        assert np.isclose(
            x["full_three_locus"],
            (d["cells"][name]["selected_all"]
             -d["cells"][name]["neutral_all"])/50,
            rtol=0,atol=1e-12)


def test_familywise_all_10_source_discordances_not_confirmed_as_5pp_effect():
    d=json.loads(RECEIPT.read_text())
    contrasts=d["all_10_paired_secondary"]
    assert len(contrasts)==10
    for x in contrasts:
        ci=familywise_interval(x["positive_only"],x["negative_only"],50,10)
        np.testing.assert_allclose(ci,x["FWER_10_95_approx"],rtol=0,atol=5.1e-5)
        assert ci[0]<=x["original_conservative95"][0]
        assert ci[1]>=x["original_conservative95"][1]
        assert ci[0]<=.05 and ci[1]>=-.05
    assurance_only_K8=next(x for x in contrasts if (
        x["K"]==8 and x["name"]=="assurance_neutral_other"))
    assert assurance_only_K8["delta"]==.34
    assert assurance_only_K8["original_conservative95"][0]>.05
    assert assurance_only_K8["FWER_10_95_approx"][0]<0
    assert d["multiplicity_note"].startswith("Bonferroni across all ten")
