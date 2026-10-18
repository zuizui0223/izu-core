# Reconcile the two budget-companion runs before designing confirmation

**2026-10-18. Read-only, post-outcome reconciliation; no new independent study.**
Single developing paper: PR #590. Existing companion branch: PR #597.

## What changed since the previous conversation

PR #597 advanced to `f6020de6c58425c0fd3b19110d8b7ffccfa17e25`.
It already contains a budget companion reporting 1/72 fixed-A survivors under
B=4.5. The conversation artifact reports 5/72. These are DIFFERENT recorded
descendant seed families, not interchangeable copies of the same execution.

| Provenance | Repository companion | Conversation companion |
|---|---|---|
| Future master prefix | `[20261018,90]` | `[20261018,104]` |
| Suffix | founder index, visitor index, historical repeat | same |
| Original sources | same 6 x 6 x 2 x 2 historical paths | same |
| Branch point and horizon | census 35 to 80 | census 35 to 80 |
| Future budgets and visitors | B=8 / 4.5; no visitors | same |
| New founder/visitor draws | zero | zero |

The two runners share a filename but are not byte-identical implementations.
**Do not apply the old conversation patch over the current repository runner.**
The old source, both protocols, and the original 42/72 vs 58/72 pilot result
are preserved. New files here only record provenance and perform arithmetic.

## Root cause checked, rather than inferred from different counts

All 37 members in the conversation ZIP's manifest passed size/SHA-256 checks.
Its 16 existing local tests passed again. Its native Model3 files match their
pinned source hashes. The read-only array verifier rechecked 144 starting
states, 1,152 saved descendant genotype states and 13,248 annual census records.
Intermediate complete genotypes were not archived in that artifact and are
NOT claimed to have been inspected.

Using the conversation's actual census-35 arrays, a separate invocation of
its driver with the ALREADY RECORDED repository prefix90 reproduced all four
repository terminal-state counts and competing-first-event counts. This was
a same-seed audit replay, not a newly chosen random seed or extra scientific
replication. It verifies that the discrepancy is accounted for by the
descendant RNG assignment under the same native model and starting cohort.
It does not establish byte identity with an unavailable repository raw ZIP
or independently implement the underlying biology.

## Keep the results separate and retain original denominators

Each entry counts all 72 historically assigned paths per policy, not only
survivors. HIGH-I support means the maximum retained I allele meets that
path's original founder-mean target; it does not prove actual trait recovery.

| Stream | Budget | Fixed alive | Evolving alive | Fixed alive/access | Evolving alive/access |
|---|---:|---:|---:|---:|---:|
| 90 | 8 | 72 | 72 | 27 | 22 |
| 90 | 4.5 | 1 | 71 | 0 | 20 |
| 104 | 8 | 72 | 72 | 30 | 21 |
| 104 | 4.5 | 5 | 71 | 0 | 17 |

The historical-A-policy x budget-challenge interaction is
`(evolving - fixed at B4.5) - (evolving - fixed at B8)`.

| Outcome | Stream90 interaction | Stream104 interaction |
|---|---:|---:|
| Unconditional survival | +97.22 pp | +91.67 pp |
| Unconditional alive AND required I allele range | +34.72 pp | +36.11 pp |

For stream104, the same six-by-six crossed percentile calculation gives an
exploratory 95% interval of +80.56 to +100 pp for survival, and +11.11 to
+61.11 pp for alive/access. Both signs agree with stream90, but these are
nested future realizations of the SAME founder/visitor backgrounds. They
do not increase the independent source counts beyond six per axis.
They do not independently confirm the mechanism or its generality.

Under challenge, 51/71 evolving survivors in stream90 and 54/71 in stream104
lack the strict founder-level HIGH-I range. Conversely, 20 and 17 retain it,
whereas none of the fixed-arm survivors do. Functional survival and inherited
options must therefore stay as separate endpoints. This remains a synthetic
conditional budget intervention, NOT an experiment returning pollinators.

## Actual inputs for the next method review

The separate unchanged equal-A pilot supplies the genetic-loss endpoint:
fixed 42/72 versus evolving 58/72. Its paired variance components are founder
0.0233333, visitor 0 after truncation, interaction 0.0655556, within-cell
0.2777778. Zero after truncation is not proof of zero true variance.

The survival-interaction components are:
- Stream90: founder 0, visitor 0, interaction 0.0005556, within-cell 0.0277778.
- Stream104: founder 0, visitor 0.0022222, interaction 0, within-cell 0.0833333.

Using the EXISTING #585 Normal/Bonferroni screening convention with two nested
historical repeats, familywise alpha .05, and joint directional target .80:

| F x V | Genetic-loss MDE proxy | Survival MDE, stream90 | Survival MDE, stream104 |
|---|---:|---:|---:|
| 6 x 6 | 34.46 pp | 7.06 pp | 13.77 pp |
| 16 x 16 | 16.74 pp | 2.65 pp | 6.12 pp |
| 32 x 32 | 10.74 pp | 1.32 pp | 3.70 pp |
| 64 x 64 | 7.17 pp | 0.66 pp | 2.36 pp |

**The baseline precision bottleneck is genetic-access loss, not rescue.**
Repeated descendant futures on the same backgrounds cannot substitute for
independent founders/visitor histories. These MDEs are conditional on noisy
pilot moments; they are not actual power guarantees. The explicit earlier
stress assumption (.05 founder, .05 visitor, .20 interaction, .40 within-cell)
gives 20.89 pp at 32x32 and 14.35 pp at 64x64, so these larger designs are
not automatically adequate either.

No smallest scientifically meaningful effect was selected here. No new
sample size was frozen, no confirmatory seed registry was allocated, and
no new confirmation is authorized. The next method review must justify
endpoint-specific effect margins, source-qualified adverse variances,
operating characteristics and a full shared-history/fork computation budget.
This review advances the measured inputs rather than relabeling exploration.

## Reproduce this arithmetic

```
python -m scripts.audit_chapter2_budget_streams_20261018 --out NEW_REVIEW.json
pytest -q tests/test_budget_streams_20261018.py
```

The four new tests first failed with the missing audit module and passed
after implementation. They check both four-arm interactions, conserved
terminal-state totals, crossed-source counts, and rejection of missing states
or duplicated stream prefixes. No native biology is imported by this review.

The compact source file preserves every terminal state in documented
founder/visitor/repeat order. The conversation ZIP is identified by its
SHA-256 in that file; its frozen prefix104 driver is not substituted for
the repository's prefix90 driver. The revalidation/replay files and the
unaltered conversation ZIP remain in the accompanying downloadable bundle.
