"""Build the Journal of Ecology review package from committed confirmed evidence."""
from pathlib import Path
import hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs/chapter2_je_delivery"
MANUSCRIPT=ROOT/"docs/CHAPTER2_MANUSCRIPT_JE_20261006.md"
SI=ROOT/"docs/CHAPTER2_SUPPORTING_INFORMATION_JE_20261006.md"
FIGDIR=ROOT/"outputs/figures/chapter2_je_20261006"
MAIN={
    "Figure1.pdf":"figure1_return_components.pdf",
    "Figure2.pdf":"figure2_confirmed_sequence.pdf",
    "Figure3.pdf":"figure3_fixed_assurance.pdf",
}
SUPPORT=[
    "docs/CHAPTER2_1005_ESTABLISHMENT_CLOSEOUT_20261006.md",
    "docs/CHAPTER2_1005_FIVE_CRITERIA_AUDIT_20261006.md",
    "docs/CHAPTER2_1005_NOVELTY_AND_LITERATURE_POSITION_20261006.md",
    "docs/CHAPTER2_JOURNAL_ROUTE_20261006.md",
    "docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md",
]
INPUTS=[
    "data/results/model3_return_components_20261005.json",
    "data/results/chapter2_1005_confirmatory_replication_20261006.json",
    "data/results/chapter2_1005_confirmatory_primary_sequence_history_20261006.csv",
    "data/results/chapter2_1005_confirmatory_primary_fixed_assurance_history_20261006.csv",
    "data/results/chapter2_1005_confirmatory_artifact_manifest_20261006.json",
    "data/design/chapter2_1005_confirmatory_replication_20261006.json",
    "scripts/figure_chapter2_je_return_components.py",
    "scripts/figure_chapter2_je_sequence.py",
    "scripts/figure_chapter2_je_fixed_assurance.py",
    "pyproject.toml",
]
EXPORTS=[
    "figure1_plotted_values.csv","figure1_receipt.json",
    "figure2_receipt.json",
    "figure3_plotted_estimates.csv","figure3_receipt.json",
]

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    members={"MANUSCRIPT.md":MANUSCRIPT.read_bytes(), "SUPPORTING_INFORMATION.md":SI.read_bytes()}
    for name,rel in MAIN.items():
        members[name]=(FIGDIR/rel).read_bytes()
    for rel in SUPPORT+INPUTS:
        members[rel]=(ROOT/rel).read_bytes()
    for name in EXPORTS:
        members["outputs/figures/chapter2_je_20261006/"+name]=(FIGDIR/name).read_bytes()
    members["READ_ME.txt"]=(
        "JOURNAL OF ECOLOGY REVIEW PACKAGE — CONFIRMED CHAPTER 2 PROCESS RESULT\n"
        "Primary inference unit: 64 independent visitor histories; eight demographic repeats are nested.\n"
        "Main paper contains three figures: ecological return, confirmed sequence/scope, and fixed-assurance necessity.\n"
        "Submission-facing Supporting Information is included as SUPPORTING_INFORMATION.md.\n"
        "The DOI-ready raw confirmatory bundle is prepared but public DOI deposition remains external and pending.\n"
        "To redraw the three figures from included committed evidence:\n"
        "python -m scripts.figure_chapter2_je_return_components\n"
        "python -m scripts.figure_chapter2_je_sequence\n"
        "python -m scripts.figure_chapter2_je_fixed_assurance\n"
        "These commands redraw summaries only; they do not rerun the 4,096 confirmatory trajectories.\n"
    ).encode("utf-8")
    manifest={name:{"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
              for name,data in sorted(members.items())}
    members["MANIFEST.json"]=(json.dumps(manifest,indent=2)+"\n").encode("utf-8")
    archive=OUT/"chapter2_je_review_20261006.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(members.items()): z.writestr(name,data)
    with zipfile.ZipFile(archive) as z:
        for name,data in members.items():
            assert z.read(name)==data
    receipt={
        "status":"je_review_package_readback_verified",
        "archive":str(archive.relative_to(ROOT)),
        "sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
        "members":len(members),
        "bytes":archive.stat().st_size,
        "main_figures":3,
        "confirmatory_status":"confirmed",
        "public_doi_deposited":False,
    }
    (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

if __name__=="__main__":
    print(json.dumps(build(),indent=2))
