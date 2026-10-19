# Bounded readaptation: completed conditional experiment

## Execution and admission

[Actions run 39208955029](https://github.com/zuizui0223/izu-core/actions/runs/39208955029)
completed production in 49m44s using scientific source
`e66178385e9f09e3f46d5285368aa88439b02811`, Python 3.12.10, NumPy 2.2.6 and
SciPy 1.15.3. All 64 transferred cohorts and 10,240 futures passed source-lineage,
raw-arithmetic and same-implementation replay checks. Validation replays are not
additional independent scientific samples or an independent biological model.

The unchanged [bounded design](CHAPTER2_READAPTATION_LOCAL_DESIGN_20261019.md)
crosses four original founders with four visitor histories, two historical A
policies and two seed-derived cohorts per donor. Each cohort enters five
destinations with 32 independently seeded futures and 80 updates. Both historical
arms permit A evolution after transfer. There is no mutation or immigration;
all transferred viable offspring establish initially. This is conditional
readaptation at one late donor census, not a new 160x160 confirmation or a test
of natural island assembly.

The 370,674,547-byte original artifact is retained in a
[draft release](https://github.com/zuizui0223/izu-core/releases/tag/untagged-2b258d2e651d1f74ec8c),
tag `readaptation-e6617838-20261019`. Downloaded artifact and release readback both
match SHA-256 `3a8014a0706daec862a9dad46a1a211a4032e7872d2dbbc8022222de58cc1399`.
This is retained GitHub storage, not an immutable DOI archive.

A separate Windows/Python 3.10.11 readback re-admitted all raw records against
the original 160x160 source archives. Strict serialized equality initially failed:
440 interior exact-interval values differed by at most 1.6653345369377348e-16.
All other JSON values and types agree exactly, including counts, traits,
performance, support and timing. A **post-run technical reconciliation rule**
permits absolute differences <=1e-12 only in interior beta-quantile fields;
exact boundaries 0/1 and all other fields remain strict. This changes neither
the frozen inference nor a biological response threshold. Both numerical versions,
the original strict failure and the difference inventory are retained. The first
audit returned successfully before its final comparison failed; because that
command did not save its result before the assertion, the complete readback was
repeated with persistence before comparison. No scientific simulation was rerun.

Receipts: [independent audit](audits/CHAPTER2_READAPTATION_INDEPENDENT_AUDIT_20261019.json),
[release readback](audits/CHAPTER2_READAPTATION_RELEASE_READBACK_20261019.json),
[strict comparison failure](audits/CHAPTER2_READAPTATION_STRICT_COMPARISON_FAILURE_20261019.json),
[descriptive tables](audits/CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json).

## Occupancy, trait response and performance

Each table cell pools **32 cohorts x 32 futures = 1,024 conditional futures** for
description only. It is not an iid sample of 1,024 founders. Pointwise exact
intervals remain attached to each of the 320 cohort/destination groups (n=32).
Even 32/32 successes retain a one-sided 95% failure upper bound of 8.94%.
No pooled confidence interval or new significance test is introduced.

| Destination (activity; visitor optima) | Occupied, fixed-A history | Occupied, evolving-A history | I increases, fixed history | I increases, evolving history |
|---|---:|---:|---:|---:|
| No visitors | 704 | 1,024 | 27 | 29 |
| .25; .5 | 1,024 | 1,024 | 109 | 101 |
| .25; .7 | 961 | 1,024 | 108 | 95 |
| 1; .5 | 1,024 | 1,024 | 105 | 115 |
| 1; .7 | 1,021 | 1,024 | 113 | 108 |

Extinction remains in the all-start denominator; trait changes and reproductive
performance are undefined for extinct endpoints. Historical treatments generated
different inherited M, I and A states. These differences do not isolate an
A-mediated mechanism or establish a pure causal effect of A at transfer.

Performance is expected genetic return against 47 fixed reference competitors:
**0.5 maternal outcross + 0.5 paternal outcross + viable self contribution**,
evaluated in the same destination at entry and the final census. It is distinct
from floral investment or attaining an ancestral target.

| Destination | Mean performance change among survivors, fixed history | Mean performance change among survivors, evolving history |
|---|---:|---:|
| No visitors | +0.071125 (n=704) | +0.007440 (n=1,024) |
| .25; .5 | +0.041494 (n=1,024) | +0.035322 (n=1,024) |
| .25; .7 | +0.089992 (n=961) | +0.068857 (n=1,024) |
| 1; .5 | +0.065507 (n=1,024) | +0.076691 (n=1,024) |
| 1; .7 | +0.162268 (n=1,021) | +0.215564 (n=1,024) |

These positive descriptive means do not imply universal improvement or significant
effects. Every row includes negative changes. Several medians and exact sign counts
include roundoff near zero; no post-outcome biological cutoff is applied. Full
effect magnitudes, endpoints, pointwise intervals, exclusion and extinction times
are retained in `campaign/SUMMARY.json` inside the release archive; the compact
tables do not replace those conditional distributions.

## Inherited variation limits the proposed asymmetry

All 32 cohorts from evolving-A histories enter with A=.75 and no A polymorphism;
all 5,120 futures retain A=.75. Their founder-relative low-A support is absent
at entry and final census for **all five** epsilon values (0, .005, .01, .02, .05).
The absence is therefore not the earlier micro-pilot's .008 target-boundary issue.
This supports inherited constraint in this sample, but cannot estimate selection
on an absent lower-A variant or prove irreversible evolution with new variation.

I remains polymorphic in only **4/32 cohorts in each historical arm**. Those four
cohorts provide all observed I changes in visitor destinations; the other 28 do
not change I. Yet 24/32 cohorts in each arm retain founder-relative high-I support.
Having an allele above a target is not equivalent to having segregating variation.
M is polymorphic in 17/32 evolving-history and 12/32 fixed-history cohorts; A is
polymorphic in 5/32 fixed-history cohorts. Later performance changes therefore
cannot automatically be attributed to I alone.

For each of the five epsilon values, terminal high-I support counts in destination
order are 576,768,758,768,768 (fixed history) and 734,766,762,768,767 (evolving
history). Terminal low-A support counts are 320,718,581,779,689 and 0,0,0,0,0,
respectively. These are supported occupied futures out of 1,024 allocated futures;
extinct records have undefined support, not biological support failure.

The broad assertion that flowers remain freely adjustable after long limitation
is **not supported at this late donor time**. The narrower prediction that floral
responses depend on surviving variation is consistent with the observations.
Assurance invariance here is structural fixation, not evidence that its selection
gradient is zero or that private benefits make evolution intrinsically deterministic.

## Central-question conclusion and limits

Together with the [160x160 confirmation](CHAPTER2_CONFIRM160_RESULTS_20261019.md),
the results support distinct assurance/investment mechanisms, conditional temporal
order, and effects of assurance evolution on accessibility and persistence.
Actual new-environment responses are now observed under the bounded intervention;
they do not establish a universal restoration window or permanent irreversibility.
The [matched repeatability audit](CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.md)
and the history/capacity analysis remain exploratory evidence that floral outcomes
have predictable structure, rather than unstructured chance.

Natural island assembly, evolving deleterious load, obligate outcrossing and the
relative contribution of within-lineage evolution versus natural lineage filtering
remain unidentified. The original central hypothesis is partially supported and
must be narrowed; completion of this experiment does not prove every clause.

Reproduce compact tables with `python scripts/summarize_readaptation_results_20261019.py
<readback-directory> --output <tables.json>`. The directory requires `campaign/`,
`independent-raw-audit.json` and `independent-audit-receipt.json`. Full records and
the source audit remain authoritative; raw-arithmetic admission is distinct from
same-implementation biological replay.
