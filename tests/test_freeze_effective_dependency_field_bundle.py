import json
from pathlib import Path

import pytest

from scripts.freeze_effective_dependency_field_bundle import (
    OPTIONAL_CHANNELS,
    REQUIRED_CHANNELS,
    build_manifest,
    write_manifest,
)


def make_csv(path: Path, header: str, rows: list[str]) -> None:
    path.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")


def make_bundle(tmp_path: Path):
    paths = {}
    for name in REQUIRED_CHANNELS:
        path = tmp_path / f"{name}.csv"
        make_csv(path, "id,value", [f"{name}_1,1", f"{name}_2,2"])
        paths[name] = path
    for name in OPTIONAL_CHANNELS:
        paths[name] = None
    return paths


def test_freeze_hashes_required_channels_without_opening_scientific_gates(tmp_path):
    manifest = build_manifest(make_bundle(tmp_path))
    assert manifest["status"] == "effective_dependency_raw_field_bundle_frozen"
    assert len(manifest["channels"]) == len(REQUIRED_CHANNELS)
    assert len(manifest["bundle_fingerprint_sha256"]) == 64
    assert all(len(row["sha256"]) == 64 for row in manifest["channels"])
    assert all(row["n_data_rows"] == 2 for row in manifest["channels"])
    assert manifest["analysis_admission_opened"] is False
    assert manifest["structural_completion_opened"] is False
    assert manifest["pilot_dispersion_opened"] is False
    assert manifest["confirmatory_adequacy_opened"] is False


def test_same_raw_bundle_can_revalidate_existing_freeze(tmp_path):
    paths = make_bundle(tmp_path)
    output = tmp_path / "freeze.json"
    first = build_manifest(paths)
    write_manifest(output, first)
    original = json.loads(output.read_text(encoding="utf-8"))
    second = build_manifest(paths)
    write_manifest(output, second)
    after = json.loads(output.read_text(encoding="utf-8"))
    assert after == original


def test_changed_raw_bytes_cannot_overwrite_existing_freeze(tmp_path):
    paths = make_bundle(tmp_path)
    output = tmp_path / "freeze.json"
    write_manifest(output, build_manifest(paths))
    plants = paths["plants"]
    plants.write_text(plants.read_text(encoding="utf-8") + "plants_3,3\n", encoding="utf-8")
    with pytest.raises(ValueError, match="different raw bytes"):
        write_manifest(output, build_manifest(paths))


def test_missing_required_channel_is_rejected(tmp_path):
    paths = make_bundle(tmp_path)
    paths["svd"] = None
    with pytest.raises(ValueError, match="required channel argument not supplied: svd"):
        build_manifest(paths)
