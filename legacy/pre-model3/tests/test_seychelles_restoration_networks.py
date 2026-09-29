import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/seychelles_restoration_network_summary.json"


def load():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_empirical_object_and_64_network_scale_are_locked():
    result = load()
    assert result["source_empirical_object"] == {
        "object": "all_dat",
        "rdata_bytes": 3971,
        "rdata_sha256": "2b68cec63be0b87c3604b99bdeb2440adb36e3c25737b4035440d3345f013715",
    }
    assert result["scale"]["network_rows"] == 64
    assert result["scale"]["sites"] == 8
    assert result["scale"]["months"] == 8
    assert result["scale"]["treatment_sites"] == {"Unrestored": 4, "Restored": 4}
    assert set(result["scale"]["site_months_per_site"].values()) == {8}


def test_site_is_the_independent_treatment_unit():
    result = load()
    assert result["treatment_site_level_means"]["Restored"]["n_sites"] == 4
    assert result["treatment_site_level_means"]["Unrestored"]["n_sites"] == 4
    assert "Site is the treatment-level independent unit" in result["analysis_unit_boundary"]
    assert "months are not independent restoration replicates" in result["analysis_unit_boundary"]


def test_restoration_response_is_multichannel_not_uniform():
    delta = load()["restored_minus_unrestored_site_mean"]
    assert delta["network_size"] > 0
    assert delta["nestedness"] > 0
    assert delta["total_visits"] > 0
    assert delta["mean_freq_visit"] < 0


def test_no_dependency_or_independent_archipelago_claim():
    boundary = load()["claim_boundary"]
    assert "do not establish direct plant reproductive dependency" in boundary
    assert "or an additional independent archipelago" in boundary
