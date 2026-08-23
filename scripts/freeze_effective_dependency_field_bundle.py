#!/usr/bin/env python3
"""Freeze linked effective-dependency field inputs before inferential analysis.

The freeze records exact SHA256 hashes, byte counts, row counts and CSV headers
for every supplied raw channel. It does not decide whether a dataset is
scientifically adequate; structural/dispersion/confirmatory admission remains in
separate audits. Re-freezing to an existing manifest is allowed only when the
raw bundle is byte-identical, unless the caller writes to a new versioned output.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REQUIRED_CHANNELS = (
    "plants",
    "effort",
    "visits",
    "svd",
    "treatments",
    "fruits",
)
OPTIONAL_CHANNELS = (
    "seeds_parentage",
    "traits",
    "geometry",
    "calibration",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_shape(path: Path) -> tuple[int, list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration as error:
            raise ValueError(f"empty CSV: {path}") from error
        if not header or any(not cell.strip() for cell in header):
            raise ValueError(f"CSV has blank header field: {path}")
        n_rows = sum(1 for row in reader if any(cell.strip() for cell in row))
    return n_rows, header


def describe_channel(name: str, path: Path, *, required: bool) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"missing {'required' if required else 'supplied'} channel {name}: {path}")
    n_rows, header = csv_shape(path)
    return {
        "channel": name,
        "path": str(path),
        "required": required,
        "n_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "n_data_rows": n_rows,
        "header": header,
    }


def bundle_fingerprint(channels: Iterable[dict[str, object]]) -> str:
    canonical = [
        {
            "channel": item["channel"],
            "sha256": item["sha256"],
            "n_bytes": item["n_bytes"],
            "n_data_rows": item["n_data_rows"],
            "header": item["header"],
        }
        for item in sorted(channels, key=lambda row: str(row["channel"]))
    ]
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_manifest(paths: dict[str, Path | None]) -> dict[str, object]:
    channels: list[dict[str, object]] = []
    for name in REQUIRED_CHANNELS:
        path = paths.get(name)
        if path is None:
            raise ValueError(f"required channel argument not supplied: {name}")
        channels.append(describe_channel(name, path, required=True))
    for name in OPTIONAL_CHANNELS:
        path = paths.get(name)
        if path is not None:
            channels.append(describe_channel(name, path, required=False))
    fingerprint = bundle_fingerprint(channels)
    return {
        "schema_version": "1.1",
        "status": "effective_dependency_raw_field_bundle_frozen",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "required_channels": list(REQUIRED_CHANNELS),
        "optional_channels": list(OPTIONAL_CHANNELS),
        "channels": channels,
        "bundle_fingerprint_sha256": fingerprint,
        "analysis_admission_opened": False,
        "structural_completion_opened": False,
        "pilot_dispersion_opened": False,
        "confirmatory_adequacy_opened": False,
        "claim_boundary": (
            "This manifest establishes immutable raw-input identity only. It does not turn missing, pending, lost, damaged, unresolved-parentage, missing-trait, or failed-QC records into analyzable outcomes and does not open any scientific admission gate."
        ),
    }


def identity_view(manifest: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": manifest.get("schema_version"),
        "status": manifest.get("status"),
        "required_channels": manifest.get("required_channels"),
        "optional_channels": manifest.get("optional_channels"),
        "channels": manifest.get("channels"),
        "bundle_fingerprint_sha256": manifest.get("bundle_fingerprint_sha256"),
        "analysis_admission_opened": manifest.get("analysis_admission_opened"),
        "structural_completion_opened": manifest.get("structural_completion_opened"),
        "pilot_dispersion_opened": manifest.get("pilot_dispersion_opened"),
        "confirmatory_adequacy_opened": manifest.get("confirmatory_adequacy_opened"),
        "claim_boundary": manifest.get("claim_boundary"),
    }


def write_manifest(output: Path, manifest: dict[str, object]) -> None:
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if identity_view(existing) != identity_view(manifest):
            raise ValueError(
                "freeze manifest already exists for different raw bytes; write a new versioned manifest rather than overwriting the frozen bundle"
            )
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in REQUIRED_CHANNELS:
        parser.add_argument("--" + name.replace("_", "-"), dest=name, type=Path, required=True)
    for name in OPTIONAL_CHANNELS:
        parser.add_argument("--" + name.replace("_", "-"), dest=name, type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = {name: getattr(args, name) for name in REQUIRED_CHANNELS + OPTIONAL_CHANNELS}
    try:
        manifest = build_manifest(paths)
        write_manifest(args.output, manifest)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error
    print(args.output)


if __name__ == "__main__":
    main()
