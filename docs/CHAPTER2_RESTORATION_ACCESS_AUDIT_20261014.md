# What the existing investment-variation restoration tests

## Answer to Q3 and the central question

The intervention restored transmissible investment variation in all 61 triggered
histories, and all 61 developed between-individual expressed investment variance
at the next census. It did **not** give every history genetic access to the
original sustained-decline criterion: 19/61 remained below the required extent
of downward access. Another 27 already had support for that criterion at the
trigger; only 15 moved from exclusion to support. All 15 belong to `causal_main`.
Thus this particular fixed-width restoration is a test of restoring variation
after complete fixation, with heterogeneous access to the earlier event target.
It is not a uniform intervention opening that target in both founder blocks.

This sharpens the central question's distinction between a genetic change being
possible and being realized within a finite population and observation period.
The actual frozen primary remains **unresolved**: original minus restored terminal
mean I = **0.0074869792**, existing 95% interval **[-0.0056152344, 0.0203460693]**;
block estimates **+0.0194905599** and **-0.0045166016**. No interval or decision was
replaced. The new event/support summaries below are retrospective descriptions,
not a second primary, a new significance family, or evidence of equivalence.

In particular, inability to reach the *event* target does not invalidate the
terminal-mean primary: an intervention can lower investment by less than the
event criterion. Nor does restoration followed by no event establish that
selection is absent or that genetic variation is generally irrelevant.

## Admitted evidence and scope

Source/readout snapshot: [`688bcdf563d4150e6f3618e27967469cbbaa341e`](https://github.com/zuizui0223/izu-core/commit/688bcdf563d4150e6f3618e27967469cbbaa341e).
The [registered protocol](https://github.com/zuizui0223/izu-core/blob/688bcdf563d4150e6f3618e27967469cbbaa341e/docs/CHAPTER2_INVESTMENT_VARIATION_RESTORATION_PROTOCOL_20261013.md)
defines the outcome-informed diagnostic: 32 histories in each of two original
assurance-causal founder blocks, supply 0.125, matched visitors, N=K=48, standing
M/I and mutating A, horizon 200. This is not the 2,304-history F1 cohort or the
new 4,096-condition assurance parent-selection control.

The audit reads these published artifacts without executing any biological
producer or extending a history:

| Artifact | SHA-256 |
|---|---|
| [Restoration64 original/restored raw bundle](https://github.com/zuizui0223/izu-core/releases/download/four-question-resolution-20261013/INVESTMENT_VARIATION_RESTORATION_64_20261013.zip) | `90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6` |
| [Existing pathwise accounting bundle](https://github.com/zuizui0223/izu-core/releases/download/four-question-resolution-20261013/RESTORED_PATHWISE_ACCOUNTING_REVIEW_20261013.zip) | `07e86248551b1dce24ea91f1566c54e6a8c7f8932ac96479e2cd78e708ce572d` |
| [Original source-input archive](https://github.com/zuizui0223/izu-core/releases/download/atom-cell-inputs-20261011/remote_atom_inputs_20261011.zip) | `f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037` |
| [Original full cohort](https://github.com/zuizui0223/izu-core/releases/download/atom-cell-inputs-20261011/completed_atom_abm_20261011.zip) | `7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918` |

All four archive hashes are recomputed. The 516 payload members of the raw bundle
match its manifest. The 64 original NPZ files are byte-identical to the members
of the full original cohort; paired receipts and restored NPZ hashes agree. The
frozen biology files match the original source manifest. The cohort/source
archives contain other work: only the declared 64 pairs enter this audit.

## What was restored, and what target could it reach?

At the first occupied census when every I allele equals v, the intervention
replaces each individual's I pair by `[v - 1/16, v + 1/16]`. The raw arrays verify
the exact edit and preservation of each individual's expressed means, M/A alleles,
IDs, origins, mutation flags and birth years. Origins are preserved metadata,
not proof that these artificial I alleles existed naturally.

At that instant allele-copy variance is 1/256 but between-individual expressed
variance is zero. All 61 triggered histories have positive expressed variance at
the next census. The three non-triggered histories have only an unchanged terminal
placeholder in the restoration archive; their full trajectories come from the
original archive. They remain in every all-64 comparison.

The original criterion is a reduction of at least 0.05 from the *history's original
initial mean*, sustained for 20 consecutive censuses. The initial means differ by
founder block. We do not reset that baseline at intervention. Without I mutation,
immigration or another restoration, all future I alleles must descend from the
extant support. If its minimum exceeds the original event target, the event is
impossible in the saved model. The reverse is only a necessary-support check:
it does not guarantee the parental returns, finite sampling, timing, or 20-census
persistence needed to realize an event.

| Property | causal_main | causal_confirmation | Total |
|---|---:|---:|---:|
| Original pairs | 32 | 32 | 64 |
| Triggered / unchanged | 31 / 1 | 30 / 2 | 61 / 3 |
| Initial mean I | 0.53125 | 0.4609375 | — |
| Original event target I | 0.48125 | 0.4109375 | — |
| Support already present at trigger | 7 | 20 | 27 |
| Newly gains support after restoration | 15 | 0 | 15 |
| Still excluded after restoration | 9 | 10 | 19 |
| Refixed by census 200 | 21 | 24 | 45 |
| Original sustained events | 11 | 20 | 31 |
| Restored sustained events | 18 | 17 | 35 |

For example, a trigger at v=0.5 restores a lower allele of 0.4375 in both blocks.
This lies below main's target 0.48125 but above confirmation's target 0.4109375.
Thus the same edit opens main's target but not confirmation's. These observed
block differences explain why the diagnostic cannot be described as providing
the same event-access treatment in both blocks; they do not uniquely explain
the terminal-mean block contrast.

## Finite opportunity and realized paths

Triggers span years 12–197, leaving 188–3 updates. Sixty of the 61 triggered paths
have at least 20 saved post-intervention censuses. The late case is
`causal_confirmation_s0.125_matched_n48_standing_MI_new_A_r6_evolving` (trigger 197),
which also remains genetically excluded from the event target. These constraints
overlap; they must not be summed into independent explanations.

By census 200, 45/61 triggered paths refix. Among these **observed refixations**,
time from intervention ranges from 19 to 128 updates (median 51). The other 16
are right-censored for refixation at 200; they are not assigned an infinite or
zero fixation time. Variation is restored once, not maintained indefinitely.

On full original-baseline trajectories, event incidence changes from 31/64 to
35/64: seven main histories gain an event, three confirmation histories lose
one. All seven gains occur among the 15 newly supported main histories; eight
newly supported histories do not realize the event. There are no new intervals
or tests for these selected descriptive counts. The original event had already
completed before intervention in 10 triggered histories. The case table therefore
separates original events, events anywhere on the stitched restored trajectory,
and starts of complete post-trigger 20-census runs. An already completed event
cannot be erased by a later edit.

The full trajectory uses original censuses strictly before the trigger and saved
restored censuses from the trigger onward. It includes events spanning the
trigger, rather than discarding their original pre-trigger observations. The
separate post-trigger field answers a narrower timing question and is not used
to replace the frozen primary or the all-64 event counts.

## Relation to the existing signed accounting

Every one of 7,740 saved restored updates is joined to the existing accounting by
case, raw hash and year. The audit reconstructs selected-parent means from raw
parentage and checks I inheritance, transmission changes, closure, cumulative
changes and both block means. Expected reproductive response is the authenticated
saved expectation already independently checked in the accounting bundle; this
audit does **not** claim to freshly recompute the reproductive kernel.

| Mean cumulative I change per original block slot | causal_main | causal_confirmation |
|---|---:|---:|
| Expected reproductive response | -0.01830064 | -0.01138617 |
| Selected-parent deviation from expectation | -0.00611342 | +0.01368516 |
| Transmission deviation | +0.00492350 | +0.00221761 |
| Observed post-restoration change | -0.01949056 | +0.00451660 |

All 32 slots per block are retained, including zero-change no-trigger controls.
The observed post-restoration change is the negative of the original-minus-
restored terminal contrast because original I remains fixed after the trigger.
This is signed accounting on realized paths. It is not a noise-free alternative
history, a unique causal share, a causal decomposition of block differences, or
a claim about persistence benefits in natural evolutionary order.

## Reproduction and verification

From the repository root, download the four named files above into `work/q3-input`
(or another input directory), then run:

```sh
python scripts/audit_restoration_access_20261014.py \
  --restoration work/q3-input/INVESTMENT_VARIATION_RESTORATION_64_20261013.zip \
  --accounting work/q3-input/RESTORED_PATHWISE_ACCOUNTING_REVIEW_20261013.zip \
  --source-input work/q3-input/remote_atom_inputs_20261011.zip \
  --cohort work/q3-input/completed_atom_abm_20261011.zip \
  --out work/q3-reproduced
python -m pytest tests/test_restoration_access_20261014.py -q
```

The first command requires a new output directory and fails closed on an input,
inventory, intervention or arithmetic mismatch. It writes the compact summary and
the [64-row case table](../data/results/restoration_access_cases_20261014.csv).
The [summary](../data/results/restoration_access_audit_20261014.json) binds the
script and case-table hashes. Blank CSV fields are undefined/not applicable,
including post-trigger fields for the three no-trigger slots; they are not zeros.
`remaining_updates=0` for those slots describes their terminal-only stored
restoration placeholder, not absence of the original 200-update history.

Focused tests cover support versus fixation, hidden versus expressed variation,
the original sustained-event rule, undefined extinct means, malformed genotypes
and offsets, exact no-trigger state equality, and duplicate inventory rejection.
Raw-data independent verification is recorded separately; passing fixture tests
alone does not validate the biological case table.

A fresh reviewer independently rebuilt all **64 × 32 case-table fields** from
raw arrays without importing the audit, and checked all **7,740 annual terms**
(maximum discrepancy 0 against the saved accounting). The
[independent receipt](../data/results/restoration_access_independent_20261014.json)
binds the reviewed code, this document, the CSV and the input archives. Reproduce
that separate implementation with a new receipt path:

```sh
python scripts/verify_restoration_access_independent_20261014.py \
  --input-dir work/q3-input \
  --case-table data/results/restoration_access_cases_20261014.csv \
  --audit-script scripts/audit_restoration_access_20261014.py \
  --document docs/CHAPTER2_RESTORATION_ACCESS_AUDIT_20261014.md \
  --out work/q3-independent.json
```
