from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from scripts import adapt_cabrera_natural_regime as cabrera
from scripts import adapt_hawaii_native_pollination_regime as hawaii
from scripts import adapt_mallorca_stability_regime as mallorca
from scripts import adapt_martinique_natural_regime as martinique
from scripts import adapt_roberts_england_natural_regime as england
from scripts import adapt_tenerife_natural_regime as tenerife
from scripts.audit_chapter2_phi_timebin_rarefaction import DEFAULT_OUT, run

ROOT = Path(__file__).resolve().parents[1]
HAWAII_CONFIG = ROOT / "config/hawaii_native_pollination_dryad_source.json"
MALLORCA_CONFIG = ROOT / "config/mallorca_stability_dryad_source.json"
TENERIFE_CONFIG = ROOT / "config/tenerife_pollination_zenodo_source.json"


def _download(url: str, *, timeout: int = 240) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_csv(rows: list[dict], path: Path, fields) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)
    return path


def _locked_dryad_workbook(
    config_path: Path,
    component_name: str,
    expected_sha256: str,
    target: Path,
) -> Path:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    package = _download(config["version_package_url"])
    try:
        archive = zipfile.ZipFile(io.BytesIO(package))
    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"{config_path.name}: Dryad package is not a ZIP") from exc
    with archive:
        candidates = [
            name for name in archive.namelist()
            if Path(name).name == component_name
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"{config_path.name}: expected exactly one {component_name!r}; got {candidates}"
            )
        payload = archive.read(candidates[0])
    observed = _sha256(payload)
    if observed != expected_sha256:
        raise RuntimeError(
            f"{config_path.name}: checksum drift for {component_name}: "
            f"{observed} != {expected_sha256}"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    return target


def _hawaii(workdir: Path) -> tuple[Path, dict]:
    config = json.loads(HAWAII_CONFIG.read_text(encoding="utf-8"))
    name = "Pollination visitation obs for dryad.xlsx"
    workbook = _locked_dryad_workbook(
        HAWAII_CONFIG,
        name,
        config["source_file_locks"][name]["sha256"],
        workdir / "hawaii.xlsx",
    )
    rows, diagnostics = hawaii.adapt_workbook(workbook)
    out = _write_csv(rows, workdir / "hawaii.csv", hawaii.OUTPUT_COLUMNS)
    return out, diagnostics


def _mallorca(workdir: Path) -> tuple[Path, dict]:
    workbook = _locked_dryad_workbook(
        MALLORCA_CONFIG,
        "Dryad_dataStability.xlsx",
        mallorca.DATA_SHA256,
        workdir / "mallorca.xlsx",
    )
    rows, diagnostics = mallorca.adapt_workbook(workbook)
    out = _write_csv(rows, workdir / "mallorca.csv", mallorca.OUTPUT_COLUMNS)
    return out, diagnostics


def _tenerife(workdir: Path) -> tuple[Path, dict]:
    config = json.loads(TENERIFE_CONFIG.read_text(encoding="utf-8"))
    record = json.loads(_download(config["api_url"]).decode("utf-8"))
    available = {Path(item["key"]).name: item for item in record.get("files", [])}
    root = workdir / "tenerife"
    root.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for filename in tenerife.SYSTEM_FILES.values():
        item = available.get(filename)
        if item is None:
            raise RuntimeError(f"Tenerife Zenodo record lacks {filename}")
        links = item.get("links", {})
        url = links.get("content") or links.get("self")
        if not url:
            raise RuntimeError(f"Tenerife {filename}: no file URL")
        payload = _download(url)
        (root / filename).write_bytes(payload)
        downloaded.append({"filename": filename, "bytes": len(payload), "sha256": _sha256(payload)})
    rows = tenerife.adapt(root)
    out = _write_csv(rows, workdir / "tenerife.csv", tenerife.OUTPUT_FIELDS)
    return out, {"files": downloaded, "rows": len(rows)}


def _cabrera(workdir: Path) -> tuple[Path, dict]:
    payload = cabrera.load_bytes(None)
    rows = cabrera.adapt(payload)
    out = _write_csv(rows, workdir / "cabrera.csv", cabrera.OUTPUT_FIELDS)
    return out, {"source_sha256": _sha256(payload), "rows": len(rows)}


def _martinique(workdir: Path) -> tuple[Path, dict]:
    payload = martinique.load_bytes(None)
    rows, structure = martinique.reconstruct(payload)
    out = _write_csv(rows, workdir / "martinique.csv", martinique.OUTPUT_FIELDS)
    return out, {"source_sha256": _sha256(payload), "rows": len(rows), "structure": structure}


def _england(workdir: Path) -> tuple[Path, dict]:
    interactions = england.load_bytes(
        england.INTERACTION_URL, england.INTERACTION_SHA256, None
    )
    flowers = england.load_bytes(
        england.FLOWER_URL, england.FLOWER_SHA256, None
    )
    rows = england.adapt(interactions, flowers)
    out = _write_csv(rows, workdir / "england.csv", england.OUTPUT_FIELDS)
    return out, {
        "interaction_sha256": _sha256(interactions),
        "flower_sha256": _sha256(flowers),
        "rows": len(rows),
    }


def build() -> dict:
    with tempfile.TemporaryDirectory(prefix="izu-phi-rarefaction-") as tmp:
        workdir = Path(tmp)
        inputs = []
        acquisition = {}
        for label, builder in (
            ("hawaii", _hawaii),
            ("mallorca", _mallorca),
            ("tenerife", _tenerife),
            ("cabrera", _cabrera),
            ("martinique", _martinique),
            ("england", _england),
        ):
            path, diagnostics = builder(workdir)
            inputs.append(path)
            acquisition[label] = diagnostics
        result = run(inputs)
    result["source_acquisition"] = acquisition
    result["source_acquisition_boundary"] = (
        "All six admitted sources are reconstructed from checksum-locked or API-identified "
        "public source bytes using the already frozen adapters. No coordinate value is used "
        "to select or alter source files."
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "valid_iterations": result["valid_iterations"],
        "phi_only": result["phi_only_primary"],
        "source_summary": result["source_summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
