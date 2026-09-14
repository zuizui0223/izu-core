from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_2_20260915.md"
WORD_RE = re.compile(r"\b[\w’'\-]+\b", re.UNICODE)


def section(text: str, start: str, end: str | None) -> str:
    marker = f"## {start}"
    if marker not in text:
        raise RuntimeError(f"missing section: {marker}")
    body = text.split(marker, 1)[1]
    if end is not None:
        end_marker = f"## {end}"
        if end_marker not in body:
            raise RuntimeError(f"missing section: {end_marker}")
        body = body.split(end_marker, 1)[0]
    return body.strip()


def word_count(text: str) -> int:
    # Conservative Markdown count: formulas and headings inside the selected
    # section remain countable tokens rather than being silently excluded.
    return len(WORD_RE.findall(text))


def audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    abstract = section(text, "Abstract", "Results")
    # The working markdown keeps the unheaded NEE introduction between
    # Abstract and Results, so main text is everything after Abstract through
    # immediately before Methods. Remove only the abstract body itself.
    after_abstract = text.split("## Abstract", 1)[1]
    if "## Methods" not in after_abstract:
        raise RuntimeError("missing section: ## Methods")
    abstract_and_main = after_abstract.split("## Methods", 1)[0]
    abstract_body = abstract
    main_text = abstract_and_main.replace(abstract_body, "", 1)

    abstract_words = word_count(abstract_body)
    main_text_words = word_count(main_text)
    result = {
        "manuscript": str(path),
        "abstract_words": abstract_words,
        "abstract_limit": 200,
        "abstract_pass": abstract_words <= 200,
        "main_text_words_conservative": main_text_words,
        "main_text_limit": 3500,
        "main_text_pass": main_text_words <= 3500,
        "display_items_planned": 4,
        "display_items_limit": 6,
        "display_items_pass": 4 <= 6,
        "counting_rule": "regex word count; text after Abstract through immediately before Methods, with abstract body removed; formulas/headings counted conservatively",
    }
    result["pass"] = all(
        (result["abstract_pass"], result["main_text_pass"], result["display_items_pass"])
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", type=Path, default=DEFAULT_MANUSCRIPT)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit(args.manuscript)
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    if args.check and not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
