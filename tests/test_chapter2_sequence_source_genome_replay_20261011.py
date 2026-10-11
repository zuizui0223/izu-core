"""Frozen Model3 genomic replay: exact annual source and selection return guards."""
import hashlib
import io
import json
import sys
from pathlib import Path
import numpy as np
import pytest

from scripts.audit_chapter2_sequence_source_genome_replay_20261011 import (
    STATUS, replay, original_exposure as replay_exposure, archived_case_path, focal_indices, one_individual_full_W_gradient,
    full_parental_W, price_shift_if_recruited, verify_original_receipt,
)
from scripts.run_model3_persistent_isolation import (
    config,exposure
)
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream,STREAM_IDS


def independent_original_prefix(seed=76001,rep=7101,arm="far",setting="assurance_cost",steps=14):
    """Uninstrumented original runner logic as an identity oracle."""
    cfg=config(setting,.01)
    history=exposure(seed,arm)
    state=founders_from_spec(
        dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),
        74001
    )
    master=int(np.random.SeedSequence([seed,rep]).generate_state(1)[0])
    streams={name:stream(master,name,0) for name in STREAM_IDS}
    data=np.full((steps+1,10),np.nan)
    for t in range(steps+1):
        data[t,0]=len(state.ids)
        if len(state.ids):
            phenotypes=state.alleles.mean(axis=2)
            data[t,1:4]=phenotypes.mean(axis=0)
            data[t,4:7]=phenotypes.var(axis=0)
            data[t,7:]=[len(np.unique(state.alleles[:,k])) for k in range(3)]
        if t==steps:break
        state,_=advance(state,reproduce(state,history.visitors[t],cfg),
            history.seed_candidates[t],cfg,streams,year=t)
    return data


@pytest.mark.parametrize("arm",("near","far"))
def test_source_replay_matches_exact_uninstrumented_original_transition(arm):
    r=replay("assurance_cost",76001,7101,arm,years=14,
             gradient_until=2,sample_n=4)
    np.testing.assert_array_equal(
        np.asarray(r["trace"]),
        independent_original_prefix(arm=arm),
    )
    assert r["status"]==STATUS
    assert r["years_replayed"]==14
    assert r["gradient_window_recorded_0_to"]==2
    assert len(r["annual_pre_mutation_expected_genetic_changes"])==14
    assert len(r["sampled_local_focal_selection"])==3
    assert r["verification"]["verified_against_exact_original_archive"] is False
    assert r["verification"]["supplied_case_record_verified"] is False
    assert r["verification"]["replay_matches_supplied_prefix"] is False
    assert r["verification"]["full_supplied_record_reproduced"] is False
    assert r["verification"]["compared_censuses"] == 0
    assert r["verification"]["compared_checkpoint_years"] == []
    for key in ("historical_source_identity_verified","runtime_identity_verified",
                "original_annual_genomes_verified","original_discovery_full_replay_completed"):
        assert r["verification"][key] is False
    assert r["trace"][0][0]==48
    assert np.isfinite(np.asarray(r["trace"])[:,0]).all()
    assert len(r["source_trace_sha256"])==64
    for event in r["sampled_local_focal_selection"]:
        for name in ("investment","assurance"):
            signal=event["local_focal_gradient"][name]
            assert 0<=signal["evaluated_adults"]<=4
            assert (signal["central_difference_available"]+
                    signal["unavailable_boundary_adults"]==
                    signal["evaluated_adults"])
            assert signal["sampled_positive"]+signal["sampled_negative"]+signal["sampled_near_zero"]==signal["central_difference_available"]


def test_original_gendered_payoff_and_price_expectation_on_full_founder_genomes():
    state=founders_from_spec(
        dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),74001)
    cfg=config("assurance_cost",.01)
    visitors=exposure(76001,"far").visitors[0]
    ledger=reproduce(state,visitors,cfg)
    full=full_parental_W(ledger)
    W=np.asarray(full)
    assert len(W)==48 and np.all(W>0)
    assert W.sum()==pytest.approx(ledger.outcross.sum()+ledger.self_viable.sum(),abs=1e-10)
    result=price_shift_if_recruited(state,ledger)
    genes=state.alleles.mean(axis=2)
    manual=(genes.T@W)/W.sum()-genes.mean(axis=0)
    assert result["mean_assurance_shift_pre_mutation"]==pytest.approx(manual[2],abs=1e-12)
    assert result["mean_investment_shift_pre_mutation"]==pytest.approx(manual[1],abs=1e-12)
    available=focal_indices(state,1,8)
    assert len(available)==8 and len(set(available))==8
    for trait in (1,2):
        sampled=[one_individual_full_W_gradient(state,visitors,cfg,int(i),trait)
                 for i in available]
        assert all(x is None or np.isfinite(x) for x in sampled)
        assert any(x is not None for x in sampled)


def test_source_history_initial_conditions_and_unmodified_rng_stream_identity():
    # The same original source-history seed generates the IDENTICAL initial
    # visitor community before the near/far replenishment trajectories diverge.
    h_near=exposure(76002,"near")
    h_far=exposure(76002,"far")
    for field in ("ids","optima","breadths","effectiveness"):
        np.testing.assert_array_equal(getattr(h_near.visitors[0],field),
                                      getattr(h_far.visitors[0],field))
    # Plant seed-arrival stream and diploid source population histories are
    # paired under both arms; only visitor replenishment distance differs.
    for t in range(9):
        np.testing.assert_array_equal(h_near.seed_candidates[t].ids,
                                      h_far.seed_candidates[t].ids)
        np.testing.assert_array_equal(h_near.seed_candidates[t].alleles,
                                      h_far.seed_candidates[t].alleles)
    near=replay("prior_selfing",76002,7102,"near",years=9,
                gradient_until=0,sample_n=3)
    far=replay("prior_selfing",76002,7102,"far",years=9,
               gradient_until=0,sample_n=3)
    assert near["trace"][0]==far["trace"][0]
    assert near["annual_pre_mutation_expected_genetic_changes"][0][
        "n_visitor_types"]==far["annual_pre_mutation_expected_genetic_changes"][0]["n_visitor_types"]==4
    assert near["annual_pre_mutation_expected_genetic_changes"][0]["mean_investment_shift_pre_mutation"]==pytest.approx(
        far["annual_pre_mutation_expected_genetic_changes"][0]["mean_investment_shift_pre_mutation"],abs=1e-12)
    assert near["genome_checkpoint_sha256"]["0"]==far["genome_checkpoint_sha256"]["0"]


def test_original_npz_required_to_claim_archival_verification(tmp_path):
    r=replay("assurance_cost",76001,7101,"far",years=2,
             gradient_until=0,sample_n=2)
    assert r["verification"]["verified_against_exact_original_archive"] is False
    with pytest.raises(FileNotFoundError):
        replay("assurance_cost",76001,7101,"far",years=2,
               gradient_until=0,sample_n=2,archive_root=tmp_path)
    with pytest.raises(ValueError):
        replay("assurance_cost",76001,7101,"far",years=1001)
    with pytest.raises(ValueError):
        replay("assurance_cost",76000,7101,"far",years=2)
    with pytest.raises(ValueError):
        replay("assurance_cost",76001,7100,"far",years=2)
    with pytest.raises(ValueError):
        replay("delayed_control",76001,7101,"far",years=2)


@pytest.fixture
def synthetic_original_archive(tmp_path):
    """Synthetic temp evidence only; no historical biological trajectory is run."""
    def make(arm):
        setting,seed,rep = "assurance_cost",76001,7101
        folder = ("model3_persistent_isolation_20261005" if arm == "far"
                  else "model3_full_mutation_20261004")
        prefix = "persistent_core" if arm == "far" else "core"
        basename = f"{prefix}_{setting}_u0.01_h{seed}_r{rep}_{arm}"
        directory = tmp_path/folder
        directory.mkdir()
        archive = directory/(basename+".npz")
        receipt_path = directory/(basename+".json")
        trace = np.zeros((1001,10),dtype=float)
        trace[:,0] = 48
        trace[:,1:4] = np.column_stack((np.full(1001,.5),
            np.linspace(.5,.4,1001),np.linspace(.5,.6,1001)))
        trace[:,4:7] = .025
        trace[:,7:] = 96
        checkpoints = {t:np.full((48,3,2),.25+t/4000)
                       for t in (0,200,400,1000)}
        arrays = {"trace":trace,**{f"state_{t}":v for t,v in checkpoints.items()}}
        np.savez_compressed(archive,**arrays)
        receipt = {"task":["abm",setting,.01,seed,rep,arm,0,"jump",False],
                   "sha256":hashlib.sha256(archive.read_bytes()).hexdigest()}
        receipt_path.write_text(json.dumps(receipt),encoding="utf-8")
        return dict(root=tmp_path,setting=setting,seed=seed,rep=rep,arm=arm,
                    archive=archive,receipt_path=receipt_path,receipt=receipt,
                    trace=trace,checkpoints=checkpoints,arrays=arrays,basename=basename)
    return make


@pytest.mark.parametrize("arm",("near","far"))
def test_verify_realistic_original_basename_preserves_decimal_mutation_rate(synthetic_original_archive,arm):
    fixture = synthetic_original_archive(arm)
    base = archived_case_path(fixture["root"],fixture["setting"],fixture["seed"],fixture["rep"],arm)
    assert base.name == fixture["basename"]
    assert fixture["archive"].name == base.name+".npz"
    result = verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],fixture["rep"],arm,
                                     fixture["trace"],fixture["checkpoints"])
    assert result["original_npz_sha256"] == fixture["receipt"]["sha256"]
    assert result["verified_against_exact_original_archive"] is False
    assert result["supplied_case_record_verified"] is True
    assert result["replay_matches_supplied_prefix"] is True
    assert result["full_supplied_record_reproduced"] is True
    assert result["compared_censuses"] == 1001
    assert result["compared_updates"] == 1000
    assert result["compared_checkpoint_years"] == [0,200,400,1000]
    for key in ("historical_source_identity_verified","runtime_identity_verified",
                "original_annual_genomes_verified","original_discovery_full_replay_completed"):
        assert result[key] is False


@pytest.mark.parametrize("censuses",(2,200,201,400,401,1001))
def test_supplied_record_agreement_reports_exact_prefix_extent(synthetic_original_archive,censuses):
    fixture=synthetic_original_archive("far")
    checkpoints={t:v for t,v in fixture["checkpoints"].items() if t<censuses}
    result=verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
        fixture["rep"],"far",fixture["trace"][:censuses],checkpoints)
    assert result["supplied_case_record_verified"] is True
    assert result["replay_matches_supplied_prefix"] is True
    assert result["compared_censuses"] == censuses
    assert result["compared_updates"] == censuses-1
    assert result["compared_checkpoint_years"] == sorted(checkpoints)
    assert result["full_supplied_record_reproduced"] is (censuses==1001)
    assert result["verified_against_exact_original_archive"] is False
    assert result["historical_source_identity_verified"] is False
    assert result["runtime_identity_verified"] is False
    assert result["original_annual_genomes_verified"] is False
    assert result["original_discovery_full_replay_completed"] is False


@pytest.mark.parametrize("shape",((0,10),(1,10),(1002,10),(2,9),(10,)))
def test_supplied_comparison_requires_a_valid_nonempty_replay_extent(synthetic_original_archive,shape):
    fixture=synthetic_original_archive("far")
    trace=np.zeros(shape)
    if shape in ((0,10),(1,10)):
        trace=fixture["trace"][:shape[0]]
    with pytest.raises(ValueError,match="2 to 1001 censuses.*10 columns"):
        verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
            fixture["rep"],"far",trace,{})


@pytest.mark.parametrize("censuses,missing",((2,0),(201,200),(401,400),(1001,1000)))
def test_supplied_comparison_requires_every_reached_checkpoint(synthetic_original_archive,censuses,missing):
    fixture=synthetic_original_archive("far")
    checkpoints={t:v for t,v in fixture["checkpoints"].items() if t<censuses and t!=missing}
    with pytest.raises(ValueError,match="checkpoint years must equal"):
        verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
            fixture["rep"],"far",fixture["trace"][:censuses],checkpoints)


def test_full_trace_without_any_checkpoints_is_not_a_complete_comparison(synthetic_original_archive):
    fixture=synthetic_original_archive("far")
    with pytest.raises(ValueError,match="checkpoint years must equal"):
        verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
            fixture["rep"],"far",fixture["trace"],{})


def test_prefix_cannot_claim_unreplayed_future_checkpoints(synthetic_original_archive):
    fixture=synthetic_original_archive("far")
    with pytest.raises(ValueError,match="checkpoint years must equal"):
        verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
            fixture["rep"],"far",fixture["trace"][:2],fixture["checkpoints"])


def test_source_cli_exposes_supplied_agreement_without_original_authentication(
        synthetic_original_archive,monkeypatch,tmp_path,capsys):
    import scripts.audit_chapter2_sequence_source_genome_replay_20261011 as source_module
    fixture=synthetic_original_archive("far")
    verification=verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
        fixture["rep"],"far",fixture["trace"],fixture["checkpoints"])
    record={"status":STATUS,"setting":fixture["setting"],"seed":fixture["seed"],
            "rep":fixture["rep"],"arm":"far","years_replayed":1000,
            "source_trace_sha256":hashlib.sha256(fixture["trace"].tobytes()).hexdigest(),
            "verification":verification}
    # Only CLI transport is stubbed; the comparison above uses real code/files.
    monkeypatch.setattr(source_module,"replay",lambda *args,**kwargs:record)
    out=tmp_path/"source.json"
    monkeypatch.setattr(sys,"argv",["source","--out",str(out),"--archive-root",str(fixture["root"])])
    source_module.main()
    printed=json.loads(capsys.readouterr().out)
    saved=json.loads(out.read_text())
    assert printed["verification"]["full_supplied_record_reproduced"] is True
    assert printed["verification"]["verified_against_exact_original_archive"] is False
    assert printed["verification"]["runtime_identity_verified"] is False
    assert saved["verification"]==printed["verification"]==verification


def test_compared_arrays_must_come_from_the_bytes_that_passed_the_receipt_hash(
        synthetic_original_archive,monkeypatch):
    fixture=synthetic_original_archive("far")
    replacement_trace=fixture["trace"].copy()
    replacement_trace[1000,2]+=.001
    replacement=io.BytesIO()
    np.savez_compressed(replacement,**{**fixture["arrays"],"trace":replacement_trace})
    replacement_bytes=replacement.getvalue()
    read_bytes=Path.read_bytes
    def replace_after_read(path):
        captured=read_bytes(path)
        if path==fixture["archive"]:
            path.write_bytes(replacement_bytes)
        return captured
    # The file changes after its initial read. A later open must not attach
    # the old receipt hash to different arrays that happen to match the caller.
    monkeypatch.setattr(Path,"read_bytes",replace_after_read)
    with pytest.raises(AssertionError,match="annual source trace differs"):
        verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],
            fixture["rep"],"far",replacement_trace,fixture["checkpoints"])


@pytest.mark.parametrize("arm",("near","far"))
@pytest.mark.parametrize("corruption",("wrong_task","npz_sha","trace","checkpoint","missing_checkpoint"))
def test_original_archive_verifier_fails_closed_on_corrupt_synthetic_evidence(synthetic_original_archive,arm,corruption):
    fixture = synthetic_original_archive(arm)
    if corruption == "wrong_task":
        fixture["receipt"]["task"][3] += 1
        fixture["receipt_path"].write_text(json.dumps(fixture["receipt"]),encoding="utf-8")
        message = "task/seed mismatch"
    elif corruption == "npz_sha":
        # ZIP files remain loadable after trailing bytes; the original byte SHA must fail first.
        with fixture["archive"].open("ab") as handle:
            handle.write(b"synthetic-byte-corruption")
        message = "receipt SHA256 mismatch"
    elif corruption == "trace":
        fixture["trace"] = fixture["trace"].copy()
        fixture["trace"][1000,2] += .001
        message = "annual source trace differs"
    elif corruption == "checkpoint":
        fixture["checkpoints"][400] = fixture["checkpoints"][400].copy()
        fixture["checkpoints"][400][12,1,0] += .001
        message = "t400 source genome differs"
    else:
        fixture["arrays"].pop("state_400")
        np.savez_compressed(fixture["archive"],**fixture["arrays"])
        fixture["receipt"]["sha256"] = hashlib.sha256(fixture["archive"].read_bytes()).hexdigest()
        fixture["receipt_path"].write_text(json.dumps(fixture["receipt"]),encoding="utf-8")
        message = "t400 source genome differs"
    with pytest.raises(AssertionError,match=message):
        verify_original_receipt(fixture["root"],fixture["setting"],fixture["seed"],fixture["rep"],arm,
                                fixture["trace"],fixture["checkpoints"])


def test_original_source_routes_persistent_far_and_reference_near_after_transfer_boundary():
    from scripts.run_model3_full_mutation import exposure as full_mutation_exposure
    # Exercise the history dependency actually bound by the replay module.
    near = replay_exposure(76001,"near")
    persistent_far = replay_exposure(76001,"far")
    transferred_far = full_mutation_exposure(76001,"far")
    original_near = full_mutation_exposure(76001,"near")
    fields = ("ids","optima","breadths","effectiveness")
    for t in (0,199):
        for field in fields:
            np.testing.assert_array_equal(getattr(persistent_far.visitors[t],field),
                                          getattr(transferred_far.visitors[t],field))
    for t in (0,199,200,400,999):
        for field in fields:
            np.testing.assert_array_equal(getattr(near.visitors[t],field),
                                          getattr(original_near.visitors[t],field))
    for t in (200,400,999):
        for field in fields:
            np.testing.assert_array_equal(getattr(transferred_far.visitors[t],field),
                                          getattr(near.visitors[t],field))
        assert any(not np.array_equal(getattr(persistent_far.visitors[t],field),
                                     getattr(near.visitors[t],field)) for field in fields)
        np.testing.assert_array_equal(persistent_far.seed_candidates[t].alleles,
                                      transferred_far.seed_candidates[t].alleles)
