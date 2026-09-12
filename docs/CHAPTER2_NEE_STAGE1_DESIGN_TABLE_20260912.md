# Chapter 2 NEE Registered Report Stage-1 design table — pre-data working surface

Version: v0.1 — 2026-09-12  
Status: **pre-data design table; scientific hypotheses frozen, R1/R2/R3 feasibility and precision details still open**

Parent contracts:

- `data/design/chapter2_nee_predata_promotion_lock_20260912.json`
- `data/design/chapter2_nee_effective_community_representation_lock_20260912.json`
- `data/design/izu_transition_linked_estimand_lock_20260909.json`
- `data/design/izu_effective_service_rank_crossover_lock_20260911.json`

This table is the working hypothesis table required for a Nature Ecology & Evolution Stage-1 Registered Report. It does not invent confirmatory sample sizes or pilot dispersion values before R2/R3 are complete.

## Global unit and outcome-state rules

- strict linked unit: `block_id x plant_id`;
- independent precision unit: plant, with plants nested in prespecified blocks;
- flowers, visits and SVD events are within-plant/block subsamples, not independent `n`;
- blocks are fixed population/site/time exposure windows before reproductive outcomes are known;
- confirmatory states are `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE`;
- a failed measurement/support gate cannot be converted into a biological null;
- effect direction cannot be used to redefine predictors, visitor groups, blocks, thresholds or endpoint families.

## Mandatory hypothesis/design table

| Hypothesis | Confirmatory prediction | Primary predictor / contrast | Primary outcome or intermediate | Unit / hierarchy | Outcome-neutral admission gate | Frozen analysis family | Confirmatory interpretation |
|---|---|---|---|---|---|---|---|
| **H1 / P1 — composition beyond amount** | Realized effective-community composition retains information after coarse amount/breadth controls. | Background-controlled effective-service composition vector; compare model/estimand with composition against the same model without composition, retaining monitored effort, total effective service and predeclared coarse breadth terms. | Mature reproductive endpoint; dependency response may be reported as a linked secondary endpoint. | Plants nested in prespecified blocks. | Q1 effort adequate; Q2 effective-service composition available under the R4 lock; Q4 endpoint linkage adequate; Q5 replication/precision adequate. | Frozen hierarchical response model plus predeclared inferential or out-of-block predictive comparison. No group selection from focal outcomes. | `SUPPORTED` if the predeclared composition contribution criterion is met under adequate measurement; `FALSIFIED_OR_ADVERSE` if it is not met under adequate measurement; `NOT_EVALUABLE` if composition/support/precision gates fail. |
| **H2 / P2 — plant state × realized community** **PRIMARY** | Pre-outcome plant functional state interacts non-additively with realized effective-community composition for same-plant reproductive response. | Pre-outcome same-plant functional state × full predeclared effective-service composition as a joint relational term. | Same-plant mature reproductive response, with dependency linkage retained. | `block_id x plant_id`; plant is the independent precision unit. | Q2 composition available; plant state measured before outcome; adequate support across the state × composition design; Q4/Q5/Q6 pass. | Prespecified hierarchical joint interaction / relational contrast, assessed by the Stage-1 inferential or out-of-block predictive criterion. No post-hoc state threshold or composition simplification. | `SUPPORTED` only if the joint relational criterion is met; `FALSIFIED_OR_ADVERSE` if an adequately measured design shows negligible/adverse relational contribution; `NOT_EVALUABLE` if Q2/Q6 or support fails. |
| **H3 / P3 — functional bridge** | Visitor identity/composition maps to an independent pollination-effectiveness intermediate before the mature endpoint is evaluated. | Visitor group/taxon identity and visit exposure under the frozen resolution rules. | Background-controlled single-visit conspecific pollen deposition; rate-weighted effective service derived only after its measurement gate passes. | SVD events within plants/blocks; visitor-group effectiveness is not inferred from seed outcome. | Confirmed first visit; valid no-visit background controls; declared pollen-count QC; sufficient controlled SVD support for the visitor groups used. | Frozen background-controlled SVD/effectiveness model; no seed/dependency-informed visitor regrouping. | `SUPPORTED` if visitor/community exposure maps to the independent functional intermediate under the predeclared criterion; `FALSIFIED_OR_ADVERSE` if it does not with adequate SVD support; `NOT_EVALUABLE` if SVD control/reliability fails. |
| **H4 / P4 — reproductive dependency consequence** | Reproductive treatment contrasts identify whether realized pollination service can alter mature reproductive outcome. | Core treatment family: open natural pollination, bagged autonomous, supplemental outcross; any single-visit-then-bagged arm must be frozen before confirmatory execution. | Mature fruit/seed endpoint linked by plant/flower/fruit IDs. | Treatment flowers nested within tagged plants, plants within blocks. | Q3 allocation/retention adequate; treatment failures/losses explicit; Q4 mature endpoint linkage adequate; donor and bagging rules pass. | Frozen hierarchical treatment-contrast model using the R2/R3-selected endpoint family and precision rule. | `SUPPORTED` if the declared dependency contrast is estimable and meets the predeclared criterion; `FALSIFIED_OR_ADVERSE` if adequate data show no declared dependency consequence; `NOT_EVALUABLE` if treatment or endpoint gates fail. |
| **H5 / P5 — determinant-order shift with exposure aggregation** | With broader and/or more stable effective service across prespecified independent exposure opportunities, plant-state contribution increases while community-realization contribution decreases; state × community non-additivity remains reported. | Effective-service breadth and repeated-block service-realization stability as context modifiers; never literal synthetic `k`. | Relative contribution of starting state, realized effective-community composition and their non-additive relation to the reproductive response. | Plants nested in repeated prespecified exposure blocks; aggregation uses only declared independent opportunities. | Same-block E3 chain observed; R4 composition available; repeated comparable blocks support stability/aggregation; Q5 precision and support pass. | Hierarchical out-of-block predictive comparison or prespecified variance/contribution decomposition across exposure-defined levels. No breakpoint search and no field cutoff near synthetic `k≈4`. | `SUPPORTED` requires both directional redistribution components under adequate support: state contribution increases and community contribution decreases. `FALSIFIED_OR_ADVERSE` if redistribution is absent/reversed or explained by prespecified effort/amount/site/time controls. `NOT_EVALUABLE` if repeated-block/support gates fail. |
| **H6 / P6 — independent transport** **ESCALATION** | The H2 mapping is challenged in at least one independent natural context or untouched external dataset without retuning. | Same frozen plant-state × effective-community mapping applied externally. | External system's prespecified comparable reproductive endpoint. | External natural system/dataset with its own independent units. | Dataset admitted before focal Izu outcome inspection and satisfies the frozen minimum mapping; no outcome-driven remapping. | Apply the H2 mapping without changing predictor direction, threshold, endpoint definition or aggregation rule. | `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE` under the same gate logic. H6 strengthens breadth but does not rescue or invalidate H1–H5. |

## Cross-hypothesis quality gates

| Gate | Requirement | Failure state |
|---|---|---|
| **Q1 effort** | usable monitored flower-hours recorded and zero-visit windows retained | affected exposure analyses `NOT_EVALUABLE` if the predeclared minimum support is not met |
| **Q2 effectiveness** | sufficient background-controlled SVD coverage for the R4 effective-community representation | H1/H2/H5 composition-dependent claims `NOT_EVALUABLE` if overall support fails |
| **Q3 dependency** | core reproductive treatments assigned and retained under the frozen within-plant/block scheme | H4 and dependent downstream claims `NOT_EVALUABLE` if support fails |
| **Q4 endpoint** | terminal mature-fruit/seed linkage complete enough for the frozen endpoint | endpoint-dependent claims `NOT_EVALUABLE` if linkage fails |
| **Q5 replication** | independent plants and repeated prespecified blocks satisfy the R3 precision/assurance rule | confirmatory effect decision withheld |
| **Q6 prediction** | the primary H2 state × effective-community estimand is identifiable without post-hoc model simplification | H2 and NEE promotion `NOT_EVALUABLE` |

## Items intentionally not numerically filled yet

The following cells are **not missing design work**; they are waiting for the declared R2/R3 state transition:

- confirmatory number of plants and blocks;
- minimum controlled SVD support by visitor group;
- terminal endpoint distribution family if pilot diagnostics are needed to choose among prespecified families;
- smallest effect/precision target for H2;
- numerical decision threshold for the chosen inferential/predictive criterion;
- attrition and treatment-loss stress assumptions.

These are locked only after pilot feasibility/dispersion summaries are frozen. Synthetic operating characteristics are not substituted for empirical power.

## R1 implication

The confirmatory field scope cannot be chosen only by island labels. R1 must predeclare a `taxon x population/site x time-window x block` universe that supplies:

1. multiple independent plants per retained block;
2. repeated prespecified exposure opportunities rather than a single island snapshot;
3. outcome-independent variation in effective-community composition for H2;
4. repeated comparable blocks if H5 stability/aggregation remains confirmatory;
5. feasible SVD background controls and all three core reproductive treatments;
6. exclusion reasons based on access, phenology, plant/treatment feasibility or measurement QC, never on favorable reproductive outcomes.

This table therefore turns R1 from a geographic itinerary into an identifiability and feasibility specification.
