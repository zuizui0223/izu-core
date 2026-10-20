# Chapter 2 — visual verification of six source-bound figures (2026-10-21)

**Status: editorial QC and non-biological drawing corrections only.** Figures remain source-linked SVG *drafts*; this does not certify journal artwork or reproducibility beyond existing figure/source-value tests.

## What was examined

- The current completed-evidence 18-page author-review PDF generated from the exact PR #615 author-review source package: 12 portrait text pages followed by six landscape SVG-vector figure plates.
- Each plate was inspected separately at 2× page-size rendering in addition to a two-sheet 18-page montage. Text/figure page boundaries, page numbering and selectable SVG text were checked. Figures 1, 3 and 6 were structurally readable; Figures 2, 4 and 5 required targeted typographic corrections.
- Figure 2: Unicode minus/arrow glyphs rendered as missing-glyph boxes in some PDF viewers. SVG text uses font-safe ASCII hyphens and “to” for numerical comparisons. Underlying values and bar geometry are unchanged.
- Figure 4: The note describing green/orange/gray states overlapped the last row. Its baseline is now y=1013, leaving more than 25 SVG units after the last bar and at least 20 before the next panel. The note is scientifically clarified: orange denotes a living target-closed state, **not a population that failed a restoration experiment**. The registered G/S intervals, all 12 original all-start categories, layout bar lengths and source-bind metadata are untouched.
- Figure 5: Unicode minus in the subtitle changed to font-safe ASCII for PDF readability. The conditional-duration values, uncertainty intervals and competing-extinction notes remain unchanged.
- Figure 6: Changed the title from “limits to adaptation” to **“distinguishes inherited support and response”** because survival and survivor-conditioned reproductive return do not constitute a test of realised adaptation. Numeric marks and cohort denominators are unchanged.

## Machine-checkable guards

- `tests/test_chapter2_figure_visual_readability_20261021.py`: checks font-safe labels, Figure 4 clearance using the actual bar y-coordinates, accurate state terminology, and Figure 6 non-adaptation title.
- Existing `tests/test_chapter2_paper_figures_20261019.py`: maintains exact SVG data-kind/metadata comparisons against registered and exploratory readouts. These checks are necessary for source integrity but do not substitute for final human visual inspection.
- New author-review archive is regenerated from committed files by `scripts/build_chapter2_current_author_review_20261020.py` (not by repackaging the obsolete EL ZIP).

## Open publication artwork gates

1. Confirm symbol legibility at the journal's final physical print size: Figure 4 has dense labels, and its smallest tick text can fall below 6 pt on a landscape A4 plate. Source-value correctness does not justify marking such text publication-final.
2. Review grayscale/colour-vision accessibility and consistency of panel typography across all six main figures; plotted numeric data must not be moved while adjusting graphical layout.
3. Check the final, revised PDF plates after CI re-export and do not reuse the previous author-review PDF with missing-glyph labels.
4. Keep the source metadata, uncertainty labels, registered vs exploratory distinctions and four independent 160-founder/visitor source axes statements intact.

No new simulations, biological predictions, significance results or retrospective endpoint changes were performed.
