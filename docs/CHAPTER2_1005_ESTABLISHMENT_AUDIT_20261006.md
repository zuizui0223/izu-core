# Chapter 2 2026-10-05 process result — establishment audit

Date: 2026-10-06  
Status: **ESTABLISHED WITHIN THE DECLARED MODEL SCOPE**

This audit applies the five predeclared establishment criteria to the active
2026-10-05 process paper. It does not promote the result to a universal island
law or a calibrated natural-island causal claim.

## Frozen central claim

> **In the delayed-selfing, assurance-cost 0.5, positive-mutation setting,
> reproductive assurance can change before floral investment declines, yet
> assurance evolution is not required for that investment decline. Reduced
> visitor replenishment can lower the outcross return to attraction directly,
> so realized temporal order does not identify a necessary serial causal
> pathway.**

The wording is deliberately about **realized trait change**, not "selection
appearing first": local selection on assurance can already be positive under
less-isolated conditions.

## Criterion 1 — central claim frozen before confirmation: PASS

The active mainline lock and confirmatory contract were frozen before the new
visitor-history outcomes were generated. The primary cell was fixed as delayed
selfing, assurance cost 0.5, mutation probability 0.01. No secondary cell was
allowed to rescue a failed primary result.

Sources:
- `data/design/chapter2_1005_ecological_mainline_lock_20261006.json`
- `data/design/chapter2_1005_confirmatory_replication_20261006.json`

## Criterion 2 — independent confirmatory rerun: PASS

The confirmation used 64 visitor histories not used in discovery
(26100601–26100664) and eight new nested demographic repeats
(26101601–26101608), for 4,096 declared trajectories.

Primary temporal result at threshold 0.05:
- assurance first: **51/64 = 0.796875**
- near-simultaneous: **13/64**
- 95% visitor-history bootstrap: **0.6875–0.890625**

The lower interval bound exceeds 0.50, satisfying the frozen temporal rule.

Primary fixed-assurance result:
- far investment change: **−0.306021**
  [−0.318054, −0.294111]
- far-minus-near investment: **−0.435389**
  [−0.453330, −0.417191]
- near occupancy: **1.0**
- far occupancy: **1.0**
- estimable histories: **64/64**

Both intervals remain wholly below zero and the admissibility rule passes.
Therefore assurance evolution is not required for investment decline in the
declared cell.

Source:
- `data/results/chapter2_1005_confirmatory_replication_20261006.json`

## Criterion 3 — sensitivity of "first" definition: PASS WITH BOUNDED SCOPE

In the confirmed primary cell, assurance-first remains the majority at every
predeclared threshold:

| threshold | assurance first | proportion | 95% history bootstrap |
|---:|---:|---:|---|
| 0.025 | 48/64 | 0.7500 | 0.640625–0.844531 |
| 0.050 | 51/64 | 0.796875 | 0.687500–0.890625 |
| 0.100 | 59/64 | 0.921875 | 0.843750–0.984375 |

Thus the primary conclusion is not an artifact of choosing only the 0.05
threshold within the declared 0.025–0.10 sensitivity range. These thresholds are
diagnostic conventions, not biological phase transitions.

## Criterion 4 — reproductive-setting scope made explicit: PASS

All four setting-by-mutation temporal cells are reported. The result is **not
universal**.

Most importantly, prior selfing with positive mutation at threshold 0.05 gives:
- assurance first: **30/64 = 0.46875**
- near-simultaneous: **34/64**
- 95% bootstrap: **0.34375–0.59375**

This does not satisfy the primary confirmation criterion. The paper therefore
restricts the headline sequence claim to delayed selfing with assurance cost
0.5 and positive mutation. The prior-selfing cell is a scope boundary, not a
failure to be hidden or a result to be averaged away.

## Criterion 5 — unresolved numerical branch separated from the biological claim: PASS

The full positive-mutation high-resolution deterministic/PDE comparison remains
closed unresolved. The 9-to-13 grid refinement failed 31/32 declared endpoint
gates and the later long comparison was stopped after verified update 7.

The confirmed process claim depends on:
1. finite-population maintained-isolation trajectories;
2. the fixed-plant reproductive-return assay; and
3. the fixed-assurance finite-population intervention.

It does **not** require a converged positive-mutation deterministic/PDE
counterpart. The unresolved numerical branch is retained as a claim boundary,
not used as supporting biological evidence.

## Additional criterion 6 — literature distance: CLOSED

The novelty claim has been narrowed against direct precedents.

- Bodbyl Roels & Kelly (2011) already proposed sequential selfing-syndrome
  evolution after pollinator loss. Therefore "assurance/selfing changes first"
  is not the novelty.
- Gervasi & Schiestl (2017) already demonstrated pollinator-driven joint floral
  and mating-system divergence.
- Sakai (1995) predates the present model in attraction/selfing allocation
  theory.
- Ashman et al. (2004), Knight et al. (2005, 2006) and Van Etten et al. (2015)
  establish that pollen limitation, resource allocation, seed production and
  viable reproductive outcome are not interchangeable.

The paper-level contribution is therefore the **separation of realized temporal
order from causal necessity using an explicit intervention in the same
pollination-to-reproduction model**.

Source:
- `docs/CHAPTER2_1005_NOVELTY_AND_LITERATURE_POSITION_20261006.md`

## Additional criterion 7 — overlapping manuscript route: CLOSED

The former Evolution Letters repeatability manuscript is retired as a standalone
active submission route. Its repeatability analyses remain provenance /
complementary material and may enter Supporting Information only with explicit
overlap disclosure.

The historical Oikos submission remains a frozen snapshot and does not define
the current manuscript.

Source:
- `docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md`

## Final adjudication

**Established within model scope: YES.**

What is established:
- sustained visitor-replenishment limitation can generate a confirmed
  assurance-first realized sequence in the declared delayed/costly reproductive
  setting;
- blocking assurance evolution does not prevent investment decline;
- therefore temporal precedence does not identify assurance evolution as a
  necessary cause of attraction loss.

What remains exploratory:
- the attenuation of near–far investment divergence by allowing assurance to
  evolve;
- the full 13-rate response shape as a general ecological law;
- transport of the mechanism to natural island systems.

What is explicitly not established:
- a universal selfing-first rule;
- a natural kilometre or geological-time threshold;
- a complete mediation fraction through realized selfing;
- a causal reconstruction of Chapter 1 regions or named islands;
- a converged positive-mutation deterministic/PDE explanation.
