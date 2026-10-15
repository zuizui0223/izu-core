# Open-PR consolidation audit — 2026-10-15

## Final merged checkpoint — after #549 (replaces all older “open” labels below)

**Verified main `c1b08577dd2a2432ce71df001df45a90ad0f0d74` on 2026-10-15:** the GitHub endpoint returned **0 open PRs**. The paper/source/cleanup PRs **#529, #535, #540, #541, #542, #543, #544, #545, #546, #547 and #549 are merged**. Historical overlap/failed-template drafts **#536, #537 and #538 are closed without merge**, with original source checks preserved independently. All older statements on this page calling those PRs “open”, “pending” or “stacked” are preserved solely as **time-stamped decision provenance** and must not be treated as current instructions.

The [mainline checkpoint](REPOSITORY_MERGED_STATE_CHECKPOINT_20261015.md) records the source-linked one-paper status (4,944 main / 147 abstract words, S1–S33), the now three-version-only CI definition, incomplete 10-candidate external deposit inventory, and **500 distinct branch names with `main` unprotected**. The prior branch count **492** was accurate at an earlier snapshot, not a currently verified count. Neither 0 open PRs nor a squash merge proves unused branches are safe to delete. See [Issue #548](https://github.com/zuizui0223/izu-core/issues/548) for protection and archival reachability; [Issue #436](https://github.com/zuizui0223/izu-core/issues/436) remains open for independent external raw-data deposition. This update leaves every historical experimental SHA and null conclusion untouched.


## Integration checkpoint — later on 2026-10-15 (supersedes the open/closed labels below)

**Verified merged onto main**: [#535](https://github.com/zuizui0223/izu-core/pull/535) Q3/prior art at `fb8179a`, [#540](https://github.com/zuizui0223/izu-core/pull/540) exact original-genome Price accounting at `79bc570`, [#529](https://github.com/zuizui0223/izu-core/pull/529) original I-mutation renewal source at `d9403db`, and [#541](https://github.com/zuizui0223/izu-core/pull/541) navigation/index at `fa5ee7e`. Older rows recording them as open describe the first audit, **not current PR status**.

**Pending integration**: [#536](https://github.com/zuizui0223/izu-core/pull/536) is a mutable draft with unresolved mainline conflicts, containing Q1–Q4 narrative, Ch1 crosswalks and overlapping already-merged sources; **do not merge or force-update blindly**. [#542](https://github.com/zuizui0223/izu-core/pull/542) is a separately drafted **clean S30–S32 and source-accounting integration** against current main; keep exact-head scientific gate, Python CI and reviewer-package source validation before merging. Preserve #536's unique Ch1 crosswalk/other audited work until reconciliation.

**Source preservation from [#537](https://github.com/zuizui0223/izu-core/pull/537) / [#538](https://github.com/zuizui0223/izu-core/pull/538)**: their three-version manuscript/route edits are not safe to mass-merge. Original CI failures isolated an outdated exact *manuscript phrase* check in each branch, rather than establishing a numerical audit failure. The [Q3 source map](CHAPTER2_Q3_SELECTION_REALIZATION_SOURCE_MAP_20261015.md) and [read-only original-transition check](../tests/test_q3_original_finite_loss_transition_receipt_20261015.py) are proposed in this independent branch to preserve the unique 315/1,238, q0^48 and sex-specific accounting without imposing dated 4,869/4,961-word templates. This source-preservation PR must pass final-head CI **before** either superseded PR is considered safe to close. Its CI status is not pre-asserted in this ledger.

All original raw numerical receipts, original allele/genome files, negative outcomes, model laws and original registered intervention definitions remain authoritative. Nothing here asserts four-question causal mediation, new biological runs or completed DOI/journal submission.


**Read-only inventory / proposed integration order.** This page records observed repository state and SHA comparisons, not a decision to merge, close, rebase, delete or promote claims. Baseline: `main` at `a412b456b435f10dd9c71014b53f3e1f37634b41`. Re-fetch PR metadata and exact heads before performing an action: concurrent updates can invalidate this snapshot.

## Six open PRs on this snapshot

| PR | Role and actual disposition | Dependency / review action |
| --- | --- | --- |
| [#529](https://github.com/zuizui0223/izu-core/pull/529) | **Draft** — independent I-mutation renewal experiment, preserved originals, readers, source-replay tests and claim synthesis. | Not a disposable duplicate of #536. The renewal source/design/readout files and scripts are unique to #529; reconcile them independently before any claim of full integration. |
| [#535](https://github.com/zuizui0223/izu-core/pull/535) | **Open** — Q3 genetic-access / prior-art manuscript foundation. | Targets `main`; #536 is stacked on its branch. Main manuscript/route overlap with #537/#538. |
| [#536](https://github.com/zuizui0223/izu-core/pull/536) | **Draft** — intended four-question integration, Ch1 six-edge crosswalk, renewal accounting, far-assurance Price audit, manuscript/SI and reviewer packaging. | **Base is #535's branch, not `main`.** Its observed base SHA `d87e3e74d2a9` differs from the later fetched #535 head `742db36c071c`; refresh the stack and inspect the complete diff before promotion. |
| [#537](https://github.com/zuizui0223/izu-core/pull/537) | **Open** — Q3 selection / finite access argument and its source-map plus distinct test. | Conflicts in active manuscript/SI/route with #535/#536/#538. Its `CHAPTER2_Q3_SELECTION_REALIZATION_SOURCE_MAP_20261015.md` and `test_chapter2_q3_selection_realization_claims_20261015.py` are not in #536's fetched file list. Audit before retiring it. |
| [#538](https://github.com/zuizui0223/izu-core/pull/538) | **Open** — Q3 finite inheritance explanation and source-backed tests. | Also edits manuscript/SI/route. #536 has a corresponding same-name test but **not identical bytes**; use content-level reconciliation rather than assuming a complete port. |
| [#540](https://github.com/zuizui0223/izu-core/pull/540) | **Draft** — 4,096 original checkpoints / 2,048 native Price cells from authentic archived source; no new biological trajectories. | The four files changed in #540 have **identical Git blob SHAs** on #536. Keep #540 as an independent evidence/review reference until #536 passes its own source and CI gates; avoid double-merging unchanged files. |

## Exact-blob overlap confirmed

The following SHA checks were made with `fetch_file` on the **named heads**, not filename heuristics:

| Compared branches and file | Result |
| --- | --- |
| #536 vs #540: `docs/CHAPTER2_FAR_ASSURANCE_ORIGINAL_GENOME_PRICE_AUDIT_20261015.md` | Equal, `c8480ac744076cceb0758eb1e86cd558afc129bf` |
| #536 vs #540: `docs/protocols/chapter2_far_assurance_price_checkpoint_20261015.json` | Equal, `69276826b5cde91b3e1d575dae9e398cf7ef7fef` |
| #536 vs #540: `scripts/audit_chapter2_far_assurance_price_checkpoints_20261015.py` | Equal, `c026c0c0604bf7767646c0dd6531da0271f7f7ea` |
| #536 vs #540: `tests/test_chapter2_far_assurance_price_checkpoints_20261015.py` | Equal, `23059c7406ca583a19fa7ffe5f2258499fccff3f` |
| #536 vs #529: `docs/CHAPTER2_CORE_CLAIMS_SYNTHESIS_20261015.md`, `docs/CHAPTER2_CORE_PRIOR_ART_CRITICAL_AUDIT_20261015.md`, `docs/audits/CHAPTER1_CURRENT_BRIDGE_SOURCE_20261015.json` | All three equal |
| #536 vs #529: `docs/ECOLOGICAL_INVESTMENT_RENEWAL_RESULTS_20261015.md` | **Different** (`d7c76a0...` vs `95e976d...`); not certified equivalent |
| #536 vs #538: `tests/test_chapter2_q3_finite_genetic_access_paper_20261015.py` | **Different** (`4c5b843...` vs `9405886...`); not certified equivalent |

Identical documentation or test blobs mean only those files match. They do **not** prove that corresponding source archives, historical runtimes, reviewed effect denominators, CI states or biological claims are identical.

## Branch inventory (counted, not pruned)

The GitHub branch listing contained **492 branches** across five complete pages of 100/100/100/100/92 at this audit, including this housekeeping branch. Prefix counts: `codex/` **160**, `agent/` **140**, `chapter2/` **61**, `analysis/` **53**, and **78** across other prefixes/unprefixed branches. The `main` branch was reported as unprotected by the same listing. Branch names and shared head hashes are **not** tests of scientific redundancy.

**No branch deletion or force update was performed.** Before reducing the branch count, protect `main`, all open PR heads, the #536 target/source branch, and any historical execution / frozen release / original-data recovery commit reachable only through a branch. For remaining candidates: inspect closed/merged PRs, unique commits, source/receipt SHA references and release/archive reachability; retain anything with unrecovered provenance. Only delete a branch after a recorded, independently verified preservation disposition.

## Safe integration sequence

1. **Freeze a refreshed source inventory:** list each PR's exact head/base, full changed-file list, upstream results/receipts, novel code, independent validation and final-head CI. Preserve the original archive/release identities and all registered negative verdicts.
2. **Decide the canonical manuscript branch:** review #535's current exact-head tests, incorporate it (or synchronize the stack) without dropping the merged main Q2 S29, then re-evaluate #536 **against the new base**. No blanket merging of #535/#537/#538 manuscript versions.
3. **Port nonduplicate science explicitly:** reconcile #537's unique source map/test, #538's nonidentical test and #529's unique frozen renewal source/readouts. #536's narrative mentions these studies but their absence from its diff must not be interpreted as automatic source admission.
4. **Avoid duplicate Price code:** #540's four bytes-identical files already sit on #536; preserve #540's original-source execution and external audit trail. Confirm no other unique change before marking it consolidated.
5. **Only then validate and merge:** exact final-commit CI on Python 3.10/3.11/3.12, Chapter 2 scientific gate, independent original readback and reviewer ZIP rebuild/member hashes; inspect manuscript word-limit counts, original data budgets and contribution identities. Archive/close redundant PRs **only after** verifying every unique contribution was retained.

## Claims not advanced by housekeeping

- The four ecological questions are **separate evidence families**, not demonstrated Q1→Q4 causal mediation.
- Inherited alleles being lost despite positive *conditional expected* contribution is a conditional Model 3 observation, not a general effect size for drift or a naturally measured extinction mechanism.
- Original fixed-I-access histories, I-mutation renewal histories, genetic-density comparisons and separate demographic capacity cohorts have different interventions and inference units. Similar counts (including “2,304”) cannot be silently pooled.
- The one-paper draft is not submitted. Reviewer package/release readback is not an external data DOI.
- This audit **does not** certify any open PR as green/merge-ready, and does not modify frozen scientific results.

For repository surfaces and evidence boundaries see [REPOSITORY_NAVIGATION.md](REPOSITORY_NAVIGATION.md).
