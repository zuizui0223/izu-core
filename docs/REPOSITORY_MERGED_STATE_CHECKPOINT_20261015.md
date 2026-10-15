# Izu Core — merged-state checkpoint (2026-10-15)

**Fixed baseline:** `main` commit [`c1b08577dd2a2432ce71df001df45a90ad0f0d74`](https://github.com/zuizui0223/izu-core/commit/c1b08577dd2a2432ce71df001df45a90ad0f0d74), read from the live GitHub repository on 2026-10-15. This page records a **dated snapshot**, not a permanently live PR dashboard. Future edits or new branches must be checked again before decisions. No numerical experiment, biological implementation, raw data, or manuscript is modified by this record.

## Scientific source of truth: one Chapter 2 paper

| Check | Exact mainline observation | Canonical source |
| --- | --- | --- |
| Active manuscript | **One** Ecology Letters-format Chapter 2 manuscript; route status `active_unified_manuscript_not_submitted` | [One-paper route](../data/design/chapter2_one_paper_route_20261010.json) |
| Word budget | **4,944 whitespace-delimited main text / 5,000 limit**; **147-word abstract / 150 limit** (both independently recounted from current source and identical to route) | [Working manuscript](CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md) |
| Supporting Information | **S1–S33 exactly once**; **S30** mutation-renewal, **S31** finite birth accounting, **S32** original-genome Price checkpoint, **S33** independent 32-history Q4 persistence | [Current SI](CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md) |
| Distinct inference families | Q1 reproductive returns; Q2 sequence and genetic access; Q3 finite realization; Q4 independently controlled persistence. **Not** a single confirmed historical Q1→Q4 mediation path | [Manuscript](CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md), [Q3 source map](CHAPTER2_Q3_SELECTION_REALIZATION_SOURCE_MAP_20261015.md) |
| Reviewer provenance | Q4A design, original result, replay receipt and original runner included as source-checked inputs by the anonymous review package builder following merged PR #546; not a journal acceptance or original raw-archive DOI | [Builder](../scripts/build_chapter2_unified_el_submission_bundle.py), [Q4 reviewer admission guard](../tests/test_chapter2_q4_independent32_review_source_20261015.py) |
| Default CI | `.github/workflows/ci.yml` **39 lines**, active three-version Python 3.10/3.11/3.12 `pytest -q` job only; separate Chapter 2 scientific gate unchanged | [General CI](../.github/workflows/ci.yml), [scientific gate](../.github/workflows/chapter2-scientific-gate.yml), [original PR #420 job provenance](CI_PR420_RETIRED_JOB_PROVENANCE_20261015.md) |

The recent [novelty/asymmetry source review](CHAPTER2_NOVELTY_ASYMMETRY_GATE_20261015.md) preserves the distinction between positive *relative* far-side E−F investment and still negative far-side evolution from the founder. It is not proof of the complete historical mechanism, a global originality priority claim, or measured natural-island change.

## PR consolidation: closed/open at this checkpoint

**0 open PRs** were returned by the GitHub `pulls?state=open` endpoint at this baseline. The following were **merged** (source changes and dated cleanup entries): [#529](https://github.com/zuizui0223/izu-core/pull/529), [#535](https://github.com/zuizui0223/izu-core/pull/535), [#540](https://github.com/zuizui0223/izu-core/pull/540), [#541](https://github.com/zuizui0223/izu-core/pull/541), [#542](https://github.com/zuizui0223/izu-core/pull/542), [#543](https://github.com/zuizui0223/izu-core/pull/543), [#544](https://github.com/zuizui0223/izu-core/pull/544), [#545](https://github.com/zuizui0223/izu-core/pull/545), [#546](https://github.com/zuizui0223/izu-core/pull/546), [#547](https://github.com/zuizui0223/izu-core/pull/547), [#549](https://github.com/zuizui0223/izu-core/pull/549).

Legacy overlapping paper drafts [#536](https://github.com/zuizui0223/izu-core/pull/536), [#537](https://github.com/zuizui0223/izu-core/pull/537), [#538](https://github.com/zuizui0223/izu-core/pull/538) are **closed without merge**; the original Q3 source-level quantities and tests were separately preserved in the merged primary plus #543, and selected S30–S32 readers and Q4 evidence in #542/#544/#546. Their distinct original branches, historical text and Git objects must not be silently deleted. Earlier [PR consolidation audit](PR_CONSOLIDATION_AUDIT_20261015.md) is a **historical overlap/decision log** and contains an obsolete “open PRs” table; consult this checkpoint for the later verified disposition.

## External source deposit is still not finished

The new [Q3/Q4 raw-source addendum](deposit/CHAPTER2_SINGLE_PAPER_RAW_SCOPE_ADDENDUM_20261015.md) and [machine-readable inventory](deposit/chapter2_single_paper_raw_scope_addendum_20261015.json) list **10 known candidate original containers**: six preflight core, two previously documented candidates, plus Q3 original 2,304-history genomes/pedigrees and Q4 separate 32-history stress source. **This is explicitly NOT a complete S1–S33 source inventory or a created/public external DOI deposit.** The original Q3 released ZIP size/hash were corroborated using live GitHub Release asset metadata; its 251 MB contents were **not re-downloaded** in that check. The Q4 original candidate is not claimed public.

[Data deposit Issue #436](https://github.com/zuizui0223/izu-core/issues/436) remains **open**: finish exact full-SI archive coverage, check original data-owner/licensing/access decisions, protect the private provider safety stop and obtain independent cross-host full-byte verification before any public DOI or Data Availability claim.

## Branch inventory and safe deletion boundary

The GitHub paginated branch endpoint returned **500 unique branch names** across **five full pages of 100**, followed by an empty sixth page. Prefix inventory: `codex/` **160**, `agent/` **140**, `chapter2/` **61**, `analysis/` **53**, all other prefixes (including `main`) **86**. This is a **count only**, not 500 duplicative or disposable research branches. At the baseline there were **zero protected branches**, including `main.protected=false`.

[Branch-protection / archival-ref Issue #548](https://github.com/zuizui0223/izu-core/issues/548) remains **open**. Before any prune, require main rules/required checks, original-receipt and release/tag SHA reachability, unique-commit comparisons, and a source-preservation plan. A squash-merged PR branch can still contain unique historical commit objects; **closed PR is not a deletion criterion**. No ref deletion, branch force-push, source-file relocation or experimental recreation was performed in this status audit.

## Immediate next work

1. **Preserve exact scientific/source states:** keep one manuscript, distinct Q1–Q4 cohorts, negative and unidentifiable results, 33 SI sections and the verified reviewer ZIP. Recheck branch SHA before changing the paper or archive.
2. **Resolve raw-data coverage/authorization:** expand 10 candidate archives to a complete SI evidence registry, then seek legitimate deposition approvals and cross-host re-download; keep #436 open until finished.
3. **Secure refs before branch pruning:** enable rules for `main`, establish branch/tag/release reachability and protect unique original experiment objects through #548; do not delete based on age/name alone.

The repository is **consolidated at the PR layer** as of this specific commit. Scientific interpretation and durable external provenance still require separate evidence, and neither has been made stronger by housekeeping.
