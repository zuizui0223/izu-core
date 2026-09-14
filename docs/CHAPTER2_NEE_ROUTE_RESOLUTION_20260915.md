# Chapter 2 NEE route resolution — 2026-09-15

Status: **active route resolution**. This file resolves the journal-selection deferral in `docs/CHAPTER2_COMBINED_NEE_SUPERSESSION_20260913.md` without changing any frozen scientific threshold or admission rule.

## Decision

The combined theory + nonlinear demonstration + natural-regime placement + identifiability-audit manuscript is promoted to a **Nature Ecology & Evolution Article candidate** under the predeclared natural-regime routing rule.

The decision is mechanical, not editorially guaranteed. `NEE_candidate` means that the repository-defined promotion ceiling has been reached; it does not mean that *Nature Ecology & Evolution* will accept the manuscript.

## Frozen evidence for promotion

The primary natural plane contains 42 systems from six independent source studies and five island/archipelago groups. The frozen six-source classifier returns `NEE_candidate`:

- source-balanced `D1` q90/q10 = 4.5213 (required >=2.0);
- source-balanced `phi` q90-q10 span = 0.3516 (required >=0.20);
- absolute source-balanced Spearman(`log D1`, `phi`) = 0.3253 (required <=0.80);
- joint-interior occupancy = 0.2619 (required >=0.20).

The formal source-robustness rule also passes after removal of the largest source study, Mallorca:

- 23 systems / five studies / five island groups remain;
- `D1` q90/q10 = 5.4944;
- `phi` span = 0.3516;
- interior occupancy = 0.2609;
- absolute Spearman = 0.4539.

The candidate search is closed under the predeclared early-stop rule. No unresolved or later-discovered source may be added to improve the primary-plane route metrics without prospectively reopening a different analysis.

## Post-promotion transparency diagnostics

The route criterion required removal of the single largest source, not universal leave-one-source-out success. A later all-source diagnostic is therefore reported as sensitivity evidence rather than a retroactive gate.

Two sensitivities fail the NEE numerical dispersion set:

- removing England STEP reduces `phi` span to 0.1619;
- removing Martinique reduces joint-interior occupancy to 0.1875.

These results do not undo the frozen route decision. They define the natural evidence ceiling: high-synchrony coverage is currently source-dependent and interior coverage is not fully redundant across studies. The manuscript must state this limitation explicitly and must not describe the natural plane as robust to removal of every source.

## England STEP validation

The three admitted England systems were fixed before their coordinates were opened using a source-native 4+4 survey schedule and constant 30-minute / 300-m2 effort. An independent implementation reproduced every committed `D1` and `phi` value exactly (`delta = 0`). Positive-bin-only synchrony diagnostics remained high, so the high-synchrony edge is not a zero-interaction-bin artefact.

## Active manuscript surface

Submission-clean primary draft:

`docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_3_SUBMISSION_20260915.md`

Submission-clean cover letter:

`docs/CHAPTER2_NEE_COVER_LETTER_DRAFT_V0_3_SUBMISSION_20260915.md`

Source-verified reference ledger:

`docs/CHAPTER2_NEE_REFERENCE_LEDGER_20260915.md`

The v0.2 manuscript and earlier Ecology Letters/Oikos surfaces remain archived scientific provenance and internal routing history. They are not the active submission files while this resolution is in force.

## Retained claim boundaries

- natural Hill `D1` is not synthetic `k`;
- natural data do not retune the synthetic mechanism;
- the 42-system plane does not validate the synthetic `C/I` crossover in nature;
- the internal NEE promotion thresholds are not biological thresholds;
- the frozen 25-entry identifiability audit remains 21/25 direct comparable responses, 2/25 direct arrival/replacement and 0/25 full contracts;
- unresolved/unavailable data remain unavailable evidence, not biological negatives;
- Great Britain retains the source compilation's pre-existing island-study classification and is not reclassified from its route effect.
