"""Package the ONE active Ecology Letters paper, not the archived 10/06 process draft.

Read-only scientific assets; refuses missing figures, author-identifying source
routing and incomplete source evidence. This is NOT an external DOI deposit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from scripts.render_chapter2_unified_manuscript import ROOT, render_manuscript
from scripts.render_chapter2_capacity_companion_evidence_figure import render_svg

OUT=ROOT/"outputs/chapter2_unified_el_delivery/EL_ONE_PAPER_REVIEW.zip"
PDF_FIGURES={
 "Figure1.pdf":ROOT/"outputs/figures/model3_return_components_20261005/return_components.pdf",
 "Figure2.pdf":ROOT/"outputs/figures/model3_assurance_compression_20261006/assurance_compression.pdf",
 "Figure3.pdf":ROOT/"outputs/figures/model3_trait_pollen_20261005/trait_pollen_snapshot400.pdf",
}
FROZEN_RESULTS={
 "EVOLUTION_DESIGN.json":"data/design/chapter2_assurance_generality_20261006.json",
 "EVOLUTION_RESULTS.json":"data/results/chapter2_assurance_generality_20261006.json",
 "CAPACITY_RESULTS.json":"results/chapter2/k_fixedB48_independent_primary_20261009.json",
}
DENIED=("zuizui0223","github.com/zuizui0223","issue #436","pr #452","pr #455")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blind_paper():
    source=render_manuscript()
    title=source.splitlines()[0]
    manuscript=title+"\n\n## Abstract"+source.split("## Abstract",1)[1]
    if manuscript.count("## Evidence hierarchy and study-origin record") != 1:
        raise ValueError("source study provenance boundary missing")
    before,after=manuscript.split("## Evidence hierarchy and study-origin record",1)
    if "# References" not in after:
        raise ValueError("manuscript references missing")
    manuscript=before+"# References"+after.split("# References",1)[1]
    start=manuscript.index("# Data accessibility")
    end=manuscript.index("# References",start)
    anonymous=(
      "# Data accessibility\n\n"
      "The originally frozen study designs, complete simulation outputs, "
      "source code and SHA-256-authenticated raw data remain preserved. "
      "A permanent DOI-backed raw-data archive has not yet been deposited. "
      "An appropriately anonymous, editor-approved access route is required "
      "before manuscript submission; depositing the underlying raw data "
      "remains an outstanding requirement.\n\n"
    )
    manuscript=manuscript[:start]+anonymous+manuscript[end:]
    # Strip internal repository-local paths, not study descriptions or results.
    manuscript=re.sub(
      r"\[([^\]\n]+)\]\((?:\.\./)?(?:docs/|figures/)[^)]*\)",
      r"\1",manuscript,
    )
    manuscript=re.sub(
      r"(?<!\w)(?:docs|figures|data/design|data/results|scripts)/[A-Za-z0-9_./-]+",
      "[source file in blinded archive]",manuscript,
    )
    if any(x in manuscript.lower() for x in DENIED):
        raise ValueError("identifying internal token remains")
    abstract=manuscript.split("## Abstract",1)[1].split("## Keywords",1)[0]
    body=manuscript.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0]
    if len(abstract.split())>150 or len(body.split())>5000:
        raise ValueError("EL Letter word limits not met")
    for phrase in ("64 independent","inconclusive","+0.007746","pollen-limited"):
        if phrase.lower() not in manuscript.lower():
            raise ValueError("scientific boundary missing in blinded paper: "+phrase)
    return manuscript.strip()+"\n"


def build(out:Path=OUT, *, figures=None):
    out=Path(out)
    figures=PDF_FIGURES if figures is None else figures
    if set(figures)!=set(PDF_FIGURES):
        raise ValueError("single paper requires Figure1–3 PDF")
    manuscript=blind_paper().encode("utf-8")
    si=(ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md").read_bytes()
    if any(token in si.lower().decode("utf-8") for token in DENIED):
        raise ValueError("blinded Supporting Information has identifying token")
    members={
      "MANUSCRIPT.md":manuscript,
      "SUPPORTING_INFORMATION.md":si,
      "Figure4.svg":render_svg().encode("utf-8"),
    }
    for dest,p in figures.items():
        b=Path(p).read_bytes()
        if not b.startswith(b"%PDF-") or len(b)<1000:
            raise ValueError("unrendered or invalid PDF figure "+dest)
        members[dest]=b
    for label,path in FROZEN_RESULTS.items():
        b=(ROOT/path).read_bytes()
        json.loads(b)
        members["EVIDENCE/"+label]=b
    manifest={
        "status":"EL_ONE_PAPER_REVIEW_VERIFIED_NOT_SUBMITTED",
        "source_active_manuscript":"CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md",
        "n_figures":4,"doi_deposit_complete":False,
        "evolution_evidence":"preregistered four-setting",
        "capacity_evidence":"one independent preregistered small K contrast; other cohorts descriptive",
        "members":{name:{"size":len(b),"sha256":sha(b)}
                   for name,b in sorted(members.items())},
    }
    members["MANIFEST.json"]=(json.dumps(manifest,sort_keys=True,indent=2)+"\n").encode("utf-8")
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,b in sorted(members.items()):
            z.writestr(name,b)
    with zipfile.ZipFile(out) as z:
        if sorted(z.namelist())!=sorted(members):
            raise ValueError("missing or duplicated archive member")
        for name,b in members.items():
            if z.read(name)!=b:
                raise ValueError("zip member readback failed: "+name)
    receipt={
        "status":manifest["status"],"zip_sha256":sha(out.read_bytes()),
        "bytes":out.stat().st_size,"members":len(members),
        "manuscript_sha256":sha(manuscript),"n_figures":4,
        "submitted":False,"doi_deposit_complete":False,
    }
    out.with_suffix(".receipt.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=OUT)
    args=parser.parse_args()
    print(json.dumps(build(args.out),indent=2))


if __name__=="__main__":
    main()
