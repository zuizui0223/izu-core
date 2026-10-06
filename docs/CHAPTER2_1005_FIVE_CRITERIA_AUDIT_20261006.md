# Chapter 2 2026-10-05 five-criteria establishment audit — 2026-10-06

## Decision

The 2026-10-05 process result **passes the five establishment criteria as a
bounded model-level result** for the preregistered primary cell:

- delayed selfing;
- assurance cost 0.5;
- mutation probability 0.01.

The established statement is:

> Under sustained visitor-replenishment limitation, realized reproductive
> assurance change can precede floral-investment decline, but assurance
> evolution is not required for that decline. Isolation can lower the
> reproductive return to attraction directly.

This is not a universal selfing-syndrome sequence law.

## Criterion 1 — Novelty: PASS, with a narrow boundary

Selfing-first sequence is not novel by itself. Bodbyl Roels & Kelly (2011)
already favored a sequential selfing-syndrome interpretation after experimental
pollinator loss, and Gervasi & Schiestl (2017) showed pollinator-driven joint
evolution of floral and mating-system traits.

The paper-level novelty is narrower and survives those precedents:

> **temporal order is separated from causal necessity by a matched intervention
> within the same explicit pollination–reproduction model.**

The result is stronger than “assurance changes first” because the fixed-assurance
experiment independently shows that investment still declines when assurance
capacity cannot evolve. The fixed-plant assay supplies an upstream ecological
route: visitor limitation reduces the outcross return to attraction before plant
traits evolve.

The pollen-deficit/viable-offspring mismatch is retained as a reproductive
consequence, not claimed as a first general discovery.

Evidence:
- `docs/CHAPTER2_1005_NOVELTY_AND_LITERATURE_POSITION_20261006.md`
- `docs/MODEL3_FIXEDPLANT_RETURNS_RESULTS_20261005.md`
- `docs/MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md`

## Criterion 2 — Independent confirmation: PASS

The discovery used visitor histories 76001–76064 and demographic repeats
7101–7108.

Before the confirmatory outcome was generated, the design froze:

- 64 new visitor histories 26100601–26100664;
- eight new demographic repeats 26101601–26101608;
- the primary reproductive cell;
- the 0.05 threshold;
- 20-update persistence;
- five-update tie window;
- bootstrap seeds;
- success/admissibility criteria;
- a no-retuning rule.

The complete preregistered campaign contained 4,096 trajectories.

Primary sequence replication:

- assurance first: **51/64**;
- near-simultaneous: 13/64;
- assurance-first proportion: **0.796875**;
- 95% history-bootstrap: **0.6875–0.890625**.

The frozen rule required proportion >0.50 and lower interval bound >0.50.

Separate fixed-assurance replication:

- far investment change: **−0.306021**
  [−0.318054, −0.294111];
- far-minus-near investment: **−0.435389**
  [−0.453330, −0.417191];
- occupancy: 1.0 near and far;
- eligible histories: 64/64.

Both preregistered components passed.

Evidence:
- `data/design/chapter2_1005_confirmatory_replication_20261006.json`
- `data/results/chapter2_1005_confirmatory_replication_20261006.json`

## Criterion 3 — Robustness / sensitivity: PASS within the declared primary setting

The threshold range was frozen before confirmatory readout.

Delayed/costly, mutation 0.01:

| threshold | assurance first | 95% history-bootstrap |
|---|---:|---|
| 0.025 | 48/64 | 0.640625–0.844531 |
| 0.05 | 51/64 | 0.687500–0.890625 |
| 0.10 | 59/64 | 0.843750–0.984375 |

The assurance-first majority and lower interval bound >0.50 therefore persist
across all three declared thresholds.

This is robustness to the declared timing threshold, not robustness to every
biological parameter or proof of infinitesimal onset order.

The fixed-assurance replication also retains both negative primary estimands
with intervals wholly below zero.

## Criterion 4 — Scope / generality: PASS as an explicitly bounded claim

The primary sequence is **not general across reproductive settings**.

At the same primary 0.05 threshold:

- delayed/costly, mutation 0.01: 51/64 assurance-first,
  95% interval 0.6875–0.890625;
- prior selfing, mutation 0.01: 30/64 assurance-first,
  95% interval 0.34375–0.59375.

Therefore the paper must not say that assurance universally evolves first.
The confirmed temporal result is restricted to the delayed-selfing,
assurance-cost 0.5, positive-mutation cell.

All four setting-by-mutation cells are retained. Secondary cells cannot rescue
or overturn the frozen primary adjudication.

The fixed-assurance result is broader than the sequence result, and a separate
prospectively frozen generality campaign now establishes that breadth directly.
Across delayed control, prior selfing, pollen discount and assurance cost,
fixed-assurance far-minus-near investment was negative with 95% history-bootstrap
intervals wholly below zero. In the same campaign, the common-four-cell
evolving-minus-fixed interaction was positive with intervals wholly above zero
in all four settings (+0.1605, +0.2200, +0.1915 and +0.1007, respectively).
All arms/modes retained occupancy 1.0 and 64/64 eligible histories.

This broadens **non-necessity and attenuation**, not temporal ordering. The
sequence claim remains restricted to the delayed/costly primary cell.

## Criterion 5 — Claim boundary / reproducibility: PASS

The claim boundary is explicit:

- independent ecological denominator = **64 visitor histories**;
- eight demographic repeats are nested, not 512 independent environments;
- trait endpoints after extinction remain undefined rather than coded as zero;
- no outcome-dependent seed extension, threshold retuning or model adjustment;
- the 13-rate replenishment extension is exploratory and cannot rescue the
  confirmatory decision;
- the full-mutation common-environment experiment is complementary;
- the high-resolution positive-mutation deterministic/PDE comparison remains
  unresolved and is excluded from the biological headline;
- model distance/time/traits are not calibrated to natural kilometres, years,
  named islands, flower colours or Chapter 1 regional cells;
- fixed assurance is not absence of realized selfing and does not estimate a
  complete mediation fraction.

Reproducibility/provenance:

- frozen design SHA256 is recorded in the confirmatory result;
- all 4,096 declared cases were required before readout;
- workflow run and result-artifact identities/hashes are frozen;
- the active Chapter 2 scientific gate passes;
- the former Evolution Letters repeatability manuscript is retired as a
  standalone submission route;
- the historical Oikos package remains a frozen snapshot rather than a second
  active manuscript.

## Final establishment status

**ESTABLISHED, BOUNDED.**

What is established:
- the delayed/costly positive-mutation assurance-first sequence under the
  declared threshold definition;
- across all four declared reproductive settings, the non-necessity of assurance
  evolution for negative near–far investment divergence;
- across all four declared settings, attenuation of that divergence when
  assurance can evolve;
- the logical/ecological separation of sequence from necessity.

What remains exploratory/supporting:
- the 13-rate response surface;
- pollen-deficit versus viable-offspring contrast as a paper-level novelty;
- full mutation/history interpretation;
- finite-versus-deterministic attribution;
- natural-island causal transport.

What would require a new study rather than more analysis of this campaign:
- sequence generality across reproductive settings;
- natural longitudinal validation;
- calibrated geographic/evolutionary rates;
- full mediation through realized selfing;
- evolving genetic load/purging.

This audit does not reopen the confirmed result when those broader questions
remain unresolved.
