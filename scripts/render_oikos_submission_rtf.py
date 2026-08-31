from __future__ import annotations

import re
from pathlib import Path

from scripts.render_chapter2_supporting_information import render_supporting_information
from scripts.render_island_ecology_submission_manuscript import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANUSCRIPT = ROOT / "dist/MANUSCRIPT.rtf"
DEFAULT_SUPPORTING_INFORMATION = ROOT / "dist/SUPPORTING_INFORMATION.rtf"


def _rtf_escape(text: str) -> str:
    out: list[str] = []
    for char in text:
        code = ord(char)
        if char in "\\{}":
            out.append("\\" + char)
        elif char == "\t":
            out.append("\\tab ")
        elif 32 <= code <= 126:
            out.append(char)
        elif char == "\n":
            out.append("\n")
        else:
            signed = code if code < 32768 else code - 65536
            out.append(f"\\u{signed}?")
    return "".join(out)


def _plain_markdown(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    return text


def _paragraph(line: str, *, bold: bool = False, size: int = 24) -> str:
    clean = _rtf_escape(_plain_markdown(line.strip()))
    controls = f"\\pard\\ql\\sl480\\slmult1\\fs{size}"
    if bold:
        return f"{controls}\\b {clean}\\b0\\par\n"
    return f"{controls} {clean}\\par\n"


def _table_line(line: str) -> str | None:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return None
    return "\t".join(cells)


def markdown_to_oikos_rtf(text: str, *, introduction_page_two: bool) -> str:
    header = (
        "{\\rtf1\\ansi\\deff0\\uc1\n"
        "{\\fonttbl{\\f0 Times New Roman;}{\\f1 Courier New;}}\n"
        "\\paperw11907\\paperh16840\\margl1440\\margr1440\\margt1440\\margb1440\n"
        "\\sectd\\linemod1\\linex360\\linecont\n"
        "{\\footer\\pard\\qr\\fs20 Page {\\field{\\*\\fldinst PAGE}{\\fldrslt 1}}\\par}\n"
    )
    parts: list[str] = [header]
    intro_break_inserted = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            parts.append("\\pard\\ql\\sl480\\slmult1\\fs24\\par\n")
            continue

        if line.startswith("# "):
            heading = line[2:].strip()
            if introduction_page_two and heading == "Introduction" and not intro_break_inserted:
                parts.append("\\page\n")
                intro_break_inserted = True
            parts.append(_paragraph(heading, bold=True, size=30))
        elif line.startswith("## "):
            heading = line[3:].strip()
            if introduction_page_two and heading == "Introduction" and not intro_break_inserted:
                parts.append("\\page\n")
                intro_break_inserted = True
            parts.append(_paragraph(heading, bold=True, size=26))
        elif line.startswith("### "):
            parts.append(_paragraph(line[4:].strip(), bold=True, size=24))
        elif line.startswith("- "):
            parts.append(_paragraph("• " + line[2:].strip(), size=24))
        elif line.startswith("|") and line.endswith("|"):
            table_text = _table_line(line)
            if table_text is not None:
                parts.append(_paragraph(table_text, size=22))
        else:
            parts.append(_paragraph(line, size=24))

    if introduction_page_two and not intro_break_inserted:
        raise ValueError("Introduction heading not found; cannot enforce page-two Introduction")
    parts.append("}\n")
    return "".join(parts)


def render_manuscript_rtf() -> str:
    return markdown_to_oikos_rtf(render_submission_manuscript(), introduction_page_two=True)


def render_supporting_information_rtf() -> str:
    return markdown_to_oikos_rtf(render_supporting_information(), introduction_page_two=False)


def render_plain_text_rtf(text: str) -> str:
    return markdown_to_oikos_rtf(text, introduction_page_two=False)


def write_submission_rtf(
    manuscript_path: Path = DEFAULT_MANUSCRIPT,
    supporting_path: Path = DEFAULT_SUPPORTING_INFORMATION,
) -> tuple[Path, Path]:
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)
    supporting_path.parent.mkdir(parents=True, exist_ok=True)
    manuscript_path.write_text(render_manuscript_rtf(), encoding="utf-8")
    supporting_path.write_text(render_supporting_information_rtf(), encoding="utf-8")
    return manuscript_path, supporting_path


if __name__ == "__main__":
    for path in write_submission_rtf():
        print(path)
