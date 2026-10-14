"""Verify the Journal of Ecology review package by isolated redraw of all three figures."""
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile, zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs/chapter2_je_delivery"
EXPORTS=[
    "outputs/figures/chapter2_je_20261006/figure1_plotted_values.csv",
    "outputs/figures/chapter2_je_20261006/figure1_receipt.json",
    "outputs/figures/chapter2_je_20261006/figure2_receipt.json",
    "outputs/figures/chapter2_je_20261006/figure3_plotted_estimates.csv",
    "outputs/figures/chapter2_je_20261006/figure3_receipt.json",
]
MODULES=[
    "scripts.figure_chapter2_je_return_components",
    "scripts.figure_chapter2_je_sequence",
    "scripts.figure_chapter2_je_fixed_assurance",
]

def main():
    archive=OUT/"chapter2_je_review_20261006.zip"
    target=Path(tempfile.mkdtemp(prefix="je-redraw-",dir=OUT))
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read("MANIFEST.json"))
        for name,rec in manifest.items():
            data=z.read(name)
            assert hashlib.sha256(data).hexdigest()==rec["sha256"]
            dest=(target/name).resolve()
            assert dest.is_relative_to(target.resolve())
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
    originals={rel:(target/rel).read_bytes() for rel in EXPORTS}
    for rel in EXPORTS: (target/rel).unlink()
    env=dict(os.environ,PYTHONPATH=str(target),PYTHONUTF8="1")
    commands=[]
    for module in MODULES:
        r=subprocess.run([sys.executable,"-m",module],cwd=target,env=env,
                         capture_output=True,text=True,encoding="utf-8",check=True)
        commands.append({"module":module,"exit_code":r.returncode})
    for rel,data in originals.items():
        if (target/rel).read_bytes()!=data:
            raise ValueError("redrawn export mismatch: "+rel)
    manuscript=(target/"MANUSCRIPT.md").read_text(encoding="utf-8")
    main=manuscript.split("# References",1)[0]
    assert len(main.split())<8000
    assert manuscript.count("**Figure 1.")==1
    assert manuscript.count("**Figure 2.")==1
    assert manuscript.count("**Figure 3.")==1
    receipt={
        "status":"three_je_figures_redrawn_from_isolated_package",
        "archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
        "commands":commands,
        "identical_exports":EXPORTS,
        "main_text_words":len(main.split()),
        "public_doi_deposited":False,
    }
    (OUT/"isolated_redraw.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))

if __name__=="__main__":
    main()
