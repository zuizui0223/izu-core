from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"


def test_active_manuscript_is_compact_but_keeps_confirmed_core():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    body = text[text.index("## Abstract"): text.index("# References")]
    words = body.split()

    assert len(words) <= 5500
    assert "## Abstract" in body
    assert "5. **Synthesis.**" in body

    normalized = " ".join(body.split())
    assert "51/64" in normalized
    assert "0.6875–0.8906" in normalized
    assert "−0.3060" in normalized
    assert "−0.4354" in normalized
    assert "30/64" in normalized
    assert "sequence does not identify necessity" in normalized.lower()
    assert "assurance evolution is not required" in normalized.lower()


def test_secondary_model_families_are_not_restored_as_main_result_sections():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    results = text[text.index("# Results"): text.index("# Discussion")]

    assert "## Realized evolution across continuous replenishment" not in results
    assert "## Reciprocal coupling of selection on capacity and investment" not in results
    assert "## Genetic diversity, fitness and model scope" not in results
    assert "## Supporting analyses define mechanism and claim boundaries" in results


def test_primary_scope_remains_explicit_after_compression():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    normalized = " ".join(text.split()).lower()

    assert "delayed-selfing, assurance-cost 0.5" in normalized
    assert "prior selfing with positive mutation" in normalized
    assert "not universal" in normalized
    assert "64 entirely new visitor histories" in normalized
    assert "eight new nested demographic repeats" in normalized
