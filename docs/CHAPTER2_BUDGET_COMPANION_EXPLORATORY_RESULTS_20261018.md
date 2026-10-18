# A source-conditional demographic companion: survival and inherited floral access

**Status: executed exploratory companion, not a registered confirmation.**
One developing Article remains in PR #590; this companion is part of PR #597.
The original equal-A pilot, its 42/72 versus 58/72 HIGH-I losses, and all older
Q1–Q4 decisions remain unchanged. No direct resource-to-fitness mediation,
field-island generality, or actual pollinator-return recovery is claimed.

## Pre-outcome scope and source reconstruction

Design commit **0c5b549888b130b086c171fc2be2ed5924dfe66b** preceded execution.
Its JSON was frozen with one checkpoint, t=35, one proposed budget challenge,
B=4.5, and B=8 control. Both futures use no visitors through t=80. The challenge
was proposed AFTER the old pilot and its analytical ceiling diagnostic; the
companion is therefore prospectively specified exploration, not retroactive
confirmation. It was deliberately chosen to distinguish demographic outcomes,
not calibrated to a real island's ovule budget.

All original 6-founder x 6-visitor x 2-demographic-repeat x 2-historical-A
histories were reconstructed using their original seeds and unchanged native
Model3 operators. Every original logged first HIGH-I loss, evolving low-A loss
and final occupancy agreed across the full 144 histories. This establishes an
exact event-record replay, NOT independent comparison with an old raw checkpoint
archive. We then saved all five PlantState fields at census 35 with hashes.

Each t35 state was cloned into B=8 and B=4.5, keeping its original A expression
policy. A was not forced to .75; no high-A-survivor selection was used. There
were 288 NEW future trajectories, each with 45 updates (12,960 maximum updates),
and no new founder/visitor draws. Future master seeds use the distinct prefix
[20261018,90], with founder, visitor and historical-repeat indices but no budget
or A-policy index. Generator identities are matched; draw consumption need not
remain synchronized after populations diverge. All assigned histories remain
in their denominators. There is no mutation, immigration, or adult carryover.

## Actual result at t80: separate living/genetic states

| Population state | Fixed A, B8 | Evolving A, B8 | Fixed A, B4.5 | Evolving A, B4.5 |
|---|---:|---:|---:|---:|
| Initially assigned | 72 | 72 | 72 | 72 |
| Alive | 72 | 72 | 1 | 71 |
| Alive with required HIGH-I allele range | 27 | 22 | 0 | 20 |
| Alive but founder HIGH-I target excluded | 45 | 50 | 1 | 51 |
| Extinct | 0 | 0 | 71 | 1 |

HIGH-I access means max retained I allele >= its own founder-mean target.
It is a necessary support condition, not proof of realized recovery. B8 futures
here have newly assigned RNG streams; their counts are NOT replacements for the
old 42/72 versus 58/72 source results.

The prespecified historical-policy x challenge occupancy interaction is

```
[(71-1)/72] - [(72-72)/72] = +0.9722222222.
```

The same interaction for unconditional **alive AND required allele range** is

```
[(20-0)/72] - [(22-27)/72] = +0.3472222222.
```

Thus the challenge makes a rescue difference measurable in this synthetic
source cohort. Survival is not equivalent to preserved floral options: 51 of
71 surviving evolving-A populations lack the founder HIGH-I range. Conversely,
20 retain it, compared with none under the fixed-A challenge. Insurance need
not have a uniformly negative effect on the joint alive-and-access outcome:
keeping lineages alive can preserve options that would otherwise disappear
with extinction. These are total historical-policy effects, not the direct
isolated effect of a final A value or a demonstrated genetic mediation path.

## Extinction is not coded as a zero-I genotype

Under B4.5, the fixed arm has 39 genetic-loss-first histories and 33
extinction-first histories. Its 71 terminal extinctions include 38 deaths
AFTER genetic closure. The evolving arm has 52 genetic-loss-first histories,
zero extinction-first, and 20 still alive/access histories; one of the 52 died
later. Both first-event probabilities and current-state probabilities partition
all 72 assignments correctly. Comparing 39/72 and 52/72 alone would ignore
competing extinction and cannot establish a faster genetic clock in the second
arm. The joint living/access endpoint is retained for that reason.

## Exploratory crossed-source uncertainty

The existing read-only pigeonhole bootstrap enumerates all multinomial weights
on six founder and six visitor levels. Each resampled cell retains both A
policies, both budgets and the average of its two nested repeats. Enumerating
weights eliminates bootstrap Monte Carlo error, not interval coverage error.

| Interaction, evolving-minus-fixed effect under B4.5 minus B8 | Nominal 95% interval | Nominal 97.5% marginal sensitivity |
|---|---|---|
| Alive probability | +90.28 to +100.00 percentage points | +88.89 to +100.00 points |
| Alive AND HIGH-I range | +6.94 to +61.11 points | +2.78 to +65.28 points |

The survival interaction is positive in all six founder-level averages. The
allelic-range interaction is nonnegative in all six, with one exactly zero.
These intervals remain exploratory with six source levels per axis. This is
not a #585-approved new independent confirmation, a natural-island probability,
or a power calculation using a justified biological SESOI.

## Verification, reproduction and retained evidence

Native types, random streams, history, reproduction and population files match
GitHub source SHA-256 hashes. Six new tests (16 including existing precision
and demographic-ceiling tests) passed locally. Scientific cohort execution is
explicit CLI work; these tests DO NOT automatically launch all 288 futures.

The separate raw reviewer imports neither the runner nor the biological
operators. It checked all 288 raw NPZ trajectories, all 13,248 genotype censuses,
all five state fields at the 288 starts, birth/ID consistency, absorbing
extinction, shrinking allele sets at every locus, summary/array agreement,
matched seeds, and the competing-event/current-state partitions. All passed.
This is independent arithmetic verification, not independently coded biology.

The conversation ZIP contains source copies, the frozen design, replayed t35
states, full padded five-field NPZ trajectories, FUTURES.json, interval matrices,
code and verification logs. The repository stores executable code, this report
and a compact execution receipt; no frozen tracked-data tree was modified.

```
python -m scripts.run_chapter2_budget_companion_20261018 replay --out replayed_checkpoints
python -m scripts.run_chapter2_budget_companion_20261018 futures --source replayed_checkpoints --out companion_futures
python -m scripts.run_chapter2_budget_companion_20261018 summary --source companion_futures --out NEW_SUMMARY.json
python -m scripts.audit_chapter2_budget_companion_raw_20261018 --root companion_futures --out NEW_RAW_AUDIT.json
pytest -q tests/test_budget_companion_20261018.py tests/test_demographic_ceiling_20261018.py tests/test_audit_equalA_precision.py
```

Use new empty output directories; the runner refuses overwrite. A freshly
reconstructed source uses the same seeds, not independent new biological data.
For a confirmation, use a new source cohort, externally justified effect margin,
reviewed two-axis power/variance assumptions and the separate #585 gate. No
additional budget/checkpoint search or automatic confirmation is authorized by
this result. Actual flower recovery after returning visitors remains unmeasured
in this companion.
