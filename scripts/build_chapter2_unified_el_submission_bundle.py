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
ATOM_DATA=ROOT/"data/results/atom_cell_completed_20261011"
ATOM_DOC=ROOT/"docs/atom_comparison_20261011"
RESOLUTION_DATA=ROOT/"data/results/four_question_resolution_20261011"
RESOLUTION_DOC=ROOT/"docs/four_question_resolution_20261011"
MECHANISM_DATA=ROOT/"data/results/persistence_mechanism_20261012"
MINIMAL_RESULTS=ROOT/"data/results"
DENIED=("zuizui0223","github.com/","/workspace/","/home/","/root/",
        "issue #436","pr #452","pr #455")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value,sort_keys=True,indent=2)+"\n").encode("utf-8")


def mechanism_materials():
    delivery_raw=(MECHANISM_DATA/"delivery.json").read_bytes()
    delivery=json.loads(delivery_raw)
    members={}
    for filename,dest in {"readout.json":"EVIDENCE/MECHANISM_READOUT.json",
                          "original_readout.json.gz":"EVIDENCE/MECHANISM_ORIGINAL.json.gz",
                          "design.md":"EVIDENCE/MECHANISM_DESIGN.md"}.items():
        raw=(MECHANISM_DATA/filename).read_bytes()
        if sha(raw)!=delivery["sha256"][filename]:
            raise ValueError("mechanism source hash mismatch: "+filename)
        members[dest]=raw
    compact=json.loads(members["EVIDENCE/MECHANISM_READOUT.json"])
    original=gzip.decompress(members["EVIDENCE/MECHANISM_ORIGINAL.json.gz"])
    if sha(original)!=compact["original_readout_sha256"]:
        raise ValueError("mechanism original readout identity differs")
    source=json.loads(original)
    if (compact["status"]!="complete_archive_verified" or compact["verified_cases"]!=20480
        or compact["primary"]!=source["primary"] or compact["policy_differences"]!=source["policy_differences"]
        or compact["independent_arithmetic"]["report_sha256"]!=sha(original)
        or compact["independent_arithmetic"]["npz_cases"]!=20480):
        raise ValueError("mechanism admission scope differs")
    for row, differences in zip(compact["partition"],source["policy_differences"]):
        if row["factorial_interaction"]!=differences[0]-differences[1]-differences[2]+differences[3]:
            raise ValueError("mechanism predeclared interaction differs")
    expected=[{"target":s["target"],"policy":s["policy"],"origin":s["origin"],
               "all_starts":s["all_starts"],"terminal_occupancy":s["occupancy_by_update"][-1]}
              for s in source["secondary_descriptive"]]
    if compact["terminal_occupancy"]!=expected or len(compact["partition"])!=2:
        raise ValueError("mechanism descriptive inventory differs")
    return members,{name:{"source_delivery_sha256":sha(delivery_raw),
        "derived_sha256":sha(raw),"original_readout_sha256":sha(original),
        "transformation":"Exact hash-bound companion bytes; original readout compressed losslessly; descriptive factorial interaction added only in compact derivative."}
        for name,raw in members.items()}


def count_manuscript_words(text):
    return {
        "abstract":len(text.split("## Abstract",1)[1].split("## Keywords",1)[0].split()),
        "main_text":len(text.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0].split()),
    }


def minimal_resolution_materials():
    receipt_raw=(MINIMAL_RESULTS/'minimal_resolution_delivery_20261013.json').read_bytes()
    receipt=json.loads(receipt_raw)
    sources={
        'ecological_order_boundary_20261013.json':'EVIDENCE/ECOLOGICAL_ORDER_READOUT.json',
        'matched_operator_gap_20261013.json':'EVIDENCE/OPERATOR_GAP_READOUT.json',
        'chapter2_discovery_archive_recovery_20261013.json':'EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json',
        'genome_response_accounting_readout_20261013.json':'EVIDENCE/GENOME_RESPONSE_READOUT.json',
        'persistence_duration_accounting_20261013.json':'EVIDENCE/DURATION_READOUT.json',
        'initial_assurance_mean_20261013/readout.json':'EVIDENCE/INITIAL_MEAN_READOUT.json',
        'initial_assurance_mean_20261013/original_readout.json.gz':'EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz',
    }
    if receipt['status']!='ACTUAL_RAW_AND_ARITHMETIC_VERIFIED' or set(receipt['sha256'])!=set(sources):
        raise ValueError('minimal resolution admission inventory differs')
    members={};derivations={}
    for name,dest in sources.items():
        raw=(MINIMAL_RESULTS/name).read_bytes()
        canonical=raw if name.endswith('.gz') else raw.replace(b'\r\n',b'\n')
        if sha(raw) not in receipt['source_raw_sha256'][name] or sha(canonical)!=receipt['sha256'][name]:
            raise ValueError('minimal resolution source hash mismatch: '+name)
        members[dest]=canonical
        derivations[dest]=dict(source_delivery_sha256=sha(receipt_raw),original_sha256=sha(raw),derived_sha256=sha(canonical),transformation=receipt['transformation'])
    value=json.loads(members['EVIDENCE/INITIAL_MEAN_READOUT.json'])
    original=gzip.decompress(members['EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz'])
    raw=json.loads(original)
    if (sha(original)!=value['original_readout_sha256'] or value['primary']!=raw['primary']
        or value['new_native_futures']!=4096 or value['new_clamp_identity_futures']!=8
        or value['independent_arithmetic']['cases']!=4096 or value['source_execution_commit']!='615cd38156b0d0004a9415797ef498791b74257c'
        or json.loads(members['EVIDENCE/GENOME_RESPONSE_READOUT.json'])['updates']!=64000
        or json.loads(members['EVIDENCE/DURATION_READOUT.json'])['kernels']!=96):
        raise ValueError('minimal resolution scientific admission differs')
    gap=json.loads(members['EVIDENCE/OPERATOR_GAP_READOUT.json'])
    intake=json.loads(members['EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json'])
    if (gap['cases']!=320 or gap['updates']!=64000 or gap['actual_readback']['run']!=38306641012
        or gap['independent_pair_matrix']['updates']!=64000
        or intake['status']!='ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED'
        or not intake['verification']['archive_identity_verified']
        or intake['counts']['discovery_cases_verified']!=2048
        or intake['verification']['runtime_identity_verified'] or intake['verification']['original_discovery_full_replay_completed']):
        raise ValueError('matched gap/original archive admission differs')
    eco=json.loads(members['EVIDENCE/ECOLOGICAL_ORDER_READOUT.json'])
    if (eco['status']!='ALL2304_RAW_GENOTYPE_AND_ORDER_TRACES_ADMITTED' or eco['cases']!=2304
        or eco['updates']!=460800 or len(eco['cells'])!=18 or eco['actual_readback']['run']!=38312090996
        or eco['independent']['cases']!=2304 or eco['independent']['checks']!=6930
        or eco['supported_supply_pairs'] or eco['supported_composition_pairs']
        or not all(c['simultaneous_interval'][0]<=0<=c['simultaneous_interval'][1] for c in eco['cells'])):
        raise ValueError('ecological order admission/negative decision differs')
    return members,derivations


def anonymous_text(text,label):
    if any(token in text.lower() for token in DENIED):
        raise ValueError("identifying internal token remains in "+label)


def atom_materials():
    """Keep numerical values exact, deriving only a path-free presentation."""
    final_raw=(ATOM_DATA/"ATOM_ABM_FINAL_READOUT_20261011.json").read_bytes()
    final=json.loads(final_raw)
    sources={}
    for name,digest in final["inputs"].items():
        raw=(ATOM_DATA/name).read_bytes()
        if sha(raw)!=digest:
            raise ValueError("atom source hash mismatch: "+name)
        sources[name]=json.loads(raw)
    comparison=sources["matched_comparison.json"]
    audit=sources["matched_comparison_independent_verification.json"]
    admission=sources["admission.json"]
    numerical=sources["independent_verification.json"]
    envelope=sources["completion_envelope.json"]
    if (envelope["status"]!="all_30_archives_and_all_10_two_pair_decisions_verified"
        or envelope["independent_readout_sha256"]!=final["inputs"]["independent_verification.json"]
        or numerical["status"]!="all_30_archives_and_10_decisions_verified"
        or audit["status"]!="all320_abm_and10_density_descriptive_readouts_independently_recomputed"
        or audit["matched_comparison_sha256"]!=final["inputs"]["matched_comparison.json"]
        or (audit["abm_archives"],audit["density_archives"],audit["event_checks"],audit["checkpoint_checks"])!=(320,10,990,40)
        or len(comparison["abm_archive_sha256"])!=320
        or len(numerical["archive_sha256"])!=30
        or len(admission["contexts"])!=10
        or not all(c["admitted"] and len(c["checks"])==2 and all(x["passed"] for x in c["checks"]) for c in admission["contexts"])
        or {r["context"] for r in comparison["rows"]}!={r["context"] for r in admission["contexts"]}):
        raise ValueError("atom admission or independent comparison scope differs")
    table=(ATOM_DOC/"ATOM_ABM_COMPARISON_TABLE_20261011.csv").read_bytes()
    figure=(ATOM_DOC/"resolution_figures_20261011/atom_abm.pdf").read_bytes()
    if sha(table)!=final["csv_sha256"] or sha(figure)!=final["outputs"]["atom_abm.pdf"]:
        raise ValueError("atom source hash mismatch: table or figure")
    derived={
        "schema":"chapter2_atom_anonymous_comparison_v1",
        "artifact_role":"derived_anonymous_comparison_not_original_readout",
        "original_comparison_sha256":final["inputs"]["matched_comparison.json"],
        "original_admission_sha256":final["inputs"]["admission.json"],
        "original_independent_comparison_sha256":final["inputs"]["matched_comparison_independent_verification.json"],
        "rows":comparison["rows"],"admission_contexts":admission["contexts"],
        "scope":{"abm_archives":320,"density_archives":10,"event_checks":990,
                 "checkpoint_checks":40,"new_raw_genome_reconstruction":False,
                 "new_biological_simulation":False,"causal_drift_decomposition":False,
                 "numerical_scope":"assurance-only original birth mutation; not heat/full-three-locus PDE/SPDE or stochastic ensemble mean"},
    }
    members={"ATOM_FULL_TABLES.csv":table,"SupplementaryFigureS3.pdf":figure,
             "EVIDENCE/ATOM_ABM_COMPARISON.json":json_bytes(derived)}
    derivations={"EVIDENCE/ATOM_ABM_COMPARISON.json":{
        "original_path":str((ATOM_DATA/"matched_comparison.json").relative_to(ROOT)),
        "original_sha256":derived["original_comparison_sha256"],
        "admission_sha256":derived["original_admission_sha256"],
        "independent_comparison_sha256":derived["original_independent_comparison_sha256"],
        "final_readout_sha256":sha(final_raw),
        "derived_sha256":sha(members["EVIDENCE/ATOM_ABM_COMPARISON.json"]),
        "transformation":"Retain every comparison row and admission context; omit identifying source paths and select the independently verified scope."},
        "ATOM_FULL_TABLES.csv":{"original_sha256":sha(table),"transformation":"Exact original bytes"},
        "SupplementaryFigureS3.pdf":{"original_sha256":sha(figure),"transformation":"Exact original bytes"}}
    return members,derivations


def resolution_materials():
    """Present already verified all-start readouts without new inference."""
    delivery_raw=(RESOLUTION_DATA/"delivery.json").read_bytes()
    delivery=json.loads(delivery_raw)
    sources={}
    for name,digest in delivery["source_inputs"].items():
        raw=(RESOLUTION_DATA/name).read_bytes()
        if sha(raw)!=digest:
            raise ValueError("resolution source hash mismatch: "+name)
        sources[name]=json.loads(raw)
    design=(RESOLUTION_DOC/"DESIGN.md").read_bytes()
    if sha(design)!=delivery["design_sha256"]:
        raise ValueError("resolution source hash mismatch: design")
    boundary=sources["boundary_readout.json"]
    history=sources["history_readout.json"]
    arithmetic=sources["independent_readout_verification.json"]
    diagnostic=sources["history_state_diagnosis.json"]
    if (boundary["status"]!="complete_verified" or history["status"]!="complete_verified"
        or boundary["interval_family"]!=12 or len(boundary["groups"])!=12
        or history["primary_family"]!=4 or len(history["contexts"])!=2
        or delivery["source_closed_cohort_counts"]!={"boundary":6144,"preparation":3072,"future":6144}
        or delivery["new_inference_computed_for_delivery"] is not False
        or len(boundary["replicated_transition_bands"])!=3
        or arithmetic["boundary"]["cases"]!=6144 or arithmetic["history"]["cases"]!=3072
        or arithmetic["boundary"]["records_sha256"]!=boundary["records_sha256"]
        or arithmetic["history"]["records_sha256"]!=history["records_sha256"]
        or diagnostic["records_sha256"]!=history["records_sha256"]):
        raise ValueError("resolution source scope differs")
    derived={"schema":"chapter2_anonymous_conditional_resolution_v1",
             "artifact_role":"derived_anonymous_resolution_not_original_records",
             "boundary":boundary,"history":history,"achieved_state_diagnostic":diagnostic,
             "independent_arithmetic":arithmetic,
             "scope":{"source_closed_cohort_counts":delivery["source_closed_cohort_counts"],
                      "new_inference_computed_for_delivery":False,
                      "interpretation":delivery["scope"],
                      "original_readout_sha256":{n:delivery["source_inputs"][n] for n in
                                                 ["boundary_readout.json","history_readout.json","history_state_diagnosis.json","independent_readout_verification.json"]}}}
    members={"EVIDENCE/RESOLUTION_READOUT.json":json_bytes(derived),"EVIDENCE/RESOLUTION_DESIGN.md":design}
    derivations={"EVIDENCE/RESOLUTION_READOUT.json":{
        "delivery_path":str((RESOLUTION_DATA/"delivery.json").relative_to(ROOT)),
        "delivery_sha256":sha(delivery_raw),"original_readout_sha256":derived["scope"]["original_readout_sha256"],
        "derived_sha256":sha(members["EVIDENCE/RESOLUTION_READOUT.json"]),
        "transformation":"Retain complete boundary/history readouts, achieved-state diagnostic and arithmetic audit; select path-free scope. No new inference."},
        "EVIDENCE/RESOLUTION_DESIGN.md":{"original_sha256":sha(design),"transformation":"Exact frozen design bytes"}}
    return members,derivations


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
      "The preservation status and verification limits of the frozen study designs, "
      "source code and simulation outputs are documented in the Supporting Information. "
      "The original discovery archive and positive-mutation endpoints have been authenticated; historical execution/runtime and annual-genome replay remain unverified. "
      "A permanent DOI-backed raw-data archive has not yet been deposited. "
      "An appropriately anonymous, editor-approved access route is required "
      "before manuscript submission; depositing the underlying raw data "
      "remains an outstanding requirement.\n\n"
    )
    manuscript=manuscript[:start]+anonymous+manuscript[end:]
    # Route references to supplied evidence; do not promise an absent source file.
    figure_path="figures/chapter2_k_at_B48_three_cohort_original_intervals_20261010.svg"
    manuscript=manuscript.replace("../"+figure_path,"Figure4.svg")
    manuscript=manuscript.replace(figure_path,"Figure4.svg")
    manuscript=manuscript.replace(
      "generated without refitting by `scripts/render_chapter2_capacity_companion_evidence_figure.py`",
      "generated without refitting from the original cohort readouts",
    )
    manuscript=manuscript.replace(
      "`docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md`",
      "Supporting Information S3",
    )
    if re.search(r"(?<!\w)(?:docs|figures|data/design|data/results|scripts)/[A-Za-z0-9_./-]+",manuscript):
        raise ValueError("unmapped internal reference in blinded paper")
    if any(x in manuscript.lower() for x in DENIED):
        raise ValueError("identifying internal token remains")
    counts=count_manuscript_words(manuscript)
    if counts["abstract"]>150 or counts["main_text"]>5000:
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
    manuscript_text=blind_paper()
    counts=count_manuscript_words(manuscript_text)
    manuscript=manuscript_text.encode("utf-8")
    si_path=ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
    si_original=si_path.read_bytes()
    si_text=si_original.decode("utf-8")
    old_link="atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md"
    old_dir="data/results/atom_cell_completed_20261011/"
    if si_text.count(old_link)!=1 or si_text.count(old_dir)!=1:
        raise ValueError("atom SI source-link boundary changed")
    si_text=si_text.replace(old_link,"ATOM_FULL_TABLES.csv").replace(old_dir,"EVIDENCE/ATOM_ABM_COMPARISON.json")
    si_text=si_text.replace("The supplemental figure does not replace existing main figures.",
                            "[Supplementary Figure S3](SupplementaryFigureS3.pdf) does not replace existing main figures.")
    resolution_link="four_question_resolution_20261011/DESIGN.md"
    resolution_dir="data/results/four_question_resolution_20261011/"
    if si_text.count(resolution_link)!=1 or si_text.count(resolution_dir)!=1:
        raise ValueError("resolution SI source-link boundary changed")
    si_text=si_text.replace(resolution_link,"EVIDENCE/RESOLUTION_DESIGN.md").replace(resolution_dir,"EVIDENCE/RESOLUTION_READOUT.json")
    si_text=si_text.replace("../data/results/persistence_mechanism_20261012/readout.json","EVIDENCE/MECHANISM_READOUT.json")
    si_text=si_text.replace("../data/results/persistence_mechanism_20261012/design.md","EVIDENCE/MECHANISM_DESIGN.md")
    si_text=si_text.replace("../data/results/persistence_mechanism_20261012/original_readout.json.gz","EVIDENCE/MECHANISM_ORIGINAL.json.gz")
    si=si_text.encode("utf-8")
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
    atom,atom_derivations=atom_materials()
    members.update(atom)
    derivations.update(atom_derivations)
    resolution,resolution_derivations=resolution_materials()
    members.update(resolution)
    derivations.update(resolution_derivations)
    mechanism,mechanism_derivations=mechanism_materials()
    members.update(mechanism)
    derivations.update(mechanism_derivations)
    minimal,minimal_derivations=minimal_resolution_materials()
    members.update(minimal)
    derivations.update(minimal_derivations)
    derivations["SUPPORTING_INFORMATION.md"]={
        "original_path":str(si_path.relative_to(ROOT)),"original_sha256":sha(si_original),
        "derived_sha256":sha(si),"transformation":"Relocate atom/resolution/mechanism companion source references and add the delivered supplementary-figure link; numerical text unchanged."}
    original_s2=next(row for row in admission["figures"] if row["path"].endswith(".svg"))
    if sha(members["SupplementaryFigureS2.svg"])!=original_s2["sha256"]:
        raise ValueError("tempo supplementary figure source hash mismatch")
    for name,raw in members.items():
        validate_member(name,raw)
    manifest={
        "status":"EL_ONE_PAPER_REVIEW_VERIFIED_NOT_SUBMITTED",
        "source_active_manuscript":"CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md",
        "n_figures":4,"n_supplementary_figures":3,"doi_deposit_complete":False,
        "word_counts":counts,
        "word_count_method":"Whitespace-separated tokens; main text begins at Introduction and ends before primary figure captions.",
        "evolution_evidence":"preregistered four-setting",
        "capacity_evidence":"one independent preregistered small K contrast; other cohorts descriptive",
        "tempo_evidence":"separately frozen descriptive supplement; 16 synthetic profiles, no pooling with the primary 64-history studies",
        "audit_scope":"Original event/order/occupancy audit: 128 setting/outcome comparisons; 156 secondary fields per setting were not independently aggregate-recomputed in that audit",
        "raw_trajectory_archive_included":False,
        "anonymous_derivations":["TEMPO_FULL_TABLES.md","EVIDENCE/TEMPO_AUDIT_SUMMARY.json","EVIDENCE/ATOM_ABM_COMPARISON.json","EVIDENCE/RESOLUTION_READOUT.json","EVIDENCE/MECHANISM_READOUT.json","SUPPORTING_INFORMATION.md"],
        "mechanism_evidence":"20480 full-genome-admitted futures and independent all-start arithmetic; lifelong expression policies, not initial-only or natural-order mediation; low-challenge terminal floor retained",
        "atom_evidence":"All10 two-grid numerical admissions and320 descriptive ABM histories;990 event and40 checkpoint independent array checks, no new raw-genome reconstruction or causal drift attribution",
        "resolution_evidence":"6144 boundary,3072 shared preparations,6144 branched challenges; genetic-access band and conditional all-start preparation-policy effects, not pure natural-order mediation",
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
        "n_supplementary_figures":3,
        "word_counts":counts,
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
