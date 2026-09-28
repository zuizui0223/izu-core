# Frozen ABM state atlas and identifiability

## Study boundary

This is a **simulation study with qualitative external island-system challenges**. The primary claim does not require a new field raw bundle, a complete empirical `V_k × E_k` mapping, or system-specific parameter fitting.

The external systems ask whether already-frozen ABM state classes occur in independent island settings. They do **not** provide calibration targets, seed choices or mechanism-selection targets for the ABM.

Canonical machine-readable outputs:

- `data/design/frozen_abm_state_atlas_contract.json`
- `data/results/frozen_abm_state_atlas_frozen.json`
- `data/results/frozen_abm_state_separability_frozen.json`
- `data/results/abm_v12_branch_generator_independent_robustness_frozen.json`

The manuscript-ready prose is frozen separately in:

- `docs/SIMULATION_MANUSCRIPT_METHODS_FROZEN_20260824.md`
- `docs/SIMULATION_MANUSCRIPT_RESULTS_FROZEN_20260824.md`

## 1. Which states can the frozen ABM generate?

| state | frozen synthetic evidence | interpretation |
|---|---|---|
| `branches_downstream` | mixed-sign run fraction = **0.4167** in the original v12 residual gate and **0.4167** in the independent block | generated without requiring the four v11 downstream modifiers |
| `same_direction_response` | non-mixed fraction = **0.5833** even with trait heterogeneity ON; **1.0** with initial trait heterogeneity OFF | common state, but not mechanistically unique |
| strong buffering | network-context support rescues reproductive sign in **16/96 = 0.1667** eligible declines | genuine capability, but not universal |
| worsening under network context | **11/96 = 0.1146** eligible declines worsen | network context is bidirectional, not a generic protective buffer |
| magnitude attenuation | network context: **85/96 = 0.8854**; assurance: **207/216 = 0.9583** | weak-response attenuation is easy to generate through more than one route |
| strong assurance sign buffering | **0/216** in the independent block and **0/525** in the broadened support envelope | not a robust property of the current assurance route |

The current 13-system external challenge contains **11 generative state challenges**. All 11 are covered or sign-compatible with a frozen synthetic state class. The remaining two systems are deliberately not treated as generative targets: Guaiacum is an empirical reproductive-axis-decoupling constraint and Dominica is a retained falsification of the frozen signed-position mapping.

This is state-space coverage, not numerical fit and not real-world mechanism identification.

## 2. What actually generates branching?

The strongest synthetic identification result is the v12 residual-factor ablation and its prespecified independent replication.

### Original frozen block

With the tested downstream modifiers fixed OFF, pre-existing lineage trait-position heterogeneity gave:

- mixed-sign run fraction: **0.4167**;
- mean within-run branching balance: **0.2569**.

When initial trait heterogeneity was removed:

- mixed-sign run fraction: **0**;
- mean within-run branching balance: **0**;
- **37** paired lineage signs changed.

Trait-adjustment heterogeneity and assurance-ceiling heterogeneity did not collapse branching when individually removed.

### Independent frozen block

Seed `90260825` was fixed before execution, with the same declared saturation envelope, 4 replicates per saturation, 24 lineages and 120 steps. No empirical targets were loaded.

The independent block produced:

- full mixed-sign run fraction: **0.4167**;
- full mean within-run branching balance: **0.2917**;
- initial-trait-OFF mixed-sign run fraction: **0**;
- initial-trait-OFF branching balance: **0**;
- **44** paired lineage sign changes after initial-trait removal.

Trait-adjustment heterogeneity OFF retained mixed-sign fraction **0.4167** and mean balance **0.2847**. Assurance-ceiling heterogeneity OFF retained **0.4167** and **0.2917**.

Therefore, across two independently seeded frozen blocks:

> **pre-existing lineage position in functional trait space is the only tested residual factor whose removal eliminates within-environment response-sign branching.**

This is a model-internal minimal generator. It does not identify tube length, FDQ, nectar guide, colour, or any other single empirical floral trait as the corresponding causal axis.

## 3. State observations are asymmetrically informative

A central result is that the forward model can generate several states, but the inverse problem is not symmetric.

### Mixed-sign branching → trait-position heterogeneity

Using mixed-sign branching as a diagnostic for initial trait heterogeneity inside the original v12 gate:

- sensitivity: **0.4167**;
- false-negative rate: **0.5833**;
- false-positive rate: **0**;
- specificity: **1.0**.

Thus mixed-sign branching is a **high-specificity, low-sensitivity** signature. Its independent replication strengthens the state boundary without changing the interpretation that many heterogeneity-ON runs remain non-mixed.

### Same-direction response → trait uniformity

Using a non-mixed response to infer trait uniformity performs poorly:

- sensitivity for the uniform-trait intervention: **1.0**;
- false-positive rate among heterogeneity-ON runs: **0.5833**;
- specificity: **0.4167**.

Thus a same-direction island response is **not** evidence that lineages lacked heterogeneous starting positions.

### Strong sign rescue → network context rather than assurance

Among the tested routes:

- network-context sign-rescue sensitivity: **0.1667**;
- assurance false-positive rate for sign rescue: **0**;
- specificity against assurance: **1.0**.

Strong sign rescue is again high-specificity but low-sensitivity. The current network-context route can do it; the robust assurance route does not.

### Magnitude attenuation → poor mechanism discrimination

Magnitude attenuation has the opposite problem:

- assurance attenuation sensitivity: **0.9583**;
- network-context attenuation frequency: **0.8854**;
- specificity against network context: **0.1146**.

A smaller decline is therefore almost useless for distinguishing the two tested routes.

## 4. Transition boundaries visible in the frozen experiments

### Initial trait heterogeneity

Turning initial trait heterogeneity OFF moves both independently seeded tested blocks from mixed-sign branching to none:

`0.4167 → 0.0`

This is the sharpest replicated state boundary currently identified.

### Assurance across saturation

Across saturation `1, 2, 3`, assurance remains in the same qualitative state:

| saturation | sign rescue | magnitude attenuation |
|---:|---:|---:|
| 1 | 0 | 71/75 = **0.9467** |
| 2 | 0 | 73/76 = **0.9605** |
| 3 | 0 | 63/65 = **0.9692** |

No transition to robust strong sign buffering is detected across this tested saturation range.

### Network-context support

Switching support from OFF to ON is not monotonic protection:

- sign rescue: **0.1667**;
- worsening: **0.1146**.

The transition is lineage/context-specific. The correct concept is **branch allocation with buffering capacity**, not a universal buffer.

## 5. External 13-system challenge

| observed class | systems | frozen interpretation |
|---|---:|---|
| branching | 3 | qualitatively generated by frozen branching capability |
| same-direction propagation | 6 | sign-class compatible; state alone does not identify mechanism |
| buffering / alternative | 2 | synthetic buffering class exists; real mechanism remains unmapped |
| reproductive-axis decoupling | 1 | empirical constraint, not a single synthetic state target |
| retained falsification | 1 | Dominica frozen mapping failure remains protected |

The external comparison therefore does **not** support the statement “one ABM mechanism explains 13 island systems.” It supports the narrower statement:

> **one frozen minimal model architecture spans multiple recurrent island-response state classes, while the inverse mapping from state to mechanism is only partially identifiable.**

## 6. Falsification table

The canonical machine-readable table is `data/results/simulation_manuscript_falsification_table_frozen.json`.

| claim | falsifying observation / current status |
|---|---|
| initial trait position is the minimal v12 branching generator | mixed-sign branching after initial-trait heterogeneity OFF; **0 in both independently seeded blocks**, so claim survives |
| network context is a universal buffer | any matched worsening under support ON; **11 worsenings**, so universal-buffer claim is rejected |
| assurance is a robust strong sign buffer | robust replicated sign rescue in the declared blocks; current result **0/216 and 0/525**, so strong-buffer claim is rejected |
| frozen Dominica signed-position mapping predicts empirical direction | observed counterdirectional/nonconcordant selection; failure retained and not retuned |
| frozen state vocabulary covers a future predeclared external target | a target outside every frozen class is a **state-space miss** and must be recorded before model extension |

## 7. Paper-level conclusion

The defensible simulation result is not a universal island syndrome and not empirical causal identification.

It is:

1. a common upstream perturbation can yield multiple lineage response signs;
2. pre-existing functional position is the independently replicated minimal identified synthetic generator of within-run branching;
3. local network context reallocates branches and can sometimes reverse a decline, but also worsens some lineages;
4. assurance robustly attenuates decline magnitude but does not robustly reverse sign;
5. qualitative state observations differ sharply in diagnostic value;
6. the 13-system challenge broadens state-space external validity while retaining one explicit failed frozen mapping.

The core simulation robustness gate is now **closed for the primary claim**. Further seed search is not part of the mainline. The active work is manuscript assembly and figure/text polish from the frozen outputs; new simulation should be opened only for a new prespecified scientific question that survives editorial review.
