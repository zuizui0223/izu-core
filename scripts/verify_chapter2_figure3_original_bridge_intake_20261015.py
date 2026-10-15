"""Re-check all 17 ORIGINAL Figure3-panelA compact source artifacts.

This read-only verifier takes the original GitHub Actions ZIP bytes (17 files)
and original committed source JSON. It recomputes the eight Figure 3 panel A
means from the 16 source endpoint arrays, not from plotted derived means.
It does NOT recover 200-update annual genomes or claim an external DOI.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PIN=ROOT/"docs/deposit/chapter2_figure3_original_bridge_17artifact_intake_20261015.json"
COMMITTED=ROOT/"data/results/model3_ch2_bridge_summary_20260927/summary.json"
CONDITIONS={
    "natural":("far","near"),
    "richness_matched":("matched_far","matched_near"),
    "visitor_pool":("pool_far","pool_near"),
    "large_plants":("large_far","large_near"),
}
KINDS=("individual","density")
SOURCE_SNAPSHOTS=20


def digest(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def read_config()->dict:
    manifest=json.loads(PIN.read_text(encoding="utf-8"))
    assert manifest["schema"]=="ch2_main_fig3_panelA_original_endpoints_17artifact_sha256_intake_v1"
    assert manifest["source_original_run"]==36311030639
    assert manifest["status"]=="INDEPENDENT_ACTUAL_OUTER_ZIP_BYTES_SHA256_CRC_17_OF_17_AND_EIGHT_MEANS_MATCH"
    assert manifest["case_total"]==24576
    assert manifest["independent_visitor_histories"]==128
    assert manifest["within_history_initial_starts"]==3
    assert manifest["within_history_nested_demographic_repeats"]==8
    assert manifest["code_snapshot_member_count"]==SOURCE_SNAPSHOTS
    assert manifest["full_raw_annual_trajectories_in_original_shards"] is False
    assert manifest["no_new_biological_runs"] is True
    assert len(manifest["shards"])==16
    for index,part in enumerate(manifest["shards"]):
        assert part["shard"]==index
        assert part["expected_own_cases"]==1536
        assert part["expected_history_seeds"]==[74001+index+16*i for i in range(8)]
        assert len(part["github_outer_sha256"])==64
        assert part["outer_bytes"]>0
    assert len(manifest["summary_artifact"]["github_outer_sha256"])==64
    return manifest


def source_bytes(*, source_dir:Path|None=None, bundle:Path|None=None):
    if (source_dir is None)==(bundle is None):
        raise ValueError("Exactly one of --source-dir or --bundle is required")
    if bundle is not None:
        with zipfile.ZipFile(bundle,"r") as z:
            if z.testzip() is not None:
                raise AssertionError("user-supplied archive CRC failure")
            expected={f"original_actions_artifacts/model3_ch2_bridge_original_shard{i}.zip"
                      for i in range(16)}
            expected.add("original_actions_artifacts/model3_ch2_bridge_original_summary.zip")
            actual=set(z.namelist())
            if not expected<=actual or len(actual)>18:
                raise AssertionError("bundle original source entries incomplete")
            return {p.split("/")[-1]:z.read(p) for p in expected}
    result={}
    for i in range(16):
        name=f"model3_ch2_bridge_original_shard{i}.zip"
        result[name]=(source_dir/name).read_bytes()
    name="model3_ch2_bridge_original_summary.zip"
    result[name]=(source_dir/name).read_bytes()
    return result


def verify(originals:dict)->dict:
    pinned=read_config()
    summary=pinned["summary_artifact"]
    name="model3_ch2_bridge_original_summary.zip"
    data=originals[name]
    if len(data)!=summary["outer_bytes"] or digest(data)!=summary["github_outer_sha256"]:
        raise AssertionError("source summary original outer archive identity mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if z.testzip() is not None:
            raise AssertionError("original summary archive CRC failure")
        if "model3_ch2_bridge_prospective_summary_20260927.json" not in z.namelist():
            raise AssertionError("historical compact final report missing")
    source_provenance={}
    raw_history={}
    checksum=[]
    for entry in pinned["shards"]:
        i=entry["shard"]
        original=originals[f"model3_ch2_bridge_original_shard{i}.zip"]
        if (len(original)!=entry["outer_bytes"]
                or digest(original)!=entry["github_outer_sha256"]):
            raise AssertionError(f"shard{i} original ZIP SHA mismatch")
        with zipfile.ZipFile(io.BytesIO(original)) as z:
            if z.testzip() is not None:
                raise AssertionError(f"shard{i} archive CRC failure")
            expected={f"{v}-{i:02d}.json" for v in
                       ("attempts","campaign-status","derived-design","runtime","shard")}
            expected.add(f"sources-{i:02d}.zip")
            if set(z.namelist())!=expected:
                raise AssertionError(f"shard{i} original member list mismatch")
            state=json.loads(z.read(f"campaign-status-{i:02d}.json"))
            result=json.loads(z.read(f"shard-{i:02d}.json"))
            if (state["complete"] is not True or state["completed"]!=1536
                    or state["executed"]!=1536 or state["expected"]!=1536
                    or result["cases_verified"]!=1536
                    or result["history_seeds"]!=entry["expected_history_seeds"]
                    or result["derived_manifest_hash"]!=state["manifest_hash"]
                    or result["claim_boundary"]!=pinned["original_shard_scope_string"]):
                raise AssertionError(f"shard{i} original execution/absence claim mismatch")
            snapshot=z.read(f"sources-{i:02d}.zip")
            with zipfile.ZipFile(io.BytesIO(snapshot)) as nested:
                if nested.testzip() is not None or len(nested.namelist())!=SOURCE_SNAPSHOTS:
                    raise AssertionError("frozen source snapshot missing or corrupt")
                these={p:digest(nested.read(p)) for p in nested.namelist()}
                if source_provenance and source_provenance!=these:
                    raise AssertionError("original source code changed across shards")
                source_provenance=these
            for h,seed in enumerate(result["history_seeds"]):
                if seed in raw_history:
                    raise AssertionError("duplicate visitor history, not new inference unit")
                raw_history[seed]={}
                for arm,raw_matrix in result["values"].items():
                    values=np.asarray(raw_matrix,dtype=float)
                    if values.shape!=(3,8,8) or not np.isfinite(values).all():
                        raise AssertionError("original endpoint dimensionality/nan drift")
                    raw_history[seed][arm]=values[:,h,:]
            checksum.append({"shard":i,"artifact_id":entry["artifact_id"],
                             "sha256":digest(original),
                             "n_original_cases":result["cases_verified"],
                             "history_seeds":result["history_seeds"]})
    if sorted(raw_history)!=list(range(74001,74129)):
        raise AssertionError("exact 128 independent history seed coverage changed")
    if len(source_provenance)!=SOURCE_SNAPSHOTS:
        raise AssertionError("missing source scripts for original scientific operator")
    if sum(v["n_original_cases"] for v in checksum)!=pinned["case_total"]:
        raise AssertionError("24,576 original endpoint-case counts changed")
    src=json.loads(COMMITTED.read_text(encoding="utf-8"))
    if src["status"]!="complete_audited_summary":
        raise AssertionError("main committed source summary no longer admitted")
    expected=src["campaigns"]["main"]["pairs"]
    rows={}
    for contrast,(far,near) in CONDITIONS.items():
        rows[contrast]={}
        for kind in KINDS:
            means=[]
            for seed in sorted(raw_history):
                a=raw_history[seed][far+"|"+kind]
                b=raw_history[seed][near+"|"+kind]
                if a.shape!=(3,8) or b.shape!=(3,8):
                    raise AssertionError("one-to-one original visitor/demographic pairing violated")
                means.append(float((a-b).mean()))
            recalculated=float(np.mean(means))
            figure_value=pinned["means"][contrast][kind]
            source_value=expected[contrast][kind]["mean"]
            if not (abs(recalculated-source_value)<1e-13
                    and abs(recalculated-figure_value)<1e-13
                    and expected[contrast][kind]["n_histories"]==128):
                raise AssertionError("Figure3 source endpoint mean differs from actual source")
            rows[contrast][kind]={"recalculated_mean":recalculated,
                                  "committed_summary_mean":source_value,
                                  "difference":recalculated-source_value,
                                  "independent_history_units":128}
    return {
        "status":"ORIGINAL_17_ACTIONS_OUTER_SHA256_AND_CRC_CHECKED_8_PANEL_A_MEANS_EXACT",
        "source_run_id":36311030639,
        "source_artifact_count":17,
        "source_original_cases_verified":24576,
        "original_environment_history_clusters":128,
        "source_code_members_verified":len(source_provenance),
        "all_source_member_bytes_equal_across_16_shards":True,
        "panel_a_eight_source_means":rows,
        "source_shards":checksum,
        "full_annual_genetic_trajectories_admitted":False,
        "original_experiment_caveat":pinned["original_shard_scope_string"],
        "no_new_biological_updates":True,
        "external_deposit_or_doi_created":False,
        "scope":"Original compact source endpoint and snapshot evidence, NOT full native trajectories; separate one-locus and original-mutation studies NOT included."
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-dir",type=Path)
    group.add_argument("--bundle",type=Path)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()
    report=verify(source_bytes(source_dir=args.source_dir,bundle=args.bundle))
    if args.out:
        if args.out.exists():
            raise FileExistsError("never overwrite an original-science verification report")
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in
          ("status","source_artifact_count","source_original_cases_verified",
           "original_environment_history_clusters","full_annual_genetic_trajectories_admitted")},
          indent=2))


if __name__=="__main__":
    main()
