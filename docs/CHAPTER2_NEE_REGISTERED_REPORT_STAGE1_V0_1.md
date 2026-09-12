# Stage-1 skeleton — Nature Ecology & Evolution Registered Report

Version: v0.4 — 2026-09-13  
Status: **pre-data working surface; H5 countercondition, R5 breadth rule and R1a focal/transport/block architecture frozen; R1b exact site/time admission, R2/R3/R6 remain open**  
Parent promotion lock: `data/design/chapter2_nee_predata_promotion_lock_20260912.json`

## Working title

**When community averaging changes — and fails to change — the determinants of plant reproductive response**

Alternative:

**Plant state, realized pollinator communities and the limits of ecological averaging**

## Stage-1 scientific sentence

> We prospectively test whether plant pre-outcome state and realized effective pollinator composition jointly determine reproductive response, whether that relation propagates through independently measured pollination function and dependency, and whether averaging repeated effective-community opportunities shifts determinant importance only when shared stochastic dependence is sufficiently low for averaging to operate; the frozen mapping is then challenged in a second prospective plant system without retuning.

## Why this is a Registered Report question

The source mechanism and its countercondition are frozen before focal reproductive outcomes:

- realized richness can move coarse regime placement without eliminating branch contingency;
- realized composition × plant starting state remains non-additive after richness control;
- finite-community realization variance changes under aggregation;
- plant-state versus community-realization ranking can reverse in the frozen synthetic sequence;
- correlated/synchronous community realizations can leave a non-shrinking community-variance floor and prevent rank reversal.

The field study therefore tests **both the predicted effect and its predicted failure condition**. It does not calibrate the synthetic model after observing Izu outcomes. Generic `rho=0.25` is a model-specific benchmark, not a natural field threshold.

---

# R1 architecture frozen before site-level admission

## Focal system

The focal natural system is *Campanula microdonta*. Oshima and Kozushima remain the candidate geographic family, not automatically admitted final sites. Oshima is first reconnaissance priority because several named occurrence localities are already source-backed; Kozushima remains necessary to resolve as a post-Oshima focal geography, but its exact current *Campanula* population is not yet admitted.

Current source-backed focal candidate rows are Fudeshima coast, Toshiki coast, Mt. Mihara, the Senzu/Oshima coastal plant community, and one unresolved Kozushima herbarium-level locality. All remain `candidate`; none is `admitted`.

## Prospective transport system

The second prospective context is *Farfugium japonicum*. This taxon was selected before focal reproductive outcomes from source-defined pollen-target membership, high interaction breadth and broad source-site coverage, rather than from agreement with any future *Campanula* effect.

The first-priority transport geography is now **Kozushima**, with Nodo Sainbara-line lighthouse area as the first source-backed locality lead. This priority was revised before focal outcomes using only occurrence evidence, geographic independence, exact-site resolvability and regulatory/field feasibility. Hitachi, Hitachinaka and Tateyama remain contingency transport geography if Kozushima fails the frozen pre-outcome R1b gates; they cannot replace Kozushima because of focal effect direction.

Oshima Nihonmatsu–Shiofuki and the Senzu coastal community remain backup *Farfugium* candidates. A same-archipelago transport is acceptable only if taxon, season, geography and sampling units make it a genuine prospective transport challenge rather than another *Campanula* focal block.

## Block-scale rule

The pre-pilot synthetic screen makes independent block count the main H5 design lever. Under its low-dependence benchmark, crossover separation was `0.5425` at 16 blocks, `0.835` at 32 blocks and `0.900` at 48 blocks. Therefore materially fewer than 32 plausibly independent repeated focal blocks is not preferred for the NEE H5 lane unless R2/R3 later provide stronger empirical information.

This is a **screening floor only**. It is not empirical power and not a final confirmatory sample size.

---

# Confirmatory hypotheses

## H1 — composition beyond amount [P1]

**Prediction:** after controlling for monitored effort, total effective service and predeclared coarse breadth summaries, realized background-controlled effective-community composition retains information for the mature reproductive endpoint.

**Decision:** `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE` under the frozen measurement and precision gates.

## H2 — plant state × realized community [P2; primary relational hypothesis]

**Prediction:** pre-outcome plant functional state interacts non-additively with realized effective-community composition for same-plant reproductive response.

No post-hoc state threshold, visitor regrouping or outcome-informed composition simplification is allowed.

## H3 — functional bridge [P3]

**Prediction:** visitor identity/composition maps to an independent background-controlled measure of pollination effectiveness before the mature reproductive endpoint is evaluated.

Primary intended bridge: single-visit conspecific pollen deposition with valid no-visit/background controls.

## H4 — dependency consequence [P4]

**Prediction:** frozen open-natural, bagged-autonomous and supplemental-outcross contrasts identify whether realized pollination service can alter mature reproductive outcome.

## H5 — conditional determinant-order response to aggregation [P5]

H5 is deliberately two-sided.

### H5a — lower shared dependence

**Prediction:** in prospectively classified lower shared dependence effective-community opportunities, increasing aggregation decreases community-realization contribution and increases plant-state contribution. A state-over-community rank reversal is tested only where the outcome-blind admission rule places the stratum in a crossover-capable domain.

**Support:** both directional redistribution components are supported under adequate measurement and R3 precision; reversal is an additional condition only where pre-admitted.

**Adverse:** adequately measured lower-dependence strata show absent or opposite redistribution after prespecified amount, effort, site and time controls.

### H5b — higher shared dependence

**Prediction:** in prospectively classified higher shared dependence effective-community opportunities, aggregation leaves a persistent community-realization floor, so state-over-community rank reversal is weakened or absent.

**Support:** the frozen higher-dependence stratum retains community dominance or otherwise lacks the predeclared reversal under adequate precision.

**Adverse:** a clear state-over-community rank reversal occurs despite satisfying the frozen higher-dependence admission rule and precision gates.

### H5 stratification rule

Dependence strata, or a continuous dependence-by-aggregation interaction, are frozen from predictor/exposure data before focal reproductive outcomes are opened. Mature seed, dependency effect direction, H1-H4 effects and post-hoc optimization cannot define the dependence coordinate.

If a stable numeric field cutoff cannot be justified outcome-blind, no cutoff is manufactured; the continuous interaction or ordered predeclared strata are retained.

## H6 — *Farfugium* prospective transport [P6; required for NEE route]

**Prediction:** the frozen H2 mapping and outcome-state logic are challenged prospectively in *Farfugium japonicum* without retuning. The same H5 dependence and aggregation coordinates are carried where estimable.

Kozushima is the first-priority transport reconnaissance geography, but no transport row is admitted yet. Existing world/Izu secondary datasets are not admitted as P6 because none supplies the full prospective contract. H6 cannot rescue adverse H1-H5 results and is not required for the already-closed Oikos manuscript.

---

# Methods architecture

## Strict unit and hierarchy

```text
flowers / visits / SVD events within plant
plants within prespecified exposure block
repeated independent blocks within focal Campanula context
plus an independent prospective Farfugium transport context for NEE
```

Plant is the independent precision unit within a block; nominal flower, visit or SVD counts are not independent `n`. Blocks are population/site/time exposure windows fixed before reproductive outcomes and cannot be split, merged or moved after inspecting effectiveness, dependency or mature seed.

## R1b exact scope admission [OPEN]

A source-backed candidate registry now contains 5 focal and 3 transport rows, with **0 admitted**. Candidate rows may preserve `pending` feasibility; unknown is not converted into biological failure.

Before R2 opens, a row can be `admitted` only when it prospectively fixes or verifies:

- actual named *Campanula* or *Farfugium* population/site unit;
- exact site-time block construction;
- eligible flowering-plant screen;
- block-independence basis;
- SVD background-control feasibility;
- open natural pollination feasibility;
- bagged autonomous treatment feasibility;
- supplemental outcross feasibility;
- outcome-blind dependence-coordinate feasibility;
- access, permit and phenology status.

The current audit is `scripts/audit_chapter2_nee_r1_site_registry.py`. It fails closed for admitted rows and treats unresolved candidate feasibility as pending rather than zero.

The Senzu/Oshima coastal plant community is high-friction for manipulation because it is a designated natural monument; occurrence there is useful, but permission is not assumed. Protected-area requirements are resolved site-by-site before admission.

## Effective-community representation [R4 CLOSED]

For block `b` and visitor group `g`:

```text
w_bg = visit_rate_per_flower_hour
       × background_adjusted_single_visit_conspecific_pollen_deposition

p_bg = w_bg / sum_g(w_bg)
```

Missing/uncontrolled effectiveness is unavailable, not zero. Negative background-adjusted weights are not clipped. Zero-total-service blocks remain valid amount/effort observations but do not receive a manufactured composition vector. Total effective service remains separate.

## H5 dependence coordinate

The field dependence/synchronization coordinate must be derived from repeated background-controlled effective-community opportunities and/or prespecified forcing covariates before reproductive outcomes. It can enter as frozen ordered strata or a continuous dependence-by-aggregation interaction.

Forbidden:

- literal import of generic `rho=0.25`;
- a dependence cutoff selected to maximize H5 separation;
- block redefinition after outcome inspection;
- literal mapping of raw richness, Hill diversity or effective-service breadth to synthetic `k`.

## Reproductive treatments and endpoint

Core treatment family:

1. open natural pollination;
2. bagged autonomous treatment;
3. supplemental outcross treatment.

Primary terminal outcome is mature reproductive output linked through plant/flower/fruit IDs. Exact response family is frozen from pilot diagnostics before confirmatory focal analysis.

## Missingness and measurement failure

Zero visits are observations. Missing SVD is not zero effectiveness. Lost treatments remain explicit failure states. Incomplete terminal linkage cannot be silently dropped. Failed support yields `NOT_EVALUABLE`, not biological absence.

---

# Sampling and precision plan

## Pre-pilot H5 operating-characteristics screen — COMPLETE, NOT EMPIRICAL POWER

The frozen synthetic scale screen is stored in `data/results/chapter2_nee_h5_prepilot_oc_20260912.json`.

Lower shared dependence becomes increasingly separable with independent blocks; near-boundary dependence remains difficult even beyond 1000 recruited plants; higher shared dependence increasingly supports the predicted no-crossover side. The bottleneck is therefore **independent repeated blocks and dependence-regime contrast**, not nominal flower/visit counts.

## R2 — pilot role [OPEN]

Pilot work estimates independent plant/block recruitment and retention, monitored effort and zero visits, SVD success/background variance, treatment attrition, mature endpoint completion/dispersion, effective-community support, and empirical support/stability of the frozen dependence coordinate. Pilot outcome direction cannot select predictors or H5 strata.

## R3 — confirmatory precision [OPEN]

After R2 is frozen, hierarchical simulation must establish confirmatory precision/assurance for H2 and the conditional H5 contrasts while preserving plant/block hierarchy and attrition.

**Predeclared retreat line:** if single-system R3 cannot support confirmatory H5, H5 is not weakened. **H1-H4 remain confirmatory** and H5 becomes descriptive/exploratory for the single-system study; confirmatory H5 plus prospective transport breadth is reserved for a later expanded NEE design.

---

# Confirmatory analysis pipeline

## A0 — R1b scope audit

Before field confirmation, verify the named focal and transport site/time registry, block-independence basis, eligible plants, SVD/treatment feasibility and outcome-blind dependence coordinate. Failure keeps the NEE design at `NOT_READY`; it is not a biological result.

## A1 — measurement/admission audit

Report effort, zero-visit windows, visitor resolution, SVD/background coverage, complete-chain plant/block counts, treatment retention and mature endpoint linkage before biological inference.

## A2 — H1 composition beyond amount

Compare the frozen amount/breadth model against the same model retaining R4 effective-community composition.

## A3 — H2 relational test

Estimate the predeclared plant-state × effective-community relation with plants nested in blocks.

## A4 — H3 functional bridge

Estimate background-controlled visitor/group effectiveness before constructing effective-service composition.

## A5 — H4 dependency consequence

Estimate frozen reproductive-treatment contrasts on the mature endpoint.

## A6 — H5 conditional aggregation test

Use only prespecified comparable opportunities: lower shared dependence predicts state contribution up/community contribution down, while higher shared dependence predicts a persistent community floor and weakened/absent reversal. No breakpoint search, outcome-selected dependence threshold, or synthetic `k≈4` field cutoff is allowed.

## A7 — H6 *Farfugium* transport

Apply the same frozen H2 mapping and outcome-state logic to the admitted *Farfugium* context without changing predictor direction or endpoint family. Carry H5 dependence/aggregation rules when the transport context supplies adequate repeated-block support.

---

# Quality-control states

Every confirmatory hypothesis receives exactly one of:

```text
SUPPORTED
FALSIFIED_OR_ADVERSE
NOT_EVALUABLE
```

A higher-dependence context lacking crossover is not automatically a falsification; it is the H5b prediction when the pre-outcome dependence criterion and precision gates pass. Unclassified or inadequately supported blocks are `NOT_EVALUABLE`.

---

# Promotion / retreat rule

```text
R1b exact focal + Farfugium site/time registry passes
+ R2 adequate
+ R3 supports confirmatory H2 and conditional H5
+ R4/R5 locks preserved
    -> NEE Stage-1 route remains eligible

Farfugium transport context infeasible
    -> EL / Ecology route for the single-system prospective study; do not weaken H5

R3 says confirmatory H5 infeasible in one system
    -> H1-H4 remain confirmatory + H5 descriptive/exploratory
       reserve full H5 + transport for later expanded NEE

measurement/support gate fails
    -> NOT_EVALUABLE; do not weaken or retune the theory
```

The current Oikos Chapter 2 paper is unaffected by all future promotion-lane outcomes.

## Final stop rule

> The purpose of the pre-data design is to predict both where the mechanism should appear and where it should fail, before either outcome is observed.
