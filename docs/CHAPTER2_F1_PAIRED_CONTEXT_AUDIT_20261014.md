# Retrospective paired-context F1 access audit (2026-10-14)

## Exact source and experimental unit

This is an additive, read-only analysis of the existing **2,304 original Model3 case-level genotype-derived summaries** already admitted in #491/S20; it is **not a new simulation**, a new independently pre-registered experiment, or an additional independent biological system. The single CSV input is pinned to Git blob **ea2c4009fc77cc59813dda0142e8da73c33a26fd**. Its original nine ZIP/genome and event reconstruction provenance remains in the existing first-meiosis access receipt.

The design has two founder genotype backgrounds and nine visitor settings (18 fixed cells), with 128 matched replicate-stream IDs per founder. The unit for the paired comparison is the **256 founder × replicate clusters**, each appearing under all nine visitor settings. Counting the resulting 2,304 rows as independent ecological replicates would be pseudoreplication.

## Newly checked exact descriptive pattern

| Paired source question | Result |
|---|---:|
| Full source-labelled cases represented | 2,304/2,304 |
| Matched founder × replicate clusters containing all nine settings | 256/256 |
| Seven recorded F1 A fields identical across nine settings within cluster | **256/256** |
| Six-class sustained order category differs in at least one setting | **255/256** |
| Sustained A-event incidence differs across settings within cluster | **191/256** |
| Sustained I-event incidence differs across settings within cluster | **252/256** |
| F1 offspring with no flagged A mutation at all | 864/2,304 |

The **seven identical F1 summary fields** are: first-offspring population count, initial expressed A variance, first-offspring expressed A variance, first-offspring individual A-threshold support, number of flagged A-mutant offspring, unmutated-individual A-threshold support, and first-offspring mean A change. This is *exact equality of the original CSV text values*, not floating-point tolerance matching.

Number of different sustained six-class categories reached among the nine settings within one paired cluster: 1 category in **1** cluster, 2 in **12**, 3 in **52**, 4 in **125**, 5 in **63**, and all 6 in **3**. The only cluster retaining the same category in all nine settings is **confirmation_r115** (assurance only). For main founders, 128/128 paired clusters vary in category; for confirmation, 127/128 do.

The original six-category totals (335 A-first, 435 I-first, 358 tie, 895 A-only, 10 I-only, 271 neither) are **unchanged**. The threshold is still the original ±0.05 first response maintained for 20 occupied annual censuses, with the original near-simultaneous definition.

## What is demonstrated — and what is not

Within the *old fixed-access experiment*, first-offspring expressed A variance, early mean change and A-mutation counts are held identical in the stored summaries across the matched visitor settings, while long-run outcome categories often differ. Thus **the measured first-generation A-access summaries are insufficient by themselves to determine the long-run six-class outcome**. This is stronger documentation of the access-versus-realization distinction than the earlier all-histories-positive-F1 observation.

It does **not** show identical complete F1 all-locus genomes, equal early I states, equal parentage/reproductive returns, or identical stochastic futures. The visitor settings differ by design; stochastic selection, trait-specific feedback, later genotype evolution, fixation, mutation and censoring can all contribute. Hence this is **not** an isolation of an ecological causal mechanism or a selection-versus-drift variance decomposition, not proof of a universal genetic clock, and not a rescue/survival-order benefit test. It does not reverse the earlier Q1 finding that no predeclared replicated ecological order reversal was supported.

There is no new significance test, interval, model fitting, outcome-dependent threshold tuning, or alteration of the four-question manuscript's primary decision. The new 1,536-case genotype-access pilot reported in #506/#491 is **a different, later-run cohort**, not pooled into these 2,304 old histories. Earlier frozen F1 historical notes that described that pilot as not-yet-executed reflect their original creation time, not the present scientific inventory.

## Replay and regression gate

Run from the #491-derived source tree:

    python scripts/audit_chapter2_f1_paired_context_20261014.py
    python -m pytest -q tests/test_chapter2_f1_paired_context_20261014.py

The script rejects source-blob drift, incomplete/duplicated 2×9×128 cases, counterfeited first-offspring access flags, six-category/onset inconsistencies, and a broken within-pair F1 signature. Regression tests require all paired and global counts above to reproduce. The original 2,304 raw genome ZIPs need not be re-downloaded **for this summary-level test**; their prior independent original-genome source admission is a separate prerequisite. Passing this test must not be described as a second raw-genome replay.

**Scope:** exploratory, post-outcome, deterministic source-locked descriptive negative-control. Maintains #491 as draft until its separate full CI and scientific review gates complete.
