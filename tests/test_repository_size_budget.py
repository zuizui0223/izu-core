from __future__ import annotations

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]

# Existing large-file debt at reviewed HEAD 54db0b79. These files may shrink or
# be removed, but they must not grow. New oversized paths are not grandfathered.
GRANDFATHERED_MAX_BYTES = {
    "data/results/model3_assurance_summary_20260925/endpoints.csv.gz": 18_715_386,
    "data/design/model3_assurance_robustness_20260925.json": 14_791_554,
    "data/design/model3_evolution_20260925.json": 10_181_145,
    "data/results/model3_evolution_summary_20260925/endpoints.csv.gz": 9_488_521,
    "data/results/model3_ch2_bridge_summary_20260927/case_receipts.csv": 6_957_008,
    "data/results/model3_island_v2_summary/case_receipts.csv": 5_057_905,
    "data/design/model3_grid_comparison_20260925.json": 1_096_302,
    "data/results/model3_island_v2_summary/production-life_perennial10_annual.svg": 2_116_623,
    "data/results/model3_island_v2_summary/production-life_perennial10_lifetime.svg": 1_914_676,
    "data/results/model3_island_v2_summary/production-life_perennial4_lifetime.svg": 1_237_339,
    "data/results/model3_island_v2_summary/production-life_perennial4_annual.svg": 1_223_302,
    "data/results/model3_island_v2_summary/production-scale_fixed_total_768.svg": 1_216_189,
    "data/results/model3_island_v2_summary/production-scale_per_capita_768.svg": 1_215_017,
    "data/results/model3_island_v2_summary/production-scale_per_capita_192.svg": 1_167_859,
    "data/results/model3_island_v2_summary/production-scale_fixed_total_192.svg": 1_132_029,
}

GENERAL_LIMIT = 5_000_000
DESIGN_LIMIT = 1_000_000
SVG_LIMIT = 1_000_000


def _tracked_paths() -> list[str]:
    out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [p.decode("utf-8") for p in out.split(b"\0") if p]


def test_tracked_files_do_not_expand_submission_size_debt() -> None:
    failures: list[str] = []
    for rel in _tracked_paths():
        path = ROOT / rel
        if not path.is_file():
            continue
        size = path.stat().st_size

        ceiling = GRANDFATHERED_MAX_BYTES.get(rel)
        if ceiling is not None:
            if size > ceiling:
                failures.append(f"{rel}: {size} > grandfathered ceiling {ceiling}")
            continue

        if rel.startswith("data/design/") and size > DESIGN_LIMIT:
            failures.append(f"{rel}: design payload {size} > {DESIGN_LIMIT}")
            continue
        if rel.endswith(".svg") and size > SVG_LIMIT:
            failures.append(f"{rel}: tracked SVG {size} > {SVG_LIMIT}")
            continue
        if size > GENERAL_LIMIT:
            failures.append(f"{rel}: tracked file {size} > {GENERAL_LIMIT}")

    assert not failures, "new repository size debt:\n" + "\n".join(failures)
