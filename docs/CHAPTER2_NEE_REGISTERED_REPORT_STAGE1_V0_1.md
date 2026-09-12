# Stage-1 skeleton — Nature Ecology & Evolution Registered Report

Version: v0.2 — 2026-09-12  
Status: **pre-data working surface; H5 countercondition and R5 breadth rule frozen, R1/R2/R3/R6 still open**  
Parent promotion lock: `data/design/chapter2_nee_predata_promotion_lock_20260912.json`

## Working title

**When community averaging changes — and fails to change — the determinants of plant reproductive response**

Alternative:

**Plant state, realized pollinator communities and the limits of ecological averaging**

## Stage-1 scientific sentence

> We prospectively test whether plant pre-outcome state and realized effective pollinator composition jointly determine reproductive response, whether that relation propagates through independently measured pollination function and dependency, and whether averaging repeated effective-community opportunities shifts determinant importance only when shared stochastic dependence is sufficiently low for averaging to operate.

## Why this is a Registered Report question

The source mechanism and its countercondition are frozen before focal reproductive outcomes:

- realized richness can move coarse regime placement without eliminating branch contingency;
- realized composition × plant starting state remains non-additive after richness control;
- finite-community realization variance changes under aggregation;
- plant-state versus community-realization ranking can reverse in the frozen synthetic sequence;
- the generic theorem also predicts a failure domain: correlated/synchronous community realizations can leave a non-shrinking community-variance floor and prevent rank reversal.

The field study therefore tests **both the predicted effect and its predicted failure condition**. It does not calibrate the synthetic model after observing Izu outcomes.

The generic theorem's `rho=0.25` critical value is a model-specific benchmark under frozen coefficients and variances. It is not a field threshold and will not be used to define natural strata.

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

### H5a — lower shared stochastic dependence

**Prediction:** in prospectively classified lower-dependence effective-community opportunities, increasing aggregation decreases community-realization contribution and increases plant-state contribution. A state-over-community rank reversal is tested only where the outcome-blind admission rule places the stratum in a crossover-capable domain.

**Support:** both directional redistribution components are supported under adequate measurement and R3 precision; reversal is an additional condition only where pre-admitted.

**Adverse:** adequately measured lower-dependence strata show absent or opposite redistribution after prespecified amount, effort, site and time controls.

### H5b — higher shared stochastic dependence

**Prediction:** in prospectively classified higher-dependence effective-community opportunities, aggregation leaves a persistent community-realization floor, so state-over-community rank reversal is weakened or absent.

**Support:** the frozen higher-dependence stratum retains community dominance or otherwise lacks the predeclared reversal under adequate precision.

**Adverse:** a clear state-over-community reversal occurs despite satisfying the frozen high-dependence admission rule and precision gates.

### H5 stratification rule

Dependence strata, or a continuous dependence-by-aggregation interaction, are frozen from predictor/exposure data before focal reproductive outcomes are opened. Mature seed, dependency effect direction, H1-H4 effects and post-hoc optimization cannot define the dependence coordinate.

If a stable numeric field cutoff cannot be justified outcome-blind, no cutoff is manufactured; the continuous interaction or ordered predeclared strata are retained.

## H6 — second prospective transport context [P6; required for NEE route]

**Prediction:** the frozen H2/H5 mapping is challenged in at least one second prospective independent natural context without retuning.

Existing world/Izu secondary datasets are not admitted as P6 because none supplies the full prospective contract. The second context may occur in the same archipelago only if it is biologically and sampling-wise independent enough to be a genuine transport challenge rather than another focal block.

H6 cannot rescue adverse H1-H5 results and is not required for the already-closed Oikos manuscript. It is a breadth requirement for keeping the NEE Stage-1 route eligible.

---

# Methods architecture

## Strict unit and hierarchy

```text
flowers / visits / SVD events within plant
plants within prespecified exposure block
repeated blocks within focal context
plus at least one independent prospective transport context for NEE
```

The independent precision unit is the plant; nominal flower, visit or SVD counts are not independent `n`.

Blocks are population/site/time exposure windows fixed before reproductive outcomes. Blocks cannot be split, merged or moved after inspecting effectiveness, dependency or mature-seed outcomes.

## Effective-community representation [R4 CLOSED]

For block `b` and visitor group `g`:

```text
w_bg = visit_rate_per_flower_hour
       × background_adjusted_single_visit_conspecific_pollen_deposition

p_bg = w_bg / sum_g(w_bg)
```

Missing/uncontrolled effectiveness is unavailable, not zero. Negative background-adjusted weights are not clipped. Zero-total-service blocks remain valid amount/effort observations but do not receive a manufactured composition vector. Total effective service remains a separate amount term.

## H5 dependence coordinate

The field dependence/synchronization coordinate must be derived from repeated background-controlled effective-community opportunities and/or prespecified forcing covariates before reproductive outcomes. It can enter as frozen ordered strata or a continuous dependence-by-aggregation interaction.

Forbidden:

- literal import of generic `rho=0.25`;
- dependence cutoff selected to maximize H5 separation;
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

Its role is only to decide whether R1 is remotely plausible before a field season. Under the generic benchmark:

- low shared dependence becomes increasingly separable as the number of independent blocks increases;
- near-boundary dependence remains difficult even with more than 1000 recruited plants;
- high shared dependence increasingly supports the predicted no-crossover side.

This establishes the design bottleneck: **independent repeated blocks and dependence-regime contrast matter more for H5 than nominal flower/visit counts**. The rates are not empirical power and cannot justify the final Stage-1 sample size.

## R2 — pilot role [OPEN]

Pilot work estimates:

- independent plant and block recruitment/retention;
- monitored effort and zero visits;
- SVD measurement success/background variance;
- treatment attrition;
- mature endpoint completion/dispersion;
- effective-community support;
- empirical support and stability of the frozen dependence coordinate/strata.

Pilot outcome direction cannot select predictors or H5 strata.

## R3 — confirmatory precision [OPEN]

After R2 is frozen, hierarchical simulation must establish confirmatory precision/assurance for H2 and the conditional H5 contrasts, preserving plant/block hierarchy and attrition.

**Predeclared retreat line:** if single-system R3 cannot support confirmatory H5, H5 is not weakened. H1-H4 remain confirmatory and H5 becomes descriptive/exploratory for the single-system study; confirmatory H5 plus transport breadth is reserved for a later expanded NEE design.

---

# Confirmatory analysis pipeline

## A1 — measurement/admission audit

Report effort, zero-visit windows, visitor resolution, SVD/background coverage, complete-chain plant/block counts, treatment retention and mature endpoint linkage before biological inference.

## A2 — H1 composition beyond amount

Compare the frozen amount/breadth model against the same model retaining R4 effective-community composition.

## A3 — H2 relational test

Estimate the predeclared plant-state × effective-community relation with plants nested in blocks.

## A4 — H3 functional bridge

Estimate background-controlled visitor/group effectiveness before constructing effective-service composition.

## A5 — H4 dependency consequence

Estimate the frozen reproductive-treatment contrasts on the mature endpoint.

## A6 — H5 conditional aggregation test

Use only prespecified comparable exposure opportunities. Evaluate the frozen dependence-by-aggregation prediction:

- lower shared dependence: state contribution up, community contribution down, with reversal tested only where pre-admitted;
- higher shared dependence: persistent community floor / weakened or absent reversal.

No breakpoint search, outcome-selected dependence threshold, or synthetic `k≈4` field cutoff is allowed.

## A7 — H6 prospective transport

Apply the same frozen H2/H5 mapping to the second prospective natural context without changing predictor direction, dependence definition, endpoint family or aggregation rule.

---

# Quality-control states

Every confirmatory hypothesis receives exactly one of:

```text
SUPPORTED
FALSIFIED_OR_ADVERSE
NOT_EVALUABLE
```

A high-dependence block lacking crossover is not automatically a falsification of H5; it is the H5b prediction when the pre-outcome dependence criterion and precision gates are satisfied. Unclassified or inadequately supported blocks are `NOT_EVALUABLE`.

No secondary analysis can rescue a failed primary gate.

---

# R5 breadth rule — CLOSED

For the NEE route, at least one second prospective independent natural context is required. Existing secondary literature remains design/transport triage only.

The exact focal and transport contexts are selected in R1 before focal confirmatory reproductive outcomes.

If no second context is feasible, do not broaden literature hunting or retrofit secondary data as P6. Route the strong single-system prospective study to Ecology Letters, Ecology, or another appropriate general-ecology venue.

---

# Open items before Stage-1 readiness

1. **R1:** focal taxon/population/site/time/block universe plus second prospective transport context and outcome-blind dependence coordinate;
2. **R2:** empirical feasibility, dispersion, attrition and dependence-support pilot;
3. **R3:** confirmatory H2/H5 precision/assurance and replication;
4. **R6:** permits, ethics, archive, protocol-registration, authorship and operational randomization/blinding details.

R4, R5 strategy, P1-P4 and the conditional H5 scientific logic are closed to outcome-driven revision.

---

# Promotion / retreat rule

```text
R1 supplies focal + second prospective context
+ R2 adequate
+ R3 supports confirmatory H2 and conditional H5
+ R4/R5 locks preserved
    -> NEE Stage-1 route remains eligible

second prospective context infeasible
    -> EL / Ecology route for the single-system prospective study

R3 says confirmatory H5 infeasible in one system
    -> H1-H4 confirmatory + H5 descriptive/exploratory
       reserve full H5 + transport for later expanded NEE

measurement/support gate fails
    -> NOT_EVALUABLE; do not weaken or retune the theory
```

The current Oikos Chapter 2 paper is unaffected by all future promotion-lane outcomes.

## Final stop rule

> The purpose of the pre-data design is to predict both where the mechanism should appear and where it should fail, before either outcome is observed.
