"""Verify and package Chapter 2 raw GitHub Actions artifacts for DOI deposition."""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/chapter2_public_archive_manifest_20261006.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def expected_artifacts(manifest):
    for campaign, block in manifest["campaigns"].items():
        for rec in block["artifacts"]:
            yield campaign, rec

def verify(artifact_dir: Path, manifest: dict) -> list[dict]:
    rows = []
    for campaign, rec in expected_artifacts(manifest):
        path = artifact_dir / campaign / (rec["name"] + ".zip")
        if not path.is_file():
            raise FileNotFoundError(path)
        got = sha256(path)
        expected = rec["digest"].removeprefix("sha256:")
        if got != expected:
            raise ValueError(f"digest mismatch: {path.name}: {got} != {expected}")
        rows.append({"campaign": campaign, "name": rec["name"], "bytes": path.stat().st_size, "sha256": got})
    for campaign, block in manifest["campaigns"].items():
        n = sum(1 for x in rows if x["campaign"] == campaign and "-shard-" in x["name"])
        if n != block["expected_shards"]:
            raise ValueError(f"{campaign}: expected {block['expected_shards']} shards, found {n}")
    return rows

def build(artifact_dir: Path, out: Path) -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = verify(artifact_dir, manifest)
    staging = out.parent / (out.stem + "-staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    shutil.copy2(MANIFEST, staging / "PUBLIC_ARCHIVE_MANIFEST.json")
    include = [
        manifest["campaigns"]["confirmatory"]["design_file"],
        manifest["campaigns"]["confirmatory"]["committed_result_file"],
        manifest["campaigns"]["assurance_generality"]["design_file"],
        manifest["campaigns"]["assurance_generality"]["committed_result_file"],
        *manifest["derived_committed_results"],
        manifest["manuscript"],
    ]
    for rel in include:
        src = ROOT / rel
        dst = staging / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for campaign, rec in expected_artifacts(manifest):
        src = artifact_dir / campaign / (rec["name"] + ".zip")
        dst = staging / "raw-artifacts" / campaign / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    receipt = {
        "status": "verified_deposition_bundle",
        "source_main_sha": manifest["source_main_sha"],
        "artifact_count": len(rows),
        "raw_artifact_bytes": sum(x["bytes"] for x in rows),
        "campaigns": {k: {"declared_cases": v["declared_cases"], "expected_shards": v["expected_shards"]} for k, v in manifest["campaigns"].items()},
        "doi_assigned": False,
    }
    (staging / "VERIFY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as z:
        for p in sorted(staging.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(staging).as_posix())
    receipt["bundle_sha256"] = sha256(out)
    receipt["bundle_bytes"] = out.stat().st_size
    (out.with_suffix(out.suffix + ".receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    shutil.rmtree(staging)
    return receipt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=ROOT / "outputs/chapter2_public_archive/chapter2_public_archive_20261006.zip")
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps(build(args.artifact_dir, args.out), indent=2))

if __name__ == "__main__":
    main()
