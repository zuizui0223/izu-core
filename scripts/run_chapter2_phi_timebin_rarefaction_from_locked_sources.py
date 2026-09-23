from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

from scripts.adapt_cabrera_natural_regime import adapt as adapt_cabrera
from scripts.adapt_cabrera_natural_regime import load_bytes as load_cabrera
from scripts.adapt_hawaii_native_pollination_regime import adapt_workbook as adapt_hawaii
from scripts.adapt_hawaii_native_pollination_regime import write_canonical_csv as write_hawaii
from scripts.adapt_mallorca_stability_regime import adapt_workbook as adapt_mallorca
from scripts.adapt_mallorca_stability_regime import write_canonical_csv as write_mallorca
from scripts.adapt_martinique_natural_regime import reconstruct as adapt_martinique
from scripts.adapt_martinique_natural_regime import load_bytes as load_martinique
from scripts.adapt_roberts_england_natural_regime import (
    FLOWER_SHA256,
    FLOWER_URL,
    INTERACTION_SHA256,
    INTERACTION_URL,
    adapt as adapt_england,
    load_bytes as load_england_bytes,
)
from scripts.adapt_tenerife_natural_regime import SYSTEM_FILES, adapt as adapt_tenerife
from scripts.audit_chapter2_phi_timebin_rarefaction import run as run_rarefaction

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"


def _request(url: str, accept: str = "*/*") -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": accept},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = response.read()
    if not payload:
        raise RuntimeError(f"empty public-source response: {url}")
    return payload


def _write_rows(rows: list[dict[str, object]], path: Path) -> None:
    fields = [
        "source_study_id",
        "archipelago_id",
        "system_id",
        "time_bin",
        "partner_id",
        "value",
        "effort",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _dryad_component(config_path: Path, component: str, destination: Path) -> Path:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    package = _request(
        str(config["version_package_url"]),
        "application/zip, application/octet-stream, */*;q=0.8",
    )
    with zipfile.ZipFile(io.BytesIO(package)) as archive:
        matches = [
            info
            for info in archive.infolist()
            if not info.is_dir() and PurePosixPath(info.filename).name == component
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"{config_path.name}: expected one {component!r}, found {len(matches)}"
            )
        data = archive.read(matches[0])
    lock = (config.get("source_file_locks") or {}).get(component)
    if lock:
        observed = hashlib.sha256(data).hexdigest()
        if int(lock["bytes"]) != len(data) or str(lock["sha256"]) != observed:
            raise RuntimeError(
                f"{config_path.name}: source lock mismatch for {component}: "
                f"bytes={len(data)} sha256={observed}"
            )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


def _zenodo_tenerife(config_path: Path, root: Path) -> Path:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    record = json.loads(_request(str(config["api_url"]), "application/json").decode("utf-8"))
    files = record.get("files") or []
    by_name = {
        PurePosixPath(str(row.get("key") or row.get("filename") or "")).name: row
        for row in files
    }
    needed = set(SYSTEM_FILES.values())
    root.mkdir(parents=True, exist_ok=True)

    # Some Zenodo records expose the source-native text files directly, while
    # record 5008210 currently exposes them inside one deposited ZIP. Support
    # both layouts without changing the frozen source-native file names.
    if needed.issubset(set(by_name)):
        for name in sorted(needed):
            row = by_name[name]
            links = row.get("links") or {}
            url = links.get("content") or links.get("self")
            if not url:
                raise RuntimeError(f"Tenerife file has no download link: {name}")
            data = _request(str(url), "application/octet-stream, text/plain, */*;q=0.8")
            checksum = str(row.get("checksum") or "")
            if checksum.startswith("md5:"):
                observed = hashlib.md5(data).hexdigest()
                if observed != checksum.split(":", 1)[1]:
                    raise RuntimeError(f"Tenerife checksum mismatch: {name}")
            (root / name).write_bytes(data)
        return root

    zip_rows = [
        row
        for row in files
        if PurePosixPath(str(row.get("key") or row.get("filename") or "")).suffix.lower() == ".zip"
    ]
    if len(zip_rows) != 1:
        missing = sorted(needed - set(by_name))
        raise RuntimeError(
            f"Tenerife Zenodo record missing direct files {missing} and "
            f"has {len(zip_rows)} ZIP candidates"
        )

    zip_row = zip_rows[0]
    links = zip_row.get("links") or {}
    zip_url = links.get("content") or links.get("self")
    if not zip_url:
        raise RuntimeError("Tenerife ZIP has no download link")
    payload = _request(str(zip_url), "application/zip, application/octet-stream, */*;q=0.8")

    checksum = str(zip_row.get("checksum") or "")
    if checksum.startswith("md5:"):
        observed_md5 = hashlib.md5(payload).hexdigest()
        if observed_md5 != checksum.split(":", 1)[1]:
            raise RuntimeError(
                f"Tenerife ZIP MD5 mismatch: observed={observed_md5}"
            )

    admission = json.loads(
        (ROOT / "data/design/chapter2_tenerife_natural_regime_admission_20260914.json")
        .read_text(encoding="utf-8")
    )
    expected_sha256 = str(admission["source"]["archive_sha256"])
    observed_sha256 = hashlib.sha256(payload).hexdigest()
    if observed_sha256 != expected_sha256:
        raise RuntimeError(
            "Tenerife ZIP SHA256 differs from frozen admission: "
            f"observed={observed_sha256} expected={expected_sha256}"
        )

    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = {
            PurePosixPath(info.filename).name: info
            for info in archive.infolist()
            if not info.is_dir()
        }
        missing = sorted(needed - set(members))
        if missing:
            raise RuntimeError(f"Tenerife ZIP missing source-native files: {missing}")
        for name in sorted(needed):
            (root / name).write_bytes(archive.read(members[name]))
    return root


def build_canonical_sources(work_dir: Path) -> list[Path]:
    work_dir.mkdir(parents=True, exist_ok=True)
    canonical_dir = work_dir / "canonical"
    raw_dir = work_dir / "raw"
    canonical_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    hawaii_workbook = _dryad_component(
        ROOT / "config/hawaii_native_pollination_dryad_source.json",
        "Pollination visitation obs for dryad.xlsx",
        raw_dir / "hawaii.xlsx",
    )
    hawaii_rows, _ = adapt_hawaii(hawaii_workbook)
    hawaii_csv = canonical_dir / "hawaii.csv"
    write_hawaii(hawaii_rows, hawaii_csv)

    mallorca_workbook = _dryad_component(
        ROOT / "config/mallorca_stability_dryad_source.json",
        "Dryad_dataStability.xlsx",
        raw_dir / "mallorca.xlsx",
    )
    mallorca_rows, _ = adapt_mallorca(mallorca_workbook)
    mallorca_csv = canonical_dir / "mallorca.csv"
    write_mallorca(mallorca_rows, mallorca_csv)

    tenerife_root = _zenodo_tenerife(
        ROOT / "config/tenerife_pollination_zenodo_source.json",
        raw_dir / "tenerife",
    )
    tenerife_rows = adapt_tenerife(tenerife_root)
    tenerife_csv = canonical_dir / "tenerife.csv"
    _write_rows(tenerife_rows, tenerife_csv)

    cabrera_rows = adapt_cabrera(load_cabrera(None))
    cabrera_csv = canonical_dir / "cabrera.csv"
    _write_rows(cabrera_rows, cabrera_csv)

    martinique_rows, _ = adapt_martinique(load_martinique(None))
    martinique_csv = canonical_dir / "martinique.csv"
    _write_rows(martinique_rows, martinique_csv)

    england_rows = adapt_england(
        load_england_bytes(INTERACTION_URL, INTERACTION_SHA256, None),
        load_england_bytes(FLOWER_URL, FLOWER_SHA256, None),
    )
    england_csv = canonical_dir / "england.csv"
    _write_rows(england_rows, england_csv)

    return [
        hawaii_csv,
        mallorca_csv,
        tenerife_csv,
        cabrera_csv,
        martinique_csv,
        england_csv,
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data/results/chapter2_phi_timebin_rarefaction_20260922.json",
    )
    args = parser.parse_args()

    inputs = build_canonical_sources(args.work_dir)
    result = run_rarefaction(inputs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "systems": result["systems"],
        "sources": result["sources"],
        "valid_iterations": result["valid_iterations"],
        "phi_only_pass_fraction": result["phi_only_primary"]["dispersion_criteria_pass_fraction"],
        "england_loo_pass_fraction": result["phi_only_primary"]["leave_one_source_out_pass_fraction"].get(
            "euppollnet_31_roberts_england_step"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
