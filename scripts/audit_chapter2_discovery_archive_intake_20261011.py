"""Read-only admission of the named replenishment archive's discovery endpoints.

This verifier does not extract archives, import biological sources, consume RNG,
or replay populations. Endpoint admission cannot establish annual replay or a
frozen numerical runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from zipfile import BadZipFile, ZipFile

import numpy as np


STATUS = "ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED"
ROOT = Path(__file__).resolve().parents[1]
DESIGN = "data/design/model3_replenishment_evolution_20261005.json"
RECEIPT = "data/results/model3_replenishment_archive_20261005.json"
# These pin the committed local trust anchors, not historical ZIP text formatting.
DESIGN_SHA256 = "dcd39ef44b98314cdbeeacbd3fc29c9755a6ff7545c3b773ab06d6df2113029a"
RECEIPT_SHA256 = "15becd79af2ed2646a8ede226761172bdd92ed139144f10379e4fdd581e03601"
CHECKPOINTS = (0, 200, 400, 1000)
SUMMARY_ATOL = 1e-12  # Numerical readback tolerance, not a biological threshold.


class _Rejected(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def _require(condition, code, detail):
    if not condition:
        raise _Rejected(code, detail)


def _json(data, label):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f"nonfinite JSON constant: {value}")

    try:
        return json.loads(data, object_pairs_hook=unique_keys,
                          parse_constant=invalid_constant)
    except (ValueError, UnicodeError) as exc:
        raise _Rejected("invalid_json", f"{label}: {exc}") from exc


def _load_contract():
    documents = []
    for name, expected in ((DESIGN, DESIGN_SHA256), (RECEIPT, RECEIPT_SHA256)):
        try:
            data = (ROOT / name).read_bytes()
        except OSError as exc:
            raise _Rejected("frozen_contract_unavailable", f"{name}: {exc}") from exc
        _require(hashlib.sha256(data).hexdigest() == expected,
                 "frozen_contract_mismatch", f"Committed trust anchor changed: {name}")
        documents.append(_json(data, name))
    return tuple(documents)


def _digest(handle):
    digest = hashlib.sha256()
    size = 0
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
        size += len(chunk)
        digest.update(chunk)
    return size, digest.hexdigest()


def _case_contract(plan):
    paths, endpoints = set(), {}
    for setting in plan["settings"]:
        for distance in plan["distance_coordinates"]:
            for seed in plan["history_seeds"]:
                for rep in plan["demographic_repeats"]:
                    if distance == 0:
                        folder = "model3_full_mutation_20261004"
                        stem = f"core_{setting}_u0.01_h{seed}_r{rep}_near"
                        arm = "near"
                    elif distance == 3:
                        folder = "model3_persistent_isolation_20261005"
                        stem = f"persistent_core_{setting}_u0.01_h{seed}_r{rep}_far"
                        arm = "far"
                    else:
                        folder = "model3_replenishment_evolution_20261005"
                        stem = f"{setting}_d{distance:.2f}_h{seed}_r{rep}"
                        arm = None
                    base = f"outputs/{folder}/{stem}"
                    paths.update((base + ".npz", base + ".json"))
                    if arm is not None:
                        endpoints[base] = ["abm", setting, .01, seed, rep,
                                           arm, 0, "jump", False]
    return paths, endpoints


def _canonical(path):
    return (isinstance(path, str) and bool(path) and
            "\\" not in path and "\x00" not in path and ":" not in path and
            all(part not in ("", ".", "..") for part in path.split("/")))


def _verify_manifest(archive, receipt, case_paths, report):
    members = {}
    for info in archive.infolist():
        name = info.filename
        _require(_canonical(name) and name == info.orig_filename,
                 "noncanonical_zip_path", f"Noncanonical ZIP member: {name!r}")
        _require(name not in members, "duplicate_zip_path", f"Duplicate ZIP member: {name}")
        members[name] = info
    reserved = {"ARCHIVE_MANIFEST.json", "RESTORE.txt"}
    _require(reserved <= members.keys(), "manifest_member_set_mismatch",
             "Archive manifest or restoration note is missing")
    manifest = _json(archive.read("ARCHIVE_MANIFEST.json"), "ARCHIVE_MANIFEST.json")
    _require(isinstance(manifest, dict) and type(manifest.get("cases")) is int and
             manifest["cases"] == receipt["cases"], "manifest_case_count_mismatch",
             "Manifest case count differs from the external receipt")
    _require(isinstance(manifest.get("files"), list), "invalid_manifest",
             "Manifest files must be a list")
    records = {}
    for row in manifest["files"]:
        _require(isinstance(row, dict) and _canonical(row.get("path")),
                 "invalid_manifest", "Manifest record lacks a canonical path")
        path = row["path"]
        _require(path not in records, "duplicate_manifest_path",
                 f"Duplicate manifest path: {path}")
        _require(type(row.get("bytes")) is int and row["bytes"] >= 0 and
                 isinstance(row.get("sha256"), str) and
                 re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None,
                 "invalid_manifest", f"Invalid size or SHA256: {path}")
        records[path] = row
    missing = sorted(case_paths - (records.keys() & members.keys()))
    _require(not missing, "missing_case_members",
             f"Missing {len(missing)} required raw/receipt members; first: {missing[:1]}")
    _require(not (reserved & records.keys()) and
             members.keys() == records.keys() | reserved and
             len(records) == receipt["members"] and
             len(members) == receipt["members"] + 2,
             "manifest_member_set_mismatch",
             "ZIP directory and external manifest-record count must match exactly")
    digests = {}
    for path, info in members.items():
        with archive.open(info) as handle:
            size, sha256 = _digest(handle)
        if path in records:
            row = records[path]
            _require(size == row["bytes"] == info.file_size and sha256 == row["sha256"],
                     "manifest_member_mismatch", f"Manifest byte identity differs: {path}")
        digests[path] = sha256
    report["verification"]["manifest_complete"] = True
    report["counts"]["zip_members_verified"] = len(members)
    report["counts"]["manifest_records_verified"] = len(records)
    report["manifest"] = {
        "sha256": digests["ARCHIVE_MANIFEST.json"],
        "cases": manifest["cases"], "records": len(records),
        "zip_entries": len(members),
    }
    return digests


def _verify_sources(archive, plan, digests, report):
    for path, expected in plan["source_sha256"].items():
        _require(digests.get(path) == expected, "embedded_source_mismatch",
                 f"Embedded raw source/configuration differs from frozen plan: {path}")
    _require(DESIGN in digests, "embedded_design_mismatch", "Embedded design is missing")
    embedded = _json(archive.read(DESIGN), DESIGN)
    # Object ordering/whitespace/line endings may differ; parsed values may not.
    _require(json.dumps(embedded, sort_keys=True) == json.dumps(plan, sort_keys=True),
             "embedded_design_mismatch", "Embedded design differs from the frozen plan")
    report["verification"]["embedded_sources_verified"] = True
    report["counts"]["embedded_sources_verified"] = len(plan["source_sha256"])


def _verify_endpoint(archive, base, task, digests, capacity):
    receipt = _json(archive.read(base + ".json"), base + ".json")
    actual = receipt.get("task") if isinstance(receipt, dict) else None
    _require(isinstance(actual, list) and len(actual) == len(task) and
             all(type(value) is type(expected) and value == expected
                 for value, expected in zip(actual, task)),
             "case_task_mismatch", f"Original typed task identity differs: {base}")
    _require(receipt.get("sha256") == digests[base + ".npz"],
             "case_receipt_sha_mismatch", f"Case receipt SHA256 differs: {base}")
    labels = {"trace", *(f"state_{year}" for year in CHECKPOINTS)}
    try:
        with archive.open(base + ".npz") as handle:
            with np.load(handle, allow_pickle=False) as saved:
                _require(len(saved.files) == len(labels) and set(saved.files) == labels,
                         "invalid_case_arrays", f"Expected exactly trace and four checkpoints: {base}")
                arrays = {label: saved[label] for label in labels}
                _require(all(isinstance(value, np.ndarray) for value in arrays.values()),
                         "invalid_case_arrays", f"Required NPZ members must all be NumPy arrays: {base}")
    except (ValueError, TypeError, KeyError, OSError, EOFError, BadZipFile, RuntimeError) as exc:
        raise _Rejected("invalid_case_arrays", f"Cannot safely read original arrays: {base}: {exc}") from exc
    trace = arrays["trace"]
    _require(trace.dtype.kind in "fiu" and trace.shape == (1001, 10),
             "invalid_case_arrays", f"Expected numeric 1001x10 trace: {base}")
    census = trace[:, 0]
    _require(np.isfinite(census).all() and (census >= 0).all() and
             (census <= capacity).all() and (census == np.floor(census)).all() and
             census[0] == capacity,
             "invalid_case_arrays", f"Invalid original ABM census: {base}")
    occupied = census > 0
    live = trace[occupied]
    _require(np.isfinite(live).all() and np.isnan(trace[~occupied, 1:]).all() and
             (live[:, 1:4] >= 0).all() and (live[:, 1:4] <= 1).all() and
             (live[:, 4:7] >= 0).all() and (live[:, 4:7] <= .25 + SUMMARY_ATOL).all() and
             (live[:, 7:] == np.floor(live[:, 7:])).all() and
             (live[:, 7:] >= 1).all() and (live[:, 7:] <= 2 * live[:, :1]).all(),
             "invalid_case_arrays", f"Invalid occupied/extinct trace summaries: {base}")
    for year in CHECKPOINTS:
        alleles = arrays[f"state_{year}"]
        n = int(census[year])
        _require(alleles.dtype.kind in "fiu" and alleles.shape == (n, 3, 2) and
                 np.isfinite(alleles).all() and (alleles >= 0).all() and (alleles <= 1).all(),
                 "invalid_case_arrays", f"Invalid diploid state_{year}: {base}")
        if n:
            # Same summary operations as the historical run_case writers;
            # no transition, founder generation, exposure generation, or RNG.
            traits = alleles.mean(axis=2)
            summaries = np.concatenate((traits.mean(axis=0), traits.var(axis=0)))
            unique = [len(np.unique(alleles[:, k])) for k in range(3)]
            _require(np.allclose(trace[year, 1:7], summaries, rtol=0, atol=SUMMARY_ATOL) and
                     np.array_equal(trace[year, 7:], unique),
                     "checkpoint_summary_mismatch", f"state_{year} disagrees with trace: {base}")


def _report(archive):
    return {
        "schema": "chapter2_discovery_archive_intake_v1",
        "status": "ARCHIVE_UNAVAILABLE",
        "archive": str(archive),
        "trust_anchor": {
            "receipt_path": RECEIPT, "receipt_sha256": RECEIPT_SHA256,
            "design_path": DESIGN, "design_sha256": DESIGN_SHA256,
            "contract_files_verified": False,
        },
        "verification": {
            "archive_identity_verified": False,
            "manifest_complete": False,
            "embedded_sources_verified": False,
            "discovery_endpoints_complete": False,
            "original_discovery_full_replay_completed": False,
            "runtime_identity_verified": False,
        },
        "counts": {
            "zip_members_verified": 0,
            "manifest_records_verified": 0,
            "embedded_sources_verified": 0,
            "discovery_cases_verified": 0,
            "genome_checkpoints_verified": 0,
        },
        "coverage": {
            "mutation_rates_verified": [], "mutation_zero_covered": False,
            "discovery_cases_expected": 2048, "archive_cases_expected": 13312,
        },
        "checkpoint_summary_absolute_tolerance": SUMMARY_ATOL,
        "limitations": [
            "Admission covers original positive-mutation discovery endpoints only; mutation zero remains missing.",
            "No annual genomes, selection, parentage, or biological RNG replay are produced.",
            "The packing recipe omits original campaign sources.json/sources.zip, the full-mutation runner, and a frozen numerical runtime lock.",
            "Embedded source byte verification does not establish the executed original sources or runtime identity.",
        ],
        "failures": [],
    }


def audit_archive(archive: Path):
    """Return a machine-readable intake result, including for missing input."""
    archive = Path(archive)
    report = _report(archive)
    try:
        plan, receipt = _load_contract()
        report["trust_anchor"]["contract_files_verified"] = True
        case_paths, endpoints = _case_contract(plan)
        _require(len(case_paths) == 2 * receipt["cases"], "frozen_contract_mismatch",
                 "Frozen archive receipt and plan disagree on case count")
        report["coverage"].update(discovery_cases_expected=len(endpoints),
                                  archive_cases_expected=receipt["cases"])
        identity = report["archive_identity"] = {
            "expected_bytes": receipt["bytes"], "expected_sha256": receipt["sha256"],
            "observed_bytes": None, "observed_sha256": None,
        }
        try:
            _require(stat.S_ISREG(archive.stat().st_mode), "archive_unavailable",
                     f"Archive must be a regular file: {archive}")
            handle = archive.open("rb")
        except OSError as exc:
            raise _Rejected("archive_unavailable", f"{archive}: {exc}") from exc
        with handle:
            before = os.fstat(handle.fileno())
            size, sha256 = _digest(handle)
            identity.update(observed_bytes=size, observed_sha256=sha256)
            _require(size == receipt["bytes"] and sha256 == receipt["sha256"],
                     "archive_identity_mismatch", "Archive bytes differ from the fixed external receipt")
            report["verification"]["archive_identity_verified"] = True
            handle.seek(0)
            with ZipFile(handle) as contents:
                digests = _verify_manifest(contents, receipt, case_paths, report)
                _verify_sources(contents, plan, digests, report)
                for base, task in endpoints.items():
                    _verify_endpoint(contents, base, task, digests, plan["plant_capacity"])
            after = os.fstat(handle.fileno())
            _require((before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
                     (after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                     "archive_changed_during_read", "Archive changed while intake was reading it")
        report["verification"]["discovery_endpoints_complete"] = True
        report["counts"]["discovery_cases_verified"] = len(endpoints)
        report["counts"]["genome_checkpoints_verified"] = len(endpoints) * len(CHECKPOINTS)
        report["coverage"]["mutation_rates_verified"] = [.01]
        report["status"] = STATUS
    except _Rejected as exc:
        _reject_report(report, exc.code, str(exc))
    except (BadZipFile, OSError, ValueError, RuntimeError, EOFError, NotImplementedError) as exc:
        _reject_report(report, "archive_read_error", str(exc))
    return report


def _reject_report(report, code, detail):
    report["status"] = "ARCHIVE_UNAVAILABLE" if code == "archive_unavailable" else "ARCHIVE_INTAKE_REJECTED"
    report["verification"]["discovery_endpoints_complete"] = False
    report["counts"]["discovery_cases_verified"] = 0
    report["counts"]["genome_checkpoints_verified"] = 0
    report["coverage"]["mutation_rates_verified"] = []
    report["failures"].append({"code": code, "detail": detail})


def _aliases(archive, out):
    if archive.resolve() == out.resolve():
        return True
    try:
        return archive.samefile(out)
    except FileNotFoundError:
        return False


def _protect_output(archive, out):
    for source, code in (
        (archive, "output_aliases_archive"),
        (ROOT / DESIGN, "output_aliases_trust_anchor"),
        (ROOT / RECEIPT, "output_aliases_trust_anchor"),
    ):
        _require(not _aliases(source, out), code,
                 f"Report output aliases protected input {source}; no file was written")


def _write_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(json.dumps(report, indent=2, allow_nan=False) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    report = _report(args.archive)
    try:
        _protect_output(args.archive, args.out)
        report = audit_archive(args.archive)
        _protect_output(args.archive, args.out)
        _write_report(args.out, report)
    except _Rejected as exc:
        _reject_report(report, exc.code, str(exc))
    except (OSError, RuntimeError) as exc:
        _reject_report(report, "report_write_failed", str(exc))
    print(json.dumps(report, sort_keys=True, allow_nan=False))
    return 0 if report["status"] == STATUS else 2


if __name__ == "__main__":
    raise SystemExit(main())
