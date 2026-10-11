"""Package the ONE active Ecology Letters paper, not the archived 10/06 process draft.

Read-only scientific assets; refuses missing figures, author-identifying source
routing and incomplete source evidence. This is NOT an external DOI deposit.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from pypdf import PdfReader

from scripts.render_chapter2_unified_manuscript import ROOT, render_manuscript
from scripts.render_chapter2_capacity_companion_evidence_figure import render_svg

OUT=ROOT/"outputs/chapter2_unified_el_delivery/EL_ONE_PAPER_REVIEW.zip"
PDF_FIGURES={
 "Figure1.pdf":ROOT/"outputs/figures/model3_return_components_20261005/return_components.pdf",
 "Figure2.pdf":ROOT/"outputs/figures/model3_assurance_compression_20261006/assurance_compression.pdf",
 "Figure3.pdf":ROOT/"outputs/figures/model3_trait_pollen_20261005/trait_pollen_snapshot400.pdf",
}
SUPPLEMENTARY_FIGURES={
 "SupplementaryFigureS1.pdf":ROOT/"outputs/figures/model3_genetic_realization_20261005/genetic_realization.pdf",
 "SupplementaryFigureS2.svg":ROOT/"figures/chapter2_functional_loss_tempo_20261011/crossing_by100.svg",
}
FROZEN_RESULTS={
 "EVOLUTION_DESIGN.json":"data/design/chapter2_assurance_generality_20261006.json",
 "EVOLUTION_RESULTS.json":"data/results/chapter2_assurance_generality_20261006.json",
 "CAPACITY_RESULTS.json":"results/chapter2/k_fixedB48_independent_primary_20261009.json",
}
TEMPO_ADMISSION=ROOT/"data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json"
TEMPO_TABLES=ROOT/"docs/CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FULL_TABLES_20261011.md"
TEMPO_DESIGN=ROOT/"data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json"
DENIED=("zuizui0223","github.com/","/workspace/","/home/","/root/",
        "issue #436","pr #452","pr #455")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value,sort_keys=True,indent=2)+"\n").encode("utf-8")


def anonymous_text(text,label):
    if any(token in text.lower() for token in DENIED):
        raise ValueError("identifying internal token remains in "+label)


def validate_member(name,raw):
    """Parse deliverable formats; visual and scientific inspection remain separate."""
    if name.endswith(".pdf"):
        try:
            if not raw.startswith(b"%PDF-"):
                raise ValueError("PDF header missing")
            pdf=PdfReader(io.BytesIO(raw),strict=True)
            if pdf.is_encrypted or len(pdf.pages)!=1:
                raise ValueError("figure must be one unencrypted PDF page")
            anonymous_text(str(pdf.metadata)+"\n"+(pdf.pages[0].extract_text() or ""),name)
        except Exception as exc:
            raise ValueError("unrendered or invalid PDF figure "+name) from exc
        return
    text=(gzip.decompress(raw) if name.endswith(".gz") else raw).decode("utf-8")
    if name.endswith((".json",".json.gz")):
        json.loads(text)
    elif name.endswith(".svg"):
        if ElementTree.fromstring(text).tag!="{http://www.w3.org/2000/svg}svg":
            raise ValueError("invalid SVG figure "+name)
    anonymous_text(text,name)


def checked_gzip(record):
    raw=(ROOT/record["path"]).read_bytes()
    if sha(raw)!=record["gzip_sha256"]:
        raise ValueError("tempo source hash mismatch: "+record["path"])
    plain=gzip.decompress(raw)
    if sha(plain)!=record["decompressed_sha256"]:
        raise ValueError("tempo decompressed source hash mismatch: "+record["path"])
    return raw,json.loads(plain)


def tempo_materials():
    """Reuse admitted bytes; derive only anonymous links and an audit presentation."""
    admission_raw=TEMPO_ADMISSION.read_bytes()
    admission=json.loads(admission_raw)
    result_raw,result=checked_gzip(admission["complete_readout"])
    audit_raw,audit=checked_gzip(admission["independent_endpoint_audit"])
    design_raw=TEMPO_DESIGN.read_bytes()
    if sha(design_raw)!=admission["frozen_design_sha256"]:
        raise ValueError("tempo design source hash mismatch")
    if (audit["status"]!="PASS_COMPLETE_RAW_GENOME_ENDPOINT_AND_PAIRED_BOOTSTRAP_AUDIT"
        or audit["official_readout_sha256"]!=admission["complete_readout"]["decompressed_sha256"]
        or result["design_sha256"]!=admission["frozen_design_sha256"]):
        raise ValueError("tempo audit and official source identities disagree")

    # The original table is immutable; only its identifying repository link changes.
    original=TEMPO_TABLES.read_bytes()
    text=original.decode("utf-8")
    original_link=("https://github.com/zuizui0223/izu-core/blob/main/"
                   "data/results/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json.gz")
    if text.count(original_link)!=1:
        raise ValueError("tempo source table link boundary changed")
    text=text.replace(original_link,"EVIDENCE/TEMPO_RESULTS.json.gz")
    text=text.replace("\n\n", "\n\nAnonymous presentation copy: only the complete-readout link was changed; "
                      "all original table rows and numerical values are retained.\n\n",1)
    comparisons=sum(len(row["independently_verified_outcomes"])
                    for row in audit["setting_results"])
    audit_summary={
        "schema":"chapter2_tempo_anonymous_audit_summary_v1",
        "artifact_role":"derived_anonymous_audit_summary_not_original_audit",
        "audit_scope_origin":"original event/order/occupancy audit",
        "status":audit["status"],
        "recomputation_performed_during_packaging":False,
        "original_audit_gzip_sha256":sha(audit_raw),
        "original_audit_json_sha256":admission["independent_endpoint_audit"]["decompressed_sha256"],
        "original_admission_sha256":sha(admission_raw),
        "official_readout_json_sha256":audit["official_readout_sha256"],
        "frozen_design_sha256":audit["frozen_design_sha256"],
        "verified_case_count":audit["verified_case_count"],
        "censuses_checked":sum(case["genotype_censuses_checked"] for case in audit["case_results"]),
        "verified_setting_count":audit["verified_setting_count"],
        "verified_outcome_fields_per_setting":audit["verified_outcome_fields_per_setting"],
        "setting_outcome_comparisons":comparisons,
        "compared_scalar_values":5*comparisons,
        "scalar_fields":"P_abrupt, P_gradual, abrupt_minus_gradual, lower and upper interval bounds",
        "comparison_absolute_tolerance":audit["comparison_absolute_tolerance"],
        "threshold_comparison":audit["threshold_comparison"],
        "bootstrap":audit["bootstrap"],
        "verification_scope":admission["verification_scope"],
        "interpretation_limits":audit["interpretation_limits"],
        "setting_results":audit["setting_results"],
    }
    if (comparisons!=admission["verification_scope"]["independently_recomputed_setting_outcomes"]
        or audit_summary["censuses_checked"]!=admission["sampling"]["censuses_including_founders"]):
        raise ValueError("tempo audit summary count mismatch")
    members={
        "TEMPO_FULL_TABLES.md":text.encode("utf-8"),
        "EVIDENCE/TEMPO_RESULTS.json.gz":result_raw,
        "EVIDENCE/TEMPO_DESIGN.json":design_raw,
        "EVIDENCE/TEMPO_AUDIT_SUMMARY.json":json_bytes(audit_summary),
    }
    derivations={
        "TEMPO_FULL_TABLES.md":{
            "original_path":str(TEMPO_TABLES.relative_to(ROOT)),
            "original_sha256":sha(original),
            "derived_sha256":sha(members["TEMPO_FULL_TABLES.md"]),
            "change":"Replace one repository URL with the packaged readout link; add derivation notice. All table rows unchanged.",
        },
        "EVIDENCE/TEMPO_AUDIT_SUMMARY.json":{
            "original_path":admission["independent_endpoint_audit"]["path"],
            "original_sha256":sha(audit_raw),
            "admission_path":str(TEMPO_ADMISSION.relative_to(ROOT)),
            "admission_sha256":sha(admission_raw),
            "derived_sha256":sha(members["EVIDENCE/TEMPO_AUDIT_SUMMARY.json"]),
            "change":"Retain all setting outcomes, scope and counts; omit case-level records and identifying input paths. Original audit unchanged.",
        },
    }
    return members,derivations,admission


def build_source_identity():
    def git(*args):
        return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
    return {"commit":git("rev-parse","HEAD"),
            "tree":git("rev-parse","HEAD^{tree}"),
            "tracked_worktree_changes":bool(git("status","--porcelain","--untracked-files=no")),
            "identity_scope":"Package build source; distinct from the frozen tempo execution source."}


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


def build(out:Path=OUT, *, figures=None,supplementary_figures=None):
    out=Path(out)
    figures=PDF_FIGURES if figures is None else figures
    if set(figures)!=set(PDF_FIGURES):
        raise ValueError("single paper requires exactly Figure1.pdf, Figure2.pdf and Figure3.pdf")
    supplementary_figures=SUPPLEMENTARY_FIGURES if supplementary_figures is None else supplementary_figures
    if set(supplementary_figures)!=set(SUPPLEMENTARY_FIGURES):
        raise ValueError("supplementary figures require SupplementaryFigureS1.pdf and SupplementaryFigureS2.svg")
    manuscript=blind_paper().encode("utf-8")
    si=(ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md").read_bytes()
    if any(token in si.lower().decode("utf-8") for token in DENIED):
        raise ValueError("blinded Supporting Information has identifying token")
    members={
      "MANUSCRIPT.md":manuscript,
      "SUPPORTING_INFORMATION.md":si,
      "Figure4.svg":render_svg().encode("utf-8"),
    }
    for dest,p in {**figures,**supplementary_figures}.items():
        members[dest]=Path(p).read_bytes()
    for label,path in FROZEN_RESULTS.items():
        b=(ROOT/path).read_bytes()
        json.loads(b)
        members["EVIDENCE/"+label]=b
    tempo,derivations,admission=tempo_materials()
    members.update(tempo)
    original_s2=next(row for row in admission["figures"] if row["path"].endswith(".svg"))
    if sha(members["SupplementaryFigureS2.svg"])!=original_s2["sha256"]:
        raise ValueError("tempo supplementary figure source hash mismatch")
    for name,raw in members.items():
        validate_member(name,raw)
    manifest={
        "status":"EL_ONE_PAPER_REVIEW_VERIFIED_NOT_SUBMITTED",
        "source_active_manuscript":"CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md",
        "n_figures":4,"n_supplementary_figures":2,"doi_deposit_complete":False,
        "evolution_evidence":"preregistered four-setting",
        "capacity_evidence":"one independent preregistered small K contrast; other cohorts descriptive",
        "tempo_evidence":"separately frozen descriptive supplement; 16 synthetic profiles, no pooling with the primary 64-history studies",
        "audit_scope":"Original event/order/occupancy audit: 128 setting/outcome comparisons; 156 secondary fields per setting were not independently aggregate-recomputed in that audit",
        "raw_trajectory_archive_included":False,
        "anonymous_derivations":["TEMPO_FULL_TABLES.md","EVIDENCE/TEMPO_AUDIT_SUMMARY.json"],
        "members":{name:{"size":len(b),"sha256":sha(b)}
                   for name,b in sorted(members.items())},
    }
    members["MANIFEST.json"]=json_bytes(manifest)
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,b in sorted(members.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
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
        "n_supplementary_figures":2,
        "build_source":build_source_identity(),
        "source_derivations":derivations,
        "receipt_is_internal_provenance_not_part_of_anonymous_archive":True,
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
