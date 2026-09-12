# Chapter 2 NEE Stage-1 readiness — 2026-09-13

Status: **source mechanism, P1-P4, conditional H5, R4, R5, and R1a focal/transport/block architecture are CLOSED; R1b exact site/time admission, R2/R3 and R6 remain OPEN.**

The current Oikos Chapter 2 paper remains scientifically closed. Nothing in this future NEE lane is a completion gate for that paper.

## Current state first

| Component | State | Current meaning |
|---|---|---|
| source mechanism | CLOSED | do not reopen or retune |
| P1-P4 | CLOSED | preserve |
| H5 conditional two-sided prediction | **CLOSED** | lower shared dependence predicts redistribution/crossover-capable behavior; higher shared dependence can preserve a community-variance floor |
| same-block E1-E4 measurement architecture | CLOSED | preserve |
| effective-community primary encoding | **CLOSED** | R4 background-controlled effective-service composition |
| R5 breadth strategy | **CLOSED** | second prospective independent context required for NEE |
| H5 pre-pilot scale screen | COMPLETE | order-of-magnitude triage only; not empirical power |
| R1a focal/transport/block architecture | **CLOSED** | focal *Campanula microdonta*; transport *Farfugium japonicum*; block-scale rules frozen |
| R1b source-backed candidate registry | SEEDED | 5 focal + 3 transport candidate rows; **0 admitted** |
| R1b exact population/site/time admission | **OPEN** | next mainline |
| pilot dispersion/attrition/dependence support | **OPEN** | R2 |
| confirmatory precision/power | **OPEN** | R3 |
| permits/authorship/admin | **OPEN** | R6 |

Canonical R1 surfaces:

- `data/design/chapter2_nee_r1_scope_architecture_20260913.json`
- `data/design/chapter2_nee_r1_site_registry_candidates_20260913.csv`
- `data/design/chapter2_nee_r1b_candidate_priority_lock_20260913.json`
- `templates/chapter2_nee_r1_site_registry_template.csv`
- `scripts/audit_chapter2_nee_r1_site_registry.py`

## What cannot be reopened

- focal taxon = `Campanula microdonta`;
- prospective transport taxon = `Farfugium japonicum`;
- strict linked unit = `block_id x plant_id`;
- R4 primary community object = background-controlled effective-service composition vector;
- total effective service remains a separate amount term;
- negative background-adjusted weights are not clipped;
- zero visits remain observations;
- missing/uncontrolled SVD is not biological zero;
- failed/lost reproductive treatments remain explicit failure states;
- generic `rho=0.25` is a model-specific theorem benchmark, **not** a field cutoff;
- synthetic `k` is never mapped literally to visitor richness, Hill diversity, or field aggregation;
- P6 cannot be manufactured from current retrospective metadata;
- focal or transport sites cannot be chosen from future reproductive effect direction;
- if R3 cannot support confirmatory H5, **do not weaken H5** to preserve the NEE label.

## H5 — conditional prediction CLOSED; empirical precision OPEN

### Lower shared dependence

With prospectively classified lower shared dependence, aggregation should reduce community-realization contribution and increase plant-state contribution. State-over-community reversal is tested only where the outcome-blind admission rule puts the stratum in a crossover-capable domain.

### Higher shared dependence

With higher shared dependence, shared/synchronous stochasticity can preserve a community-realization floor, so reversal should be weakened or absent.

A no-crossover result in a correctly admitted high-dependence context is therefore not automatic falsification. Failure to measure/classify the dependence regime is `NOT_EVALUABLE`.

The frozen pre-pilot screen gives only scale information. Under its generic low-dependence benchmark, crossover separation rises from `0.5425` at 16 blocks to `0.835` at 32 and `0.900` at 48. Near the generic boundary, even more than 1000 recruited plants can remain indecisive. These rates are **not empirical power** and do not set final `n`.

## R5 — breadth strategy CLOSED

For the NEE route, at least one second prospective independent natural context is required under the same frozen H2/H5 mapping and outcome-state logic.

Existing secondary systems remain metadata confrontation or transport triage only. They do not count as P6.

If the prospective transport context is infeasible, the correct response is a strong single-system EL/Ecology route, not weakening H5 or promoting retrospective metadata.

## R1a — architecture CLOSED

### Focal system

- taxon: *Campanula microdonta*;
- candidate geography: Oshima + Kozushima;
- Oshima is first reconnaissance priority because several named occurrence localities are already source-backed;
- Oshima + Kozushima are candidate geography only, not automatically admitted final sites.

### Prospective transport system

- taxon: *Farfugium japonicum*;
- first-priority transport geography: **Kozushima**;
- first-priority locality lead: **Nodo Sainbara-line lighthouse area**;
- reason: it gives a second island geography relative to Oshima-first focal reconnaissance and has an official occurrence lead, while selection remains pre-outcome;
- Hitachi / Hitachinaka / Tateyama are now contingency transport sites, not the preferred route. They may be used only if the Kozushima candidate fails frozen pre-outcome feasibility gates.

A same-archipelago transport context is acceptable only if taxon, season, geography, and sampling units make it a genuine prospective transport challenge rather than another focal block.

## R1b — exact site/time registry OPEN

The candidate registry currently contains **5 focal rows and 3 transport rows, all `candidate`, all 0 admitted**.

The registry is tri-state by design. `candidate` rows may retain `pending/unknown` feasibility. A row becomes `admitted` only when all structural gates pass:

1. named population/site and block ID;
2. predeclared site-time window;
3. eligible flowering plants > 0 under the screening definition;
4. block-independence review = `pass`;
5. SVD background control feasible;
6. open natural pollination feasible;
7. bagged autonomous treatment feasible;
8. supplemental outcross treatment feasible;
9. outcome-blind dependence coordinate feasible;
10. access confirmed;
11. permit confirmed or not required;
12. phenology confirmed.

Unknown feasibility is not coded as biological failure. It remains pending.

### Current focal reconnaissance priority

1. Oshima: Fudeshima coast;
2. Oshima: Toshiki coast;
3. Oshima: Mt. Mihara;
4. Oshima: Senzu coastal plant community;
5. Kozushima: exact *Campanula* locality still unresolved from current herbarium-level evidence.

The Senzu/Oshima coastal plant community is useful occurrence evidence but has high regulatory friction because it is a designated natural monument. Do not assume manipulative work is permitted there.

### Current transport reconnaissance priority

1. Kozushima: Nodo Sainbara-line lighthouse area — first priority;
2. Oshima: Nihonmatsu–Shiofuki coastal trail — backup;
3. Oshima: Senzu coastal plant community — backup/high regulatory friction.

National-park or monument status must be resolved site-by-site before admission. The current screening does not infer that every listed manipulation is prohibited; it only forbids assuming permission.

## R1 block-scale rule

Independent repeated blocks are the H5 lever; extra flowers, visits, or SVD events within a plant do not repair an inadequate block design.

The current R1 triage rule keeps **32 plausibly independent focal blocks** as a screening floor because of the pre-pilot OC. This is not empirical power and not a final confirmatory sample size. R2/R3 may later move the required scale in either direction using empirical dispersion, attrition, community support, and dependence structure.

## R2 — pilot feasibility/dispersion OPEN

Once R1b admits a workable site/time registry, freeze pilot information on:

- independent plant and block recruitment/retention;
- usable monitored flower-hours and zero visits;
- SVD acquisition/background variance;
- treatment loss/damage;
- mature endpoint completion;
- between-plant and between-block dispersion;
- effective-community composition support;
- empirical support/stability of the frozen H5 dependence coordinate.

Pilot outcome direction cannot select predictors or H5 strata.

## R3 — confirmatory precision OPEN

After R2 is frozen:

1. lock the smallest scientifically useful H2/H5 precision target;
2. choose two-sided CI precision or Bayesian assurance/posterior precision;
3. simulate the actual plant-within-block hierarchy;
4. stress-test site/block attrition, SVD availability, treatment loss, composition support, and dependence-stratum support;
5. only then freeze confirmatory replication.

Existing planner: `scripts/plan_effective_dependency_pilot_precision.py`.

Predeclared retreat line: if single-system R3 cannot estimate confirmatory H5, keep H1-H4 confirmatory and H5 descriptive/exploratory for the single-system paper; reserve full H5 + prospective transport for a later expanded NEE design.

## NEE Stage-1 activation rule

```text
R1b exact focal + transport site/time registry admitted
+ R2 pilot feasibility adequate
+ R3 confirmatory H2/H5 precision locked
+ R4 representation preserved
+ lower shared dependence / higher shared dependence rule executable
+ P1-P5 executable under measurement gates
+ R6 data/code/protocol commitments complete
```

The second prospective context is not optional for the NEE route.

## Route rule

```text
R1b + R2 + R3 + prospective transport feasible
    -> NEE Stage-1 remains eligible

strong focal system but transport infeasible
    -> EL / Ecology; do not weaken H5

R3 says confirmatory H5 infeasible
    -> H1-H4 remain confirmatory + H5 descriptive/exploratory
       reserve full H5 + transport for later NEE

measurement/support gate fails
    -> NOT_EVALUABLE
```

Current Oikos paper remains scientifically closed and unaffected by every branch above.
