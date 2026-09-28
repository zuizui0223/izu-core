# Chapter 2 NEE submission render v0.4 — 2026-09-15

Status: **layout-only submission surface**. This file does not alter any frozen analysis, source membership, route metric, audit denominator or manuscript claim boundary.

## Purpose

Visual QA of the initial-submission Word manuscript showed that the long categorical labels in Figure 4 collided when the original v0.3 figure was embedded at manuscript width. The underlying values and logic were correct; the defect was purely presentational.

For the v0.4 submission surface, `scripts/render_chapter2_nee_v04_submission_figures.py` therefore retains Figures 1–3 exactly through the frozen v0.3 renderer and redraws Figure 4 only.

## Figure 4 invariants

The submission redraw preserves exactly:

- frozen denominator: **25** research entries;
- directly comparable plant response: **21/25**;
- direct partner arrival/replacement: **2/25**;
- complete outcome-independent determinant–response contract: **0/25**;
- the same source-state → transition/filtering → realized-community → plant-response measurement chain;
- the same statement that the 42-system regime map estimates context but does not add matched outcomes.

The only graphical change is to render the three audit counts as horizontal bars with wrapped labels so they remain readable at journal-manuscript width.

## Provenance rule

The original `scripts/render_chapter2_nee_v03_figures.py` remains unchanged as scientific provenance. The v0.4 submission renderer is an additive presentation layer. No result may be recomputed, selected or reinterpreted from the layout change.
