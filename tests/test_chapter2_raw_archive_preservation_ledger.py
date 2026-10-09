"""Source-preservation ledger controls; no new simulations or source writes."""
from pathlib import Path
import json
import re


ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"docs/CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md"
RESULTS=ROOT/"results/chapter2"


def test_three_source_cohorts_stay_separate_with_correct_evidence_rank():
    datasets=[
        ("orthogonal_capacity_full_readout_20261009.json","primary_decision","inconclusive",172032),
        ("kb_independent_full_readout_20261009.json","primary_verdict","inconclusive",229376),
        ("k_fixedB48_independent_primary_20261009.json",
         "primary_verdict","supported_controlled_demographic_K_moderation_at_fixed_B48",114688),
    ]
    for fname,verdict_key,verdict,number in datasets:
        source=json.loads((RESULTS/fname).read_text())
        assert source[verdict_key]==verdict
        assert source["n_independent_visitor_histories"]==64
        assert source["n_t400_sources"]==2048
        count=source.get("n_future_cells",source.get("n_future_trajectories"))
        assert count==number


def test_archive_ledger_is_draft_only_and_records_exact_release_digests():
    s=LEDGER.read_text()
    expected={
        "chapter2-orthogonal-raw-20261009-v1":
            "03e1292511219ea4ee64499d35ac0e5a5f824f1ee0fd420ecd7ca97f4f9ebf65",
        "chapter2-kb-raw-20261009-v1":
            "7d367a9e4a9f4f60f25dbee2ccabc84ef0969f5d9b0096c7df07380314dcfff9",
        "chapter2-fixedB48-raw-20261009-v1":
            "3e522fc9d8da904ed70cc2213bc3b08816761c4e44a4badc72e0c87ba04bd42c",
    }
    for tag,digest in expected.items():
        assert tag in s
        assert re.fullmatch(r"[0-9a-f]{64}",digest)
        assert digest in s
    assert "unpublished" in s.lower()
    assert "not" in s.lower() and "DOI" in s
    assert "retention-days: 90" in s
    assert "Issue #436" in s
    assert "Execution pending confirmation" not in s



def test_fourth_timed_cohort_original_zips_in_unpublished_draft_release():
    from scripts.archive_chapter2_timed_raw_originals import CONFIG
    d=CONFIG["timed"]
    assert d["run_shas"]=={37944527799:"e679e0ee190fa02e0a9d60876cd1a3e9987a4c79"}
    assert d["counts"]=={37944527799:130}
    assert d["futures"]==229376
    assert d["readout_sha256"]=="42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01"
    assert d["verdict"]=="inconclusive"
    assert d["tag"]=="chapter2-timed-self-raw-20261009-v1"

    ledger=LEDGER.read_text()
    assert "chapter2-timed-self-raw-20261009-v1" in ledger
    assert "chapter2-timed-130-original-shard-artifacts.tar" in ledger
    assert "b5ab3a99eeaf36da399290508a64fa022cacc734aa1d794cab3b8443707309aa" in ledger
    assert "ade98a9e3916f8d92b4cdc6b3a724fae811fb0696fdbc4bccf6290f0e51586a6" in ledger
    assert "521 original Actions artifact ZIPs" in ledger
    assert "inconclusive" in ledger.lower()
    assert "unpublished" in ledger.lower()
    assert "external" in ledger.lower() and "DOI" in ledger
