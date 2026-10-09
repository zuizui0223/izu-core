"""Full original raw shard artifact ZIPs into private draft Github Releases.

One-time archival procedure ONLY. No biological simulations, no new
statistical analyses, no change to machine verdicts or frozen protocols.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import zipfile

CONFIG={
    "timed":{
        "run_shas":{37944527799:"e679e0ee190fa02e0a9d60876cd1a3e9987a4c79"},
        "counts":{37944527799:130},
        "source_prefix":"chapter2-timed-t400-shard-",
        "future_prefix":"chapter2-timed-future-shard-",
        "summary_names":{
            "chapter2-timed-self-viability-source-admission",
            "chapter2-timed-self-viability-64-history-full-readout",
        },
        "readout_artifact":"chapter2-timed-self-viability-64-history-full-readout",
        "readout_sha256":"42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01",
        "futures":229376,
        "verdict":"inconclusive",
        "tag":"chapter2-timed-self-raw-20261009-v1",
    },
}

def api(path):
    return json.loads(subprocess.run(["gh","api",path],check=True,capture_output=True,text=True).stdout)


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda:file.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()


def verify_manifest_input(study):
    cfg=CONFIG[study]
    artifacts=[]
    for run,sha in cfg["run_shas"].items():
        meta=api(f"repos/zuizui0223/izu-core/actions/runs/{run}")
        if meta["head_sha"]!=sha or meta["conclusion"]!="success":
            raise AssertionError("Original run has changed SHA/status")
        page=1
        while True:
            data=api(f"repos/zuizui0223/izu-core/actions/runs/{run}/artifacts?per_page=100&page={page}")
            if page==1 and data["total_count"]!=cfg["counts"][run]:
                raise AssertionError("Original artifact count changed")
            for a in data["artifacts"]:
                if a["expired"] or a["workflow_run"]["id"]!=run:
                    raise AssertionError("Expired/mismatched original source artifact")
                if not re.fullmatch(r"[A-Za-z0-9_.-]+",a["name"]):
                    raise AssertionError("Invalid unexpected artifact name")
                artifacts.append({
                    "name":a["name"],"id":a["id"],"source_run":run,
                    "github_digest":a.get("digest"),
                    "original_size_bytes":a["size_in_bytes"],
                    "created_at":a["created_at"],"expires_at":a["expires_at"],
                })
            if len(data["artifacts"])<100:
                break
            page+=1
    want=({cfg["source_prefix"]+str(i) for i in range(64)}
          | {cfg["future_prefix"]+str(i) for i in range(64)}
          | cfg["summary_names"])
    if len(artifacts)!=130 or {a["name"] for a in artifacts}!=want:
        raise AssertionError("Not exactly 64 complete original source/future shards + two summaries")
    return sorted(artifacts,key=lambda x:x["name"])


def archive(study,out):
    if not os.getenv("GH_TOKEN"):
        raise PermissionError("No authenticated GitHub access")
    cfg=CONFIG[study]
    artifacts=verify_manifest_input(study)
    files=out/"raw-original-zips"
    files.mkdir(parents=True,exist_ok=True)
    for i,a in enumerate(artifacts,1):
        path=files/(a["name"]+".zip")
        url=f"https://api.github.com/repos/zuizui0223/izu-core/actions/artifacts/{a['id']}/zip"
        if not path.exists():
            subprocess.run([
                "curl","--fail","--silent","--show-error","--location",
                "--retry","4","-H",f"Authorization: Bearer {os.environ['GH_TOKEN']}",
                "-H","Accept: application/vnd.github+json",url,
                "--output",str(path)],check=True)
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:
                raise AssertionError("Original raw ZIP CRC verification failed")
            if a["name"]==cfg["readout_artifact"]:
                members=[n for n in z.namelist() if n.endswith(".json")]
                if len(members)!=1 or hashlib.sha256(z.read(members[0])).hexdigest()!=cfg["readout_sha256"]:
                    raise AssertionError("Original registered result JSON SHA256 changed")
        a["downloaded_zip_bytes"]=path.stat().st_size
        a["downloaded_zip_sha256"]=sha256(path)
        if a["github_digest"] and a["github_digest"]!="sha256:"+a["downloaded_zip_sha256"]:
            raise AssertionError("Original GitHub artifact digest differs")
        if i%16==0:
            print(f"{study}: independently authenticated {i}/{len(artifacts)} original raw ZIPs",flush=True)
    manifest={
        "status":"IMMUTABLE_SOURCE_ORIGINAL_ARTIFACT_PRESERVATION_NO_NEW_SCIENCE",
        "study":study,"release_tag":cfg["tag"],"draft_release":True,
        "original_run_shas":cfg["run_shas"],
        "artifact_count":130,"source_shards":64,"future_shards":64,
        "independent_visitor_histories":64,"complete_diploid_t400_sources":2048,
        "future_trajectories":cfg["futures"],
        "frozen_primary_verdict":cfg["verdict"],
        "original_readout_sha256":cfg["readout_sha256"],
        "individual_original_artifacts":artifacts,
        "warning":"Draft Github Release is not a DOI-bearing externally deposited scientific archive.",
    }
    mpath=out/f"{study}-raw-130-manifest.json"
    mpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    tarpath=out/f"chapter2-{study}-130-original-shard-artifacts.tar"
    with tarfile.open(tarpath,"w") as tar:
        tar.add(mpath,arcname=mpath.name)
        for a in artifacts:
            name=a["name"]+".zip"
            tar.add(files/name,arcname="original-zip-artifacts/"+name)
    receipt={
        "status":"READY_FOR_PRIVATE_DRAFT_RELEASE",
        "study":study,"release_tag":cfg["tag"],
        "archive_bytes":tarpath.stat().st_size,
        "archive_sha256":sha256(tarpath),
        "manifest_sha256":sha256(mpath),
        "members_expected":131,
    }
    (out/f"{study}-archive-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt),flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--study",choices=CONFIG,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--execute-original-draft-archive",action="store_true")
    args=parser.parse_args()
    if not args.execute_original_draft_archive:
        raise PermissionError("Original archive preservation requires explicit execution")
    archive(args.study,args.out)


if __name__=="__main__":
    main()
