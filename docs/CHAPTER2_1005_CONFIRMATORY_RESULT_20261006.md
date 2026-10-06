# Chapter 2 process result — independent confirmatory replication

Status: **CONFIRMED under the preregistered primary rule.**

The design was frozen before the new visitor-history and demographic outcomes
were generated. It used visitor-history seeds `26100601–26100664` and
demographic-repeat seeds `26101601–26101608`, distinct from the 2026-10-05
discovery seeds. All 4,096 declared trajectories completed before biological
readout. The inferential unit remains 64 independent visitor histories; eight
demographic repeats are nested within each history.

## Primary sequence result

The preregistered primary cell is delayed selfing with assurance cost 0.5,
mutation probability 0.01, and a 0.05 trait-change threshold sustained for
20 updates. Histories within five updates are classified as near-simultaneous.

The independent replication produced:

- assurance first: **51/64**
- near-simultaneous: **13/64**
- investment first: **0/64**
- assurance-first proportion over all histories: **0.796875**
- 95% visitor-history bootstrap interval: **0.6875–0.890625**

The frozen success rule required an assurance-first proportion above 0.50 and a
95% bootstrap lower bound above 0.50. **Both conditions passed.**

This exactly reproduces the discovery count of 51/64 on new visitor histories
and new demographic repeats. It is a confirmation of realized threshold-crossing
order, not evidence that assurance selection first appears under isolation.

## Threshold sensitivity

For the preregistered delayed/costly positive-mutation cell, assurance-first
remained the majority across all three declared thresholds:

| threshold | assurance first | near-simultaneous | proportion | bootstrap 95% |
|---:|---:|---:|---:|---:|
| 0.025 | 48 | 16 | 0.750 | 0.641–0.845 |
| 0.050 | 51 | 13 | 0.797 | 0.688–0.891 |
| 0.100 | 59 | 5 | 0.922 | 0.844–0.984 |

The direction is therefore not an artifact of selecting only the 0.05 threshold
within this cell.

The result is **not universal across reproductive settings**. Under prior selfing
with positive mutation, the 0.05 threshold gave 30/64 assurance-first histories
and a 95% interval of 0.344–0.594. The manuscript must therefore restrict the
confirmed sequence claim to the delayed-selfing, assurance-cost setting unless a
separate preregistered generality test broadens it.

All four setting-by-mutation cells at the primary 0.05 threshold were reported:

| setting | mutation | assurance first | near-simultaneous / assurance-only | proportion | bootstrap 95% |
|---|---:|---:|---:|---:|---:|
| delayed + assurance cost | 0 | 42 | 6 near-simultaneous + 16 assurance-only | 0.656 | 0.531–0.766 |
| delayed + assurance cost | 0.01 | 51 | 13 near-simultaneous | 0.797 | 0.688–0.891 |
| prior selfing + no assurance cost | 0 | 40 | 24 near-simultaneous | 0.625 | 0.500–0.734 |
| prior selfing + no assurance cost | 0.01 | 30 | 34 near-simultaneous | 0.469 | 0.344–0.594 |

Only the predeclared delayed/costly positive-mutation cell determines the
confirmatory success decision. The remaining cells define generality limits and
cannot rescue or overturn that frozen primary test.

## Primary fixed-assurance result

The separate preregistered intervention held assurance capacity at 0.5 and used
the same new visitor-history and demographic seed blocks. Occupancy was 100% in
both near and far arms, with all 64 histories eligible.

Delayed-selfing/costly primary cell:

- far investment change from founders:
  **−0.30602**, 95% bootstrap **−0.31805 to −0.29411**
- far-minus-near investment:
  **−0.43539**, 95% bootstrap **−0.45333 to −0.41719**

The frozen rule required both means to be negative and both upper confidence
bounds to remain below zero. **The fixed-assurance criterion passed.**

The prior-selfing secondary cell also retained negative investment responses:

- far change: **−0.33160** [−0.34178, −0.32099]
- far-minus-near: **−0.30938** [−0.32463, −0.29418]

These secondary results cannot rescue the primary test, but they strengthen the
bounded statement that investment decline does not require assurance-capacity
evolution under the declared intervention.

## Adjudication

Both preregistered primary components passed:

```text
sequence_success       = true
fixed_assurance_success = true
overall status          = confirmed
```

Therefore the 2026-10-05 process result can now be stated as a confirmed
model-level finding:

> **Under sustained visitor-replenishment limitation in the delayed-selfing,
> costly-assurance setting, realized reproductive-assurance change can precede
> floral-investment decline, yet assurance evolution is not required for the
> investment decline.**

The mechanistic fixed-plant assay remains the upstream explanation: isolation
can reduce the marginal outcross return to attraction before either plant trait
has evolved.

## Claim boundary

This confirmation does not establish that:

- assurance-first order is universal across reproductive systems;
- assurance selection is initiated by isolation before investment selection;
- temporal precedence proves mediation;
- fixed assurance means no realized selfing;
- the 13-rate exploratory extension is confirmatory evidence;
- model time/distance are calibrated natural units;
- the unresolved positive-mutation high-resolution deterministic/PDE comparison
  has been solved.

## Provenance

- preregistration:
  `data/design/chapter2_1005_confirmatory_replication_20261006.json`
- compact frozen result:
  `data/results/chapter2_1005_confirmatory_replication_20261006.json`
- GitHub Actions run: `37390991122`
- result artifact: `11381590034`
- full result JSON SHA-256:
  `1951af2f2d5a8be883eae514aa84dce7d6a40407201c9a8cce501d4502773900`
- artifact ZIP SHA-256:
  `7c5c252cf559067f218bbd9f37b74b00c5d9c52fe30f25bb0196c9bfb9cb4872`
