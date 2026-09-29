# Chapter 2 submission-route firewall — 2026-09-12

Status: **three lanes separated; current Oikos paper remains closed except author metadata/confirmations. Lane B has reached an EL-ready analytical candidate state but remains downstream of Lane A submission/disclosure.**

## Purpose

Recent work created two legitimate escalation paths beyond the current Chapter 2 manuscript. Those paths must not reopen or silently redefine the already closed Oikos paper.

1. **Lane A — current Oikos Research Paper**
2. **Lane B — Ecology Letters general-theory candidate**
3. **Lane C — prospective natural validation / NEE Stage-1 lane**

## Lane A — current Oikos paper

Scientific chain:

```text
R1 regime-dependent response architecture
→ R2 real-world compositional exposure
→ R3 Izu biological consequence
```

Current R1:

```text
small stochastic community → community-realization dominated
larger finite community under active adjustment → starting-state dominated while branching persists
deterministic mean-field limit → stochastic branching disappears
```

The synthetic crossover near `k=4` is model-specific, not a natural threshold.

Current conceptual claim: island syndromes are **ensemble-level response regimes with regime-dependent variance architecture**, not deterministic lineage-level phenotype rules.

R2 and R3 do not provide one matched historical visitor → deposition → dependency → mature-seed transition chain. That missing chain limits causal interpretation but is not a blocker for this paper.

Closure:

```text
scientific analysis = CLOSED
submission surface = CLOSED
remaining blockers = author-supplied metadata / confirmations only
```

Canonical Lane A manuscript: `docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`.

Do not reopen synthetic calibration, add retrospective significance hunting, or require prospective field data for Lane A.

## Lane B — Ecology Letters candidate

This is a separate general-theory manuscript object, not the island-syndrome paper with a more ambitious title.

Active Lane B surfaces:

- manuscript: `docs/CHAPTER2_EL_LETTER_DRAFT_V0_4_20260913.md`;
- cover letter / overlap disclosure: `docs/CHAPTER2_EL_COVER_LETTER_DRAFT_V0_4_20260913.md`;
- first higher-order freeze: `data/design/chapter2_el_higher_order_sufficiency_freeze_20260913.json`;
- fresh mixed-feedback freeze: `data/design/chapter2_el_mixed_feedback_validation_freeze_20260913.json`;
- result receipt: `data/results/chapter2_el_higher_order_sufficiency_20260913.json`.

Primary statement:

> Variance-equivalent effective independence is an exact second-order coordinate, but it is not generally a sufficient ecological state descriptor. Equal `k_eff` leaves higher cumulants and discrete support unconstrained; those omitted dimensions change community versus state-by-community response whenever pure and mixed response geometry are not proportionally aligned.

The analytical spine is now explicit rather than simulation-only:

```text
bilinear exact null
→ equal k_eff fixes κ2 but not κ3/κ4
→ exact quadratic functional-ANOVA condition for C/I sensitivity
→ failed scalar-curvature prediction retained
→ fresh full-factorial feedback intervention on previously unused seeds
→ support and higher-order distributional failure routes kept distinct
```

The exact quadratic extension identifies the finite-order condition. For centered independent state `X` and community coordinate `Z`,

```text
C = b²τ + bd μ3 + (d²/4) Var(Z²)
I = Var(X)[c²τ + ce μ3 + (e²/4) Var(Z²)]
```

and, for symmetric `Z` at fixed `τ`, the sign of the higher-moment effect on `I/C` is controlled by `e²b² − c²d²`. Thus the bilinear invariant is a special aligned case, not a generic nonlinear law.

The first prespecified setting-level predictor—larger Holling fourth-order curvature should produce more C/I reversal—was **not supported** and remains visible in the audit trail. A revised mixed-feedback prediction was then frozen before six previously unused seeds were executed across all 18 parameter blocks. Feedback knockout produced `0/108` C/I reversals; active adjustment produced `52/108`, with 52 positive paired differences and zero negative pairs. This is fresh synthetic mechanism validation, not empirical ecological prevalence.

Chapter 2 plant–pollinator results remain one nonlinear motivating system in Lane B. The shared six-seed `k` scaling is not a new EL result and must be disclosed as shared with Lane A. Lane B's new contribution is the sufficiency question, higher-order derivation, mixed-response condition, structurally separate consumer–resource model, failed predictor, fresh feedback intervention, and equal-`k_eff` challenge.

Do not rename/restructure Lane A merely because Lane B is stronger. Lane B may proceed to EL only with explicit companion-manuscript disclosure. If Lane A has not yet been submitted, the cover letter must state its exact status; preferred routing remains **Lane A first, Lane B second**.

## Lane C — prospective natural validation / NEE lane

Target chain:

```text
block visitor community
→ single-visit deposition / independent effectiveness
→ dependency
→ mature reproductive output
```

Primary unit: `block_id × plant_id`. Same plant is required across linked outcomes; same flower is not required because SVD is destructive.

Lane C tests whether effective-community composition predicts response beyond coarse amount, whether pre-outcome plant state × realized effective community predicts residual branch identity, whether visitor effectiveness propagates through dependency to mature reproductive output, and whether determinant ordering changes as independent effective exposure is increasingly aggregated.

Natural visitor richness, Hill diversity or flower-hours must not be mapped literally onto synthetic `k`.

NEE Stage 1 requires its own field scope, pilot feasibility/dispersion, confirmatory precision/assurance, primary effective-community representation and administrative/protocol commitments. Future data may limit or strengthen transport; they are not required to rescue Lane A.

## Cross-lane firewall

Forbidden:

- future NEE pilot outcomes retuning the frozen synthetic mechanism;
- synthetic `k≈4` being presented as a natural threshold;
- Oikos R2/R3 being presented as the matched transition chain required by Lane C;
- current Izu patterns being presented as empirical proof of the generic EL theorem;
- shared Lane A scaling output being presented as newly generated EL evidence;
- erasing the failed Lane B scalar-curvature prediction after the fresh feedback result;
- weakening Lane A merely because stronger future lanes exist;
- author metadata incompleteness being treated as scientific non-closure.

Allowed:

- use Lane A as the motivating nonlinear example in Lane B while explicitly disclosing shared provenance;
- add genuinely separate analytical and synthetic-validation objects to Lane B without modifying Lane A inference;
- derive Lane C predictions from frozen Lane A/B theory before outcomes open;
- let null/adverse Lane C results limit transport without rewriting the original mechanism;
- keep all three lanes in one repository while their submission surfaces and claim contracts remain distinct.

## Immediate routing

```text
NOW: finish/submit Lane A once author metadata are supplied
PARALLEL THEORY: complete Lane B V0.4 CI/reviewer audit, but submit it after Lane A or with explicit Lane A status disclosure
PROSPECTIVE FIELD: develop Lane C as a separate pre-data/Stage-1 object; do not make it a blocker for Lane A
```

This routing remains active until a new evidence package explicitly changes an admission gate.