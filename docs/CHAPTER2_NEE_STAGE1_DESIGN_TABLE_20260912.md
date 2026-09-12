# Chapter 2 NEE Registered Report Stage-1 design table — pre-data working surface

Version: v0.2 — 2026-09-12  
Status: **pre-data design table; P1-P4, conditional P5/H5, R4 and the R5 breadth rule are frozen; R1/R2/R3 and R6 remain open**

Parent contracts:

- `data/design/chapter2_nee_predata_promotion_lock_20260912.json`
- `data/design/chapter2_nee_effective_community_representation_lock_20260912.json`
- `data/design/chapter2_nee_h5_correlation_stratification_lock_20260912.json`
- `data/design/chapter2_nee_r5_transport_decision_20260912.json`
- `data/design/chapter2_nee_h5_prepilot_oc_freeze_20260912.json`
- `data/design/izu_transition_linked_estimand_lock_20260909.json`
- `data/design/izu_effective_service_rank_crossover_lock_20260911.json`

This table is the working hypothesis table for a possible Nature Ecology & Evolution Stage-1 Registered Report. It does not invent confirmatory sample sizes or pilot dispersion values before R2/R3 are complete. The pre-pilot H5 operating-characteristics screen is an order-of-magnitude triage only, not empirical power.

## Global unit and outcome-state rules

- strict linked unit: `block_id x plant_id`;
- independent precision unit: plant, with plants nested in prespecified blocks;
- flowers, visits and SVD events are within-plant/block subsamples, not independent `n`;
- blocks and any dependence/synchronization strata are fixed from outcome-blind exposure information before reproductive outcomes are opened;
- confirmatory states are `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE`;
- a failed measurement/support gate cannot be converted into a biological null;
- effect direction cannot be used to redefine predictors, visitor groups, blocks, dependence strata, thresholds or endpoint families;
- the generic-theory value `rho=0.25` is a model-specific benchmark, **not** a natural cutoff and cannot be imported as a field threshold.

## Mandatory hypothesis/design table

| Hypothesis | Confirmatory prediction | Primary predictor / contrast | Primary outcome or intermediate | Unit / hierarchy | Outcome-neutral admission gate | Frozen analysis family | Confirmatory interpretation |
|---|---|---|---|---|---|---|---|
| **H1 / P1 — composition beyond amount** | Realized effective-community composition retains information after coarse amount/breadth controls. | Background-controlled effective-service composition vector; compare model/estimand with composition against the same model without composition, retaining monitored effort, total effective service and predeclared coarse breadth terms. | Mature reproductive endpoint; dependency response may be reported as a linked secondary endpoint. | Plants nested in prespecified blocks. | Q1 effort adequate; Q2 effective-service composition available under the R4 lock; Q4 endpoint linkage adequate; Q5 replication/precision adequate. | Frozen hierarchical response model plus predeclared inferential or out-of-block predictive comparison. No group selection from focal outcomes. | `SUPPORTED` if the predeclared composition contribution criterion is met under adequate measurement; `FALSIFIED_OR_ADVERSE` if it is not met under adequate measurement; `NOT_EVALUABLE` if composition/support/precision gates fail. |
| **H2 / P2 — plant state × realized community** **PRIMARY** | Pre-outcome plant functional state interacts non-additively with realized effective-community composition for same-plant reproductive response. | Pre-outcome same-plant functional state × full predeclared effective-service composition as a joint relational term. | Same-plant mature reproductive response, with dependency linkage retained. | `block_id x plant_id`; plant is the independent precision unit. | Q2 composition available; plant state measured before outcome; adequate support across the state × composition design; Q4/Q5/Q6 pass. | Prespecified hierarchical joint interaction / relational contrast, assessed by the Stage-1 inferential or out-of-block predictive criterion. No post-hoc state threshold or composition simplification. | `SUPPORTED` only if the joint relational criterion is met; `FALSIFIED_OR_ADVERSE` if an adequately measured design shows negligible/adverse relational contribution; `NOT_EVALUABLE` if Q2/Q6 or support fails. |
| **H3 / P3 — functional bridge** | Visitor identity/composition maps to an independent pollination-effectiveness intermediate before the mature endpoint is evaluated. | Visitor group/taxon identity and visit exposure under frozen resolution rules. | Background-controlled single-visit conspecific pollen deposition; rate-weighted effective service derived only after its measurement gate passes. | SVD events within plants/blocks; visitor-group effectiveness is not inferred from seed outcome. | Confirmed first visit; valid no-visit background controls; declared pollen-count QC; sufficient controlled SVD support for visitor groups used. | Frozen background-controlled SVD/effectiveness model; no seed/dependency-informed visitor regrouping. | `SUPPORTED` if visitor/community exposure maps to the independent functional intermediate under the predeclared criterion; `FALSIFIED_OR_ADVERSE` if it does not with adequate SVD support; `NOT_EVALUABLE` if SVD control/reliability fails. |
| **H4 / P4 — reproductive dependency consequence** | Reproductive treatment contrasts identify whether realized pollination service can alter mature reproductive outcome. | Core treatment family: open natural pollination, bagged autonomous, supplemental outcross; any single-visit-then-bagged arm must be frozen before confirmatory execution. | Mature fruit/seed endpoint linked by plant/flower/fruit IDs. | Treatment flowers nested within tagged plants, plants within blocks. | Q3 allocation/retention adequate; treatment failures/losses explicit; Q4 mature endpoint linkage adequate; donor and bagging rules pass. | Frozen hierarchical treatment-contrast model using the R2/R3-selected endpoint family and precision rule. | `SUPPORTED` if the declared dependency contrast is estimable and meets the predeclared criterion; `FALSIFIED_OR_ADVERSE` if adequate data show no declared dependency consequence; `NOT_EVALUABLE` if treatment or endpoint gates fail. |
| **H5a / P5 — low shared-dependence aggregation** | In prospectively classified lower-shared-dependence exposure strata, aggregation across comparable opportunities should decrease community-realization contribution and increase plant-state contribution. State-over-community reversal is tested only where the outcome-blind admission rule places the stratum in a crossover-capable domain. | Outcome-blind effective shared stochastic dependence/synchronization × prespecified exposure aggregation; never literal synthetic `k`, raw richness, or a post-hoc field `rho` cutoff. | Relative contributions of plant state, realized effective-community composition and their non-additive relation. | Plants nested in repeated prespecified blocks; aggregation uses only declared comparable opportunities. | R4 composition available; dependence coordinate/stratum frozen from exposure data before focal reproductive outcomes; repeated-block support adequate; Q5 precision passes. | Prespecified dependence-by-aggregation interaction and/or contribution decomposition. No breakpoint search. | `SUPPORTED` requires both directional redistribution components; state-over-community reversal is additionally evaluated only when pre-admitted. `FALSIFIED_OR_ADVERSE` requires adequate low-dependence support and precision with absent/opposite redistribution. Otherwise `NOT_EVALUABLE`. |
| **H5b / P5 — high shared-dependence countercondition** | In prospectively classified higher-shared-dependence exposure strata, aggregation should leave a persistent community-realization floor, weakening or preventing state-over-community reversal. | Same frozen dependence/synchronization coordinate and aggregation rule as H5a. | Same contribution decomposition as H5a. | Same repeated-block hierarchy. | High-dependence admission rule frozen before outcomes; repeated-block/support and Q5 precision gates pass. | Same frozen H5 analysis family; no outcome-selected cutoff or regrouping. | `SUPPORTED` if the predeclared high-dependence stratum retains community dominance or otherwise lacks the state-over-community reversal under adequate precision. `FALSIFIED_OR_ADVERSE` if a clear reversal occurs despite the frozen high-dependence condition. Otherwise `NOT_EVALUABLE`. |
| **H6 / P6 — independent prospective transport** **REQUIRED FOR NEE ROUTE** | The frozen H2/H5 mapping is challenged in at least one second prospective independent natural context without retuning. | Same frozen plant-state × effective-community and dependence/aggregation mapping applied externally. | Prespecified comparable reproductive endpoint. | Second natural context with genuinely independent biological/sampling units; may be within the same archipelago only if it is not merely another focal block. | Context selected outcome-blind during R1 and before focal confirmatory outcomes; same mapping is feasible; no outcome-driven remapping. | Apply the frozen mapping without changing predictor direction, dependence definition, endpoint family or aggregation rule. | `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE` under the same gate logic. H6 is required to keep the NEE route eligible but cannot rescue adverse H1-H5 results. Existing secondary metadata do not count as P6. |

## Cross-hypothesis quality gates

| Gate | Requirement | Failure state |
|---|---|---|
| **Q1 effort** | usable monitored flower-hours recorded and zero-visit windows retained | affected exposure analyses `NOT_EVALUABLE` if the predeclared minimum support is not met |
| **Q2 effectiveness** | sufficient background-controlled SVD coverage for the R4 effective-community representation | H1/H2/H5 composition-dependent claims `NOT_EVALUABLE` if overall support fails |
| **Q3 dependency** | core reproductive treatments assigned and retained under the frozen within-plant/block scheme | H4 and dependent downstream claims `NOT_EVALUABLE` if support fails |
| **Q4 endpoint** | terminal mature-fruit/seed linkage complete enough for the frozen endpoint | endpoint-dependent claims `NOT_EVALUABLE` if linkage fails |
| **Q5 replication** | independent plants and repeated prespecified blocks satisfy the R3 precision/assurance rule for the dependence-conditioned H5 contrasts | confirmatory H5 decision withheld |
| **Q6 prediction** | primary H2 and H5 estimands are identifiable without post-hoc model simplification or outcome-selected strata | H2/H5 and NEE promotion `NOT_EVALUABLE` |
| **Q7 breadth** | a second prospective independent natural context is feasible under the same frozen mapping | NEE route closes; retain the single-system study for EL/Ecology rather than weakening H5 |

## H5 pre-pilot operating-characteristics screen

The frozen pre-pilot screen (`data/results/chapter2_nee_h5_prepilot_oc_20260912.json`) exists only to determine design scale before R1. It is **not empirical R3 power**.

Under the generic benchmark, low shared dependence became increasingly separable with more independent blocks, whereas a near-boundary dependence benchmark remained difficult even above 1000 recruited plants. High shared dependence increasingly supported the predicted no-crossover side. The actionable conclusion is therefore not a final `n`: **independent repeated blocks and dependence-regime contrast are the H5 bottleneck**.

If empirical R3 later shows that the single focal system cannot estimate H5 with the frozen precision rule, H5 is not weakened. H1-H4 may remain confirmatory and H5 become descriptive/exploratory for a strong single-system EL/Ecology study; confirmatory H5 plus transport breadth is reserved for a later expanded NEE design.

## Items intentionally not numerically filled yet

The following remain open until R2/R3:

- confirmatory number of plants and blocks;
- minimum controlled SVD support by visitor group;
- terminal endpoint distribution family if pilot diagnostics are needed to choose among prespecified families;
- smallest scientifically useful precision/effect target;
- confirmatory decision threshold for the chosen inferential/predictive criterion;
- attrition and treatment-loss stress assumptions;
- empirical support/precision for the outcome-blind H5 dependence strata or continuous dependence interaction.

Synthetic operating characteristics cannot substitute for empirical pilot-frozen R3 precision planning.

## R1 implication

R5's breadth rule is already closed. R1 must now freeze both the focal and transport field scope. The `taxon x population/site x time-window x block` universe must supply:

1. multiple independent plants per retained block;
2. enough independent repeated exposure blocks for H5 rather than only more flowers/visits within blocks;
3. outcome-independent variation in effective-community composition for H2;
4. outcome-blind variation in effective shared dependence/synchronization so H5a and H5b are prospectively distinguishable, or a predeclared continuous dependence-by-aggregation analysis;
5. feasible SVD background controls and all three core reproductive treatments;
6. at least one second prospective independent natural context if the NEE route is retained;
7. exclusion reasons based on access, phenology, feasibility or measurement QC, never reproductive effect direction.

If R1 cannot instantiate both the H5 contrast and the second prospective context, the correct decision is to close the NEE route for the single-system study rather than retrofit the hypothesis after pilot investment.
