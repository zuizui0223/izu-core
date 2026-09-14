from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_2_20260915.md"
WORD_RE = re.compile(r"\b[\w’'\-]+\b", re.UNICODE)


def word_count(text: str) -> int:
    # Conservative Markdown count: formulas and headings inside the selected
    # section remain countable tokens rather than being silently excluded.
    return len(WORD_RE.findall(text))


def split_abstract_and_main(text: str) -> tuple[str, str]:
    marker = "## Abstract"
    if marker not in text:
        raise RuntimeError(f"missing section: {marker}")
    after = text.split(marker, 1)[1].lstrip()
    if "## Methods" not in after:
        raise RuntimeError("missing section: ## Methods")
    pre_methods = after.split("## Methods", 1)[0].rstrip()
    # NEE Articles use an unheaded introduction. In the working markdown the
    # abstract is therefore exactly the first paragraph after ## Abstract.
    parts = re.split(r"\n\s*\n", pre_methods, maxsplit=1)
    if len(parts) != 2:
        raise RuntimeError("could not separate abstract paragraph from unheaded main text")
    abstract, main_text = parts[0].strip(), parts[1].strip()
    return abstract, main_text


def audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    abstract, main_text = split_abstract_and_main(text)
    abstract_words = word_count(abstract)
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
        "counting_rule": "regex word count; abstract is first paragraph after ## Abstract; main text is all following text through immediately before ## Methods; formulas/headings counted conservatively",
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
