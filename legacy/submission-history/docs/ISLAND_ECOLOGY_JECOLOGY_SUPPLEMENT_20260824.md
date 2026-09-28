# Supporting Information

## One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification

This Supporting Information accompanies the ecology-first manuscript. It contains only prespecified or already-frozen analyses and source audits. No new simulation, parameter tuning, external-system admission, or empirical mechanism mapping is introduced here.

---

# Appendix S1. Frozen study architecture and claim boundary

The study separates three inferential layers.

1. **Synthetic mechanism experiments.** A frozen island pollination ABM is perturbed by matched mainland-like versus island-like pollinator-functional environments. Mechanism axes are manipulated by factorial or residual ablation.
2. **Independent robustness blocks.** The strongest branch-generator boundary, network-context buffering capability, and autonomous-assurance conclusions are checked in separately frozen stochastic blocks.
3. **External ecological challenge.** A source-audited island literature set is used only to ask whether recurrent response states occur outside the focal synthetic system. External systems were not used to select model parameters, random seeds, thresholds, mechanisms, or state definitions.

The central claim is therefore conditional: the experiments identify causal roles **within the declared ABM** and the external comparison tests recurrence of response classes. The study does not claim that one synthetic mechanism has been empirically identified in every island system.

The standardized plant matching trait is an abstract relative coordinate. It is not post-hoc equivalent to corolla length, colour, nectar guides, FDQ, or any single measured floral trait.

---

# Appendix S2. Experimental block inventory

## Table S1. Frozen simulation blocks used in the manuscript

| Block | Purpose | Frozen design | Primary readout |
|---|---|---|---|
| v11 downstream factorial | Test whether downstream modifiers generate or reallocate branching | 16 factorial cells; saturation 1, 2, 3; 4 replicates per saturation; 24 lineages; 288 lineage contrasts per cell; no empirical inputs | mixed-sign run fraction; branching balance; paired sign changes |
| v12 residual branch generator | Identify the minimal tested residual source of within-run response-sign branching | 8 cells; saturation 1, 2, 3; 4 replicates per saturation; 24 lineages; 288 contrasts per cell; downstream four-factor gate fixed off | mixed-sign run fraction; mean within-run branching balance |
| independent v12 robustness | Independently retest the strongest branch-generator boundary | seed 90260825; 4 replicates per saturation; 24 lineages; 120 steps; saturation 1, 2, 3; no empirical inputs | replicated-minimal-generator decision |
| network-context robustness | Separate local support from autonomous assurance and allow rescue or worsening | matched support OFF versus ON; assurance disabled; evaluation restricted to eligible declines | magnitude attenuation, sign rescue, worsening |
| assurance robustness | Test attenuation versus strong sign rescue | matched assurance OFF versus ON with identical upstream service changes; independent block plus broadened support envelope | attenuation and sign-rescue counts |

The v11 and v12 design metadata are frozen in `data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json` and `data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json`. The independent branch-generator design is frozen in `data/design/abm_v12_branch_generator_independent_robustness_freeze.json`.

---

# Appendix S3. Response-state definitions

**Mixed-sign branching** occurs when positive and negative lineage reproductive responses coexist within the same matched stochastic run.

**Same-direction propagation** denotes a run or empirical system in which the focal downstream response moves in a common qualitative direction rather than splitting into opposite-sign branches.

For network context, a **magnitude rescue** makes an eligible negative reproductive response less negative, a **sign rescue** moves it to zero or above, and **worsening** makes it more negative.

For autonomous assurance, **magnitude attenuation** means a smaller reproductive decline under assurance than under the matched no-assurance condition. **Strong sign rescue** requires a negative upstream service response but a non-negative downstream reproductive response attributable to assurance.

These state definitions were frozen before the final external challenge.

---

# Appendix S4. Downstream factorial and residual branch generator

The v11 all-on configuration contained 64 positive, 201 negative and 23 equal lineage responses, with mixed-sign runs in 0.6667 of matched runs. When all four tested downstream factors—local support, dependency heterogeneity, assurance responsiveness and partner effectiveness—were fixed off, two-sided branching persisted: 157 positive and 131 negative responses, no equal responses, and mixed-sign runs in 0.4167 of matched runs.

Drop-one paired sign changes were 105/288 for local support, 13/288 for partner effectiveness, 1/288 for assurance responsiveness and 0/288 for dependency heterogeneity. These results identify local support as a strong branch allocator, not as the origin of two-sided branching.

The v12 residual experiment then fixed the four downstream modifiers off. The full residual model retained mixed-sign runs in 0.4167 of matched runs with mean within-run branching balance 0.2569. Removing initial trait-position heterogeneity reduced both quantities to zero and changed 37 paired lineage signs. Removing trait-adjustment heterogeneity retained mixed-sign frequency 0.4167 and changed only two paired signs; removing assurance-ceiling heterogeneity retained mixed-sign frequency 0.4167 and changed none.

The all-three-residual-factors-off state had no within-run branching. These counts concern stochastic runs and matched lineage contrasts; pooled positive/negative totals across runs are not a substitute for within-run branching.

---

# Appendix S5. Independent branch-generator robustness

Before execution, the independent v12 block froze seed 90260825, four replicates per saturation, 24 lineages, 120 steps and saturation values 1, 2 and 3. The decision rule classified the result as `replicated_minimal_generator` only if:

1. the independent full residual block contained mixed-sign branching;
2. initial-trait heterogeneity OFF eliminated mixed-sign branching and within-run branching balance; and
3. at least one other single residual ablation retained branching.

The first workflow attempt failed before scientific execution because of an import-path error. Only that import path was repaired; the seed and design were unchanged. The first successfully executed scientific result was retained, and no further seed search was performed.

The independent full block again had mixed-sign run fraction 0.4167. Initial functional-position heterogeneity OFF reduced mixed-sign frequency and branching balance to zero and changed 44 paired lineage signs. Trait-adjustment OFF and assurance-ceiling OFF both retained mixed-sign frequency 0.4167. The prespecified decision was therefore `replicated_minimal_generator`.

---

# Appendix S6. Network-context and autonomous-assurance robustness

## Network context

Among 96 eligible negative support-OFF reproductive contrasts, support ON:

- attenuated the decline in 85/96;
- crossed the sign boundary in 16/96; and
- worsened 11/96.

The coexistence of rescue and worsening rejects a monotonic universal-buffer interpretation. The manuscript therefore describes local interaction context as a **bidirectional branch allocator with buffering capacity**.

## Autonomous assurance

Among 216 lineages with upstream service decline in the independent assurance block, assurance attenuated reproductive decline in 207/216 but produced 0/216 sign rescues. By saturation, attenuation occurred in 71/75, 73/76 and 63/65 eligible declines at saturation 1, 2 and 3, respectively. In the broadened support envelope, strong sign rescue remained 0/525.

The stable conclusion is therefore magnitude attenuation rather than robust qualitative sign rescue.

---

# Appendix S7. State-separability diagnostics

State-separability is a supporting inference guard rather than a primary biological result.

## Table S2. Observation-to-mechanism diagnostic asymmetry within the tested intervention family

| Observable state | Intervention contrast | Sensitivity | False-positive rate | Specificity | Interpretation |
|---|---|---:|---:|---:|---|
| mixed-sign branching | initial functional-position heterogeneity present vs absent | 0.4167 | 0.0000 | 1.0000 | highly specific when present, but insensitive |
| same-direction response | uniform starting state vs heterogeneous starting state | 1.0000 | 0.5833 | 0.4167 | common and weakly identifying |
| strong sign rescue | network context vs assurance route | 0.1667 | 0.0000 | 1.0000 | highly specific but uncommon |
| magnitude attenuation | assurance vs network context | 0.9583 | 0.8854 | 0.1146 | frequent but poorly separable |

Thus a common response state can be non-identifying, whereas a rare state may be highly mechanism-specific within the declared model family. These quantities are model-internal diagnostics, not empirical estimates across natural islands.

**Figure S1** visualizes these sensitivity, false-positive-rate and specificity contrasts.

---

# Appendix S8. Strict external island-system challenge

The global screen retained 54 geographic/system units. Thirteen systems met the strict source and state-assignment contract. The counts are not prevalence estimates because the systems were not randomly sampled.

## Table S3. Strict external systems and frozen response-state assignments

| System | State | Primary source(s) | Claim boundary |
|---|---|---|---|
| Izu multi-taxon Hiraiwa–Ushimaru | branching | Hiraiwa & Ushimaru 2017, 2024 | response heterogeneity across source-locked island studies; not same-estimand replication |
| Caribbean Gesneriaceae | branching | Martén-Rodríguez et al. 2010, 2015 | clade-level recurrence; not a matched population causal chain |
| Canary Islands / Teide | branching | Valido et al. 2019 | common honeybee/network perturbation with plant-specific reproductive responses |
| Ogasawara *Psychotria homalosperma* | same-direction propagation | Watanabe et al. 2018 | access asymmetry and directional pollen/reproductive consequences; no numeric signed-position test |
| New Zealand *Rhabdothamnus solandri* | same-direction propagation | Anderson et al. 2011 | bird functional loss propagates to seed and recruitment |
| Guam–Saipan | same-direction propagation | Mortensen et al. 2008 | bird extirpation natural experiment; not a generic isolation mechanism |
| Seychelles ant disruption | same-direction propagation | Costa et al. 2023 | within-island ant-context experiment; qualitative propagation only |
| Mauritius *Roussea simplex* | same-direction propagation | Hansen & Müller 2009 | invasive-ant disruption of pollination; not evidence for one universal ant effect |
| Bahamas *Pavonia bahamensis* | same-direction propagation | Rathcke 2000 | hurricane caused both resource and pollination limitation; state uses source-separated pollination component |
| Hawaiian lobelioids | buffering / alternative | Case et al. 2026a,b | high reproductive performance or altered matching after bird loss; synthetic buffer mechanism not empirically identified |
| California Channel Islands *Nicotiana glauca* | buffering / alternative | Schueller 2004, 2007 | increased selfing capacity and morphology differ; establishment filtering remains an alternative |
| Puerto Rico–Mona *Guaiacum sanctum* | reproductive axes decouple | Fumero-Cabán et al. 2022 | visitor context differs while self/outcross index remains similar; do not collapse all axes into one buffer label |
| Dominica *Heliconia* | retained falsification | Martén-Rodríguez et al. 2011; Temeles et al. 2013 | frozen negative signed-position projection failed and was not retuned |

The 11 generative challenges comprise three branching, six same-direction propagation and two buffering/alternative systems. All 11 are covered or sign-compatible with response classes already available in the frozen model. *Guaiacum* remains an axis-decoupling constraint and Dominica remains a failure.

The complete source ledger, including secondary sources and DOI-level provenance, is in `docs/SIMULATION_MANUSCRIPT_EXTERNAL_SYSTEM_REFERENCES_20260824.md` and `data/design/simulation_manuscript_external_system_reference_matrix.json`.

---

# Appendix S9. Protected falsifications and stop rules

The manuscript retains explicit failure conditions.

- **Branch generator:** contradicted if mixed-sign branching survives initial functional-position heterogeneity OFF in the declared residual gate.
- **Universal network buffer:** rejected by matched worsening; worsening is retained rather than relabelled.
- **Robust assurance sign buffer:** rejected when sign rescue does not replicate in the declared robustness blocks.
- **Dominica signed-position mapping:** remains failed; no outcome-informed remapping is allowed.
- **External state vocabulary:** a future predeclared state outside every frozen response class must be logged as a state-space miss before any model extension.

These rules prevent a flexible ABM from absorbing every external observation post hoc.

---

# Appendix S10. Reproducibility map

The main numerical artifacts are:

- `data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json`;
- `data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json`;
- `data/results/abm_v12_branch_generator_independent_robustness_frozen.json`;
- `data/results/network_context_buffering_capability_robustness_frozen.json`;
- `data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json`;
- `data/results/frozen_abm_state_atlas_frozen.json`;
- `data/results/frozen_abm_state_separability_frozen.json`;
- `data/results/simulation_manuscript_figure_data_frozen.json`;
- `data/results/simulation_manuscript_falsification_table_frozen.json`.

Ecology-first main figures are routed as Fig. 1–4; state-separability diagnostics are routed to Fig. S1. The anonymous review archive excludes author-identifying title-page information and public repository identity while retaining the frozen scientific materials needed for peer review.
