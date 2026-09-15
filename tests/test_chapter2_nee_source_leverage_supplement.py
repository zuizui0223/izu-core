from pathlib import Path

from scripts.build_chapter2_nee_source_leverage_supplement import OUT, build


def test_source_leverage_supplement_matches_frozen_diagnostics() -> None:
    committed = OUT.read_text(encoding="utf-8")
    regenerated = build()
    assert committed == regenerated

    lower = committed.lower()
    for required in (
        "england step / great britain | 39 | 6.199 | 0.162 | 0.231 | 0.193 | no",
        "martinique (cyrille 2025) | 32 | 2.883 | 0.352 | 0.188 | 0.358 | no",
        "all four candidates closed before d1 or phi extraction",
        "no numerical d1-to-k or d1-to-k_eff mapping is estimated or used",
        "source-complementary rather than leave-any-source-out invariant",
        "great britain retains the pre-existing euppollnet island-study classification",
        "no candidate values were available for selection",
    ):
        assert required in lower

    assert lower.count("| no |") >= 6  # 2 failed LOO rows + 4 unopened candidates
    assert Path(OUT).name == "CHAPTER2_NEE_SUPPLEMENTARY_SOURCE_LEVERAGE_20260915.md"
