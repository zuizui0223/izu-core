# Active development mainline — simulation-first island programme

Updated: 2026-08-24  
Current machine-readable routing: `data/design/simulation_study_mainline_20260824.json`  
Parent comparative state: `data/design/active_development_mainline.json`  
Frozen state atlas: `data/results/frozen_abm_state_atlas_frozen.json`  
State separability: `data/results/frozen_abm_state_separability_frozen.json`

The older comparative routing remains useful as an evidence inventory, but it is **not the current execution mainline**. The current primary study is a simulation study with qualitative external island-system challenges.

## Current primary question

> Which island-response state classes can the already-frozen ABM generate, which tested mechanism axes distinguish those states, and which observations count as state-space misses or protected falsifications?

External island systems are used as qualitative held-out challenges. They are not numerical calibration rows and do not choose seeds, parameters, or mechanisms.

## What is already complete

### Global external challenge

- 54 screened island / archipelago system units;
- 13 strict qualitative external systems;
- 11 generative state challenges, all covered or sign-compatible with a frozen synthetic state class;
- 1 reproductive-axis-decoupling constraint;
- 1 retained Dominica falsification.

### Minimal branching mechanism

Within the declared v12 residual ABM:

- mixed-sign run fraction with initial trait heterogeneity ON: **0.4167**;
- mean within-run branching balance: **0.2569**;
- removing initial trait heterogeneity collapses both to **0**.

Pre-existing lineage position in functional trait space is therefore the minimal identified synthetic generator of within-run response-sign branching.

### Branch allocation and buffering

- local-support paired sign changes: **105/288 = 0.3646**;
- partner-effectiveness paired sign changes: **13/288 = 0.0451**;
- network-context sign rescues: **16/96 = 0.1667**;
- network-context worsenings: **11/96 = 0.1146**;
- network-context magnitude rescues: **85/96 = 0.8854**.

Network context is a bidirectional branch allocator with buffering capacity, not a universal protective buffer.

### Assurance

- independent block sign rescues: **0/216**;
- independent magnitude attenuations: **207/216 = 0.9583**;
- broadened support envelope sign rescues: **0/525**.

Autonomous assurance is a robust magnitude attenuator in the tested model, not a robust strong sign buffer.

### State separability

The inverse mapping from observed state to mechanism is asymmetric:

- mixed-sign branching → initial trait heterogeneity: specificity **1.0**, sensitivity **0.4167**;
- same-direction → trait uniformity: false-positive rate **0.5833**, specificity **0.4167**;
- sign rescue → network context versus tested assurance: specificity **1.0**, sensitivity **0.1667**;
- magnitude attenuation → assurance versus network context: specificity **0.1146**.

Thus state compatibility does not imply one-to-one mechanism identification.

## Current mainline

### P0 — protect the frozen model state

Do not retune the ABM to any of the 13 external systems. Preserve the v12 branch-generator result, replicated network-context buffering, assurance attenuation result, and Dominica failure.

### P1 — manuscript figures and result architecture

Generate the main figures directly from:

`data/results/simulation_manuscript_figure_data_frozen.json`

Planned main figures:

1. model state-map / analysis logic;
2. minimal branch-generator ablation;
3. branch allocation, buffering and attenuation;
4. 13-system external challenge plus state-identifiability diagnostics.

### P2 — result and falsification prose

The primary paper statement is:

> A frozen minimal model architecture spans multiple recurrent island-response state classes, while the mapping from observed state back to mechanism is only partially identifiable.

The paper must retain explicit negative results:

- network context is not universally protective;
- assurance does not robustly rescue response sign;
- Dominica fails the frozen signed-position mapping;
- any future predeclared external state outside all frozen state classes is recorded as a state-space miss before model extension.

### P3 — optional empirical translation

Issue #91 field data and the five-gate `V_k × E_k` empirical network-context mapping remain scientifically useful, but only for a stronger future claim assigning a named real island system to a synthetic mechanism.

They are **not required for the primary simulation study** and do not block manuscript completion.

## Not the active mainline

Do not spend the next cycle on:

- collecting a field raw bundle before the simulation paper is resolved;
- closing the current 0/12 empirical network-context mapping before writing the simulation result;
- adding more island systems merely to increase counts;
- retuning parameters or choosing seeds based on external outcomes;
- adding a mechanism to rescue Dominica or another future state-space miss;
- calling qualitative state compatibility empirical causal identification;
- claiming universal network buffering or robust assurance sign rescue;
- formal cross-system effect-size pooling of noncommensurate systems.

## Next executable task

Generate the manuscript figures from the frozen figure-data layer, then perform one final repository sweep so stale comparative/field-oriented routing cannot override `simulation_study_mainline_20260824.json`.
