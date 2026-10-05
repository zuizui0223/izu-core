"""Render the current process manuscript without repository routing metadata.

The older Oikos renderer deliberately reproduces the historical bridge snapshot.
This renderer performs document-structure checks, not scientific verification.
"""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md'
TITLE = 'How island isolation generates floral change: selection conditions, evolutionary sequence and finite realization'


def render_manuscript(source: Path | None = None) -> str:
    text = (SOURCE if source is None else source).read_text(encoding='utf-8')
    for section in ['## Abstract','## Keywords','# Introduction','# Materials and Methods',
                    '# Results','# Discussion','# Conclusion','# Primary figure assembly and captions','# References']:
        if text.splitlines().count(section) != 1:
            raise ValueError(f'missing required section or duplicate: {section}')
    if text.splitlines()[0] != '# ' + TITLE:
        raise ValueError('Current process manuscript title does not match its route')
    body = text[text.index('## Abstract'):].strip()
    return '# ' + TITLE + '\n\n' + body + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'outputs/chapter2_process_delivery/MANUSCRIPT.md')
    args = parser.parse_args()
    text = render_manuscript()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(text,encoding='utf-8')
    print(args.output)


if __name__ == '__main__':
    main()
