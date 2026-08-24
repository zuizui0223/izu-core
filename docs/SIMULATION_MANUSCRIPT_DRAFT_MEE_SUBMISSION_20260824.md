# From state generation to mechanism identification: a frozen separability framework for agent-based ecological models

## Abstract

1. **Agent-based models can reproduce multiple ecological patterns, but forward pattern generation does not establish which mechanism generated an observed state.** This inverse problem is a form of equifinality: the same state can emerge under different internal mechanisms, while a genuinely important mechanism may express its most diagnostic state only in a subset of stochastic realizations.

2. We introduce **frozen state-separability analysis**, a workflow that: (i) freezes a model, state classifier and intervention contrasts before external challenge; (ii) estimates state frequencies when a candidate mechanism is present versus absent or replaced; (iii) converts these frequencies to synthetic sensitivity, false-positive rate and specificity; (iv) independently replicates the highest-value intervention boundary using a predeclared stochastic design; and (v) protects external prediction failures and state-space misses from post-hoc model extension. The method is implemented as a reusable Python API.

3. We demonstrate the workflow with a frozen plant–pollinator ABM motivated by island biotic simplification. Removing pre-existing lineage functional-position heterogeneity eliminated within-run response-sign branching in both the original and independently seeded blocks (mixed-sign frequency 0.4167 to 0), whereas other residual single-factor ablations retained branching. Network context rescued reproductive sign in 16/96 eligible declines but worsened 11/96; autonomous assurance attenuated 207/216 declines but produced 0/216 sign rescues and 0/525 across a broadened envelope. Mixed-sign branching and strong sign rescue were specific (1.0) but insensitive (0.4167 and 0.1667), whereas same-direction response and magnitude attenuation were weak mechanism discriminators.

4. In a held-out qualitative application, 11 generative cases among 13 strict island systems were covered or sign-compatible with the already-frozen state vocabulary; one reproductive-axis-decoupling constraint and one failed signed prediction were retained rather than absorbed into the model. **Frozen state separability therefore distinguishes forward generative adequacy from inverse mechanism identification and gives flexible ecological simulations explicit diagnostic and falsification rules.** The workflow is applicable wherever intervention-defined mechanisms generate overlapping macroscopic states.

## Data/Code for peer review

An anonymised review archive should contain the reusable `state_separability` module, frozen intervention summaries, exact-regeneration tests, figure-generation scripts and the machine-readable external-state registry. The public development repository is `zuizui0223/izu-core`; for double-anonymous review, a private or anonymised archive should be supplied at submission. No new unpublished field dataset is required for the primary analysis.

**Keywords:** agent-based model; ecological networks; equifinality; falsification; model validation; pattern-oriented modelling; sensitivity; specificity

---

# 1. Introduction

Agent-based and individual-based models are widely used in ecology because population- and community-level patterns can emerge from interactions among heterogeneous entities. This flexibility creates an inferential problem. A model may generate the same macroscopic state through more than one internal route, while a mechanism that is necessary for a class of outcomes may express its most diagnostic state only in some stochastic realizations. Consequently, a model can be **generatively adequate**—capable of producing an observed state—without the state being **mechanistically identifying**.

Pattern-oriented modelling (POM) provides a foundational strategy for constraining bottom-up models with multiple empirical patterns rather than a single fitted target (Grimm et al. 2005; Grimm & Railsback 2012). POM directly addresses structural uncertainty and equifinality. However, after a model has generated a set of candidate patterns, an additional inverse question remains useful: **how informative is a particular state about a particular mechanism?** A pattern is often described as supporting a mechanism because the model can produce it, but forward compatibility does not quantify how often the same pattern appears when that mechanism is removed or replaced.

We formulate this inverse question as an intervention-derived diagnostic problem. For an observable state `S` and a declared mechanism contrast `M=1` versus `M=0`, repeated simulation experiments estimate `P(S|M=1)` and `P(S|M=0)`. The first quantity is analogous to sensitivity: how often the model expresses the state when the mechanism is present. The second is a synthetic false-positive rate: how often the state appears when the mechanism is absent or a declared alternative is active. Specificity is `1-P(S|M=0)`. These quantities describe **state separability within the declared simulation family**. They are not empirical diagnostic accuracies unless transport to natural systems is independently justified.

The workflow adds three safeguards. First, the state vocabulary, intervention contrasts and stochastic envelope are frozen before held-out external challenges are scored. Second, the strongest causal boundary is independently replicated under a predeclared stochastic design and stop rule. Third, failures are protected: a failed signed prediction or a new external state outside the frozen vocabulary is recorded before model extension. The aim is not to replace POM but to add a **forward-state / inverse-separability layer** to simulation models evaluated through interventions and patterns.

We demonstrate the workflow using a plant–pollinator ABM motivated by island systems. Island reproductive ecology is a useful stress test because broad comparative patterns coexist with heterogeneous local responses. Self-compatibility and other reproductive traits can act as colonization filters (Grossenbacher et al. 2017; Zell et al. 2025), while island studies report varied changes in pollination, morphology and reproduction (Traveset & Navarro 2018; Whittaker et al. 2023). Network resilience theory further predicts that partner loss can be compensated by rewiring or alternative interactions rather than propagating monotonically to function (Bascompte & Scheffer 2023; Marjakangas et al. 2025). Branching, propagation, attenuation and buffering can therefore overlap as observable states.

We ask four methodological questions. **First**, can a state vocabulary be frozen before external challenge? **Second**, which interventions generate, eliminate or merely reallocate those states? **Third**, what sensitivity and specificity does each state have for its candidate mechanism contrast? **Fourth**, does the frozen vocabulary remain useful when challenged by independent ecological systems without refitting?

# 2. Materials and Methods

## 2.1 Frozen state-separability workflow

The method begins with a frozen simulation model `M`, a state classifier `C`, a declared scenario/parameter envelope and a set of mechanism interventions. Investigators define observable states before inspecting held-out external outcomes. State classifiers can be categorical or derived prospectively from continuous outcomes. In the demonstration, states included mixed-sign branching, same-direction response, sign rescue, magnitude attenuation and worsening.

For each candidate mechanism, a mechanism-present intervention and a mechanism-absent or declared-alternative intervention are specified. Given state `S`, we calculate

\[
\mathrm{sensitivity}=P(S=1\mid M=1),
\]

\[
\mathrm{FPR}=P(S=1\mid M=0),
\]

\[
\mathrm{specificity}=1-\mathrm{FPR},
\]

and

\[
\mathrm{FNR}=1-\mathrm{sensitivity}.
\]

The reusable implementation (`channel_id/state_separability.py`) accepts either event counts or already-frozen intervention frequencies. It additionally reports Youden's J and a positive likelihood ratio as descriptive summaries. These are conditional synthetic measures, not empirical population-level diagnostics.

We distinguish four intervention roles. A **generator** is necessary for the tested state boundary when its removal eliminates that state. A **branch allocator** changes which units occupy which state without eliminating the state family. A **magnitude modifier** changes response strength but rarely qualitative state. A **non-discriminating factor** has little effect in the tested conditional model.

The strongest intervention boundary is independently replicated under a frozen stochastic design. The seed or seed-generation rule, replicate count, parameter envelope, classifier, decision categories and stop rule are defined before execution. The first scientific result is accepted. Software failures before scientific execution can be repaired without changing the design but must remain in provenance.

External systems can then challenge the frozen state vocabulary without fitting it. Three outcomes remain distinct: state coverage, empirical mechanism identification and state-space miss/prediction failure. Only the first follows from qualitative state compatibility.

## 2.2 Worked plant–pollinator ABM

The worked example represents multiple plant lineages exposed to matched mainland-like and oceanic-like pollinator environments. Pollination opportunity emerges from interaction between plant and pollinator functional traits under a fixed visit-budget formulation. Plant lineages can differ in initial standardized matching-trait position and, depending on the experimental layer, in trait adjustment, local support, pollinator dependency, assurance ceiling, assurance responsiveness and partner effectiveness.

The standardized matching trait is an abstract functional coordinate. It is not assigned post hoc to corolla length, colour, nectar guides or any one empirical trait.

A downstream factorial removed local support, dependency heterogeneity, assurance responsiveness and partner effectiveness. We recorded response signs, within-run mixed-sign frequency, branching balance and paired sign changes. A residual factorial then fixed those downstream modifiers OFF and manipulated initial trait-position heterogeneity, trait-adjustment heterogeneity and assurance-ceiling heterogeneity.

## 2.3 Independent branch-generator replication

The central residual boundary was replicated once using seed `90260825`, four replicates per saturation, 24 lineages, 120 steps and saturations 1, 2 and 3. External targets and empirical inputs were absent. The predeclared outcome was `replicated_minimal_generator` if the full block branched, initial-trait removal eliminated within-run branching and at least one other single residual ablation retained branching; `inconclusive` if the full independent block did not branch; or `contradicted` if initial-trait removal retained branching.

The first workflow attempt failed before simulation execution because of an import-path error. Only that software error was repaired; the seed and scientific design were unchanged. The first successfully executed scientific result was retained and additional seed search was closed.

## 2.4 Network context and autonomous assurance

Network-context buffering compared local support OFF and ON using matched opportunity networks while autonomous assurance was disabled. Sign-rescue analyses were restricted to lineages in which global opportunity declined and the support-OFF reproductive contrast was negative. A sign rescue crossed the zero boundary, a magnitude rescue made the response less negative, and a worsening made it more negative.

The assurance analysis compared matched simulations with the autonomous-assurance route enabled or disabled while upstream effective-service changes were identical. Robustness was assessed in an independent block and a broadened local-support envelope. A non-replicating sign rescue from an earlier block was retained but not promoted to the stable claim.

## 2.5 Held-out island-system challenge

A global literature screen retained 54 geographic/system units as the denominator. Thirteen met a strict state-challenge contract. Their observed states were assigned from source-locked evidence before comparison with the frozen model vocabulary. The strict set comprised three branching systems, six same-direction propagation systems, two buffering/alternative systems, one reproductive-axis-decoupling constraint and one retained falsification.

The 11 generative cases were evaluated only for qualitative state coverage or sign-class compatibility. We did not optimize parameters, fit a pooled effect, or treat state compatibility as empirical mechanism identification. System-specific citations and claim boundaries are provided in the Supplementary reference matrix.

## 2.6 Falsification rules

Five rules were frozen. The minimal branch-generator claim fails if mixed-sign branching survives initial-trait removal. A universal network-buffer claim is rejected by any matched worsening. A robust assurance sign-buffer claim requires replicated sign rescue. The failed Dominica signed-position prediction remains failed. Any future predeclared external state outside every frozen class must be recorded as a state-space miss before model extension.

# 3. Results

## 3.1 Initial functional position generated within-run branching

In the original residual block, mixed-sign branching occurred in 0.4167 of matched runs. Removing initial trait-position heterogeneity reduced mixed-sign frequency and mean within-run branching balance to zero, whereas removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity individually retained branching.

The same boundary occurred in the independent block. Full-model mixed-sign frequency was 0.4167 and mean within-run balance was 0.2917. Initial-trait removal again reduced both to zero and changed 44 paired lineage signs. Trait-adjustment heterogeneity OFF and assurance-ceiling heterogeneity OFF each retained mixed-sign frequency 0.4167. Across both frozen blocks, initial functional-position heterogeneity was the only tested residual factor whose removal eliminated within-run response-sign branching.

## 3.2 Downstream mechanisms reallocated or attenuated states

Two-sided branching persisted when all four tested downstream modifiers were fixed OFF. Local support nevertheless changed 105 of 288 paired lineage signs when removed, compared with 13 of 288 for partner effectiveness, one for assurance responsiveness and none for dependency heterogeneity. Local support therefore strongly reallocated branch identity without being the origin of two-sided branching.

In the independent network-context block, support ON produced sign rescue in 16 of 96 eligible negative reproductive contrasts, attenuated 85 of 96 and worsened 11 of 96. Network context thus had strong buffering capacity but was not monotonic protection.

Autonomous assurance occupied a different region. It attenuated 207 of 216 service-decline responses in an independent block but produced no strong sign rescues. A broadened envelope likewise produced zero sign rescues in 525 eligible contrasts.

## 3.3 State diagnostics were strongly asymmetric

| Observable state | Mechanism contrast | Sensitivity | False-positive rate | Specificity |
|---|---|---:|---:|---:|
| Mixed-sign branching | initial heterogeneity ON vs OFF | 0.4167 | 0.0000 | 1.0000 |
| Same-direction response | uniformity vs heterogeneity ON | 1.0000 | 0.5833 | 0.4167 |
| Strong sign rescue | network context vs assurance | 0.1667 | 0.0000 | 1.0000 |
| Magnitude attenuation | assurance vs network context | 0.9583 | 0.8854 | 0.1146 |

Mixed-sign branching and strong sign rescue were highly specific but insensitive. Their presence was informative within the tested mechanism family, whereas their absence did not exclude the mechanism. Same-direction response was common even while the necessary branching generator was present. Magnitude attenuation was generated readily by both tested downstream routes and was therefore largely non-separable.

## 3.4 External challenges expanded state-space coverage without identifying mechanism

Thirteen island systems entered the strict held-out challenge. Eleven were generative targets—three branching, six same-direction and two buffering/alternative cases—and all 11 were covered or sign-compatible with an already-frozen state class. Puerto Rico–Mona *Guaiacum* was retained as a reproductive-axis-decoupling constraint rather than forced into a buffering label. A frozen signed-position prediction for Dominica *Heliconia* failed and remained failed.

No external case changed a model parameter, seed, mechanism or state label.

# 4. Discussion

## 4.1 Forward coverage and inverse identification are different tests

The main methodological result is that the evidential value of an observable state depends on its intervention-derived separability. A mechanism can be necessary for a state family even when its most diagnostic state appears in fewer than half of realizations. Conversely, a common state can have poor specificity because alternatives generate it readily. Model reproduction of a state is therefore not a uniform unit of evidence.

This framework complements POM. POM uses multiple patterns to constrain bottom-up models and reduce equifinality (Grimm et al. 2005; Grimm & Railsback 2012). Frozen state separability adds a conditional inverse question: **how much does an observed state distinguish a declared mechanism intervention from its absence or alternative?** Sensitivity and specificity expose two common interpretation errors: rejecting a mechanism because an insensitive state is absent, and favoring a mechanism because a nonspecific state is present.

## 4.2 Freezing turns flexible simulation into a falsifiable sequence

The procedural contribution is equally important. State labels, interventions and confirmatory stochastic design were fixed before external challenge. The central branch-generator boundary was tested once under a predeclared independent seed and stop rule. The external challenge retained an axis-decoupling constraint and a failed signed prediction rather than absorbing them through redefinition.

The approach does not prohibit model development. It orders it. A miss is first recorded under model version `M_t`; a new mechanism can then define `M_{t+1}` and face a new frozen challenge. This prevents explanatory flexibility from increasing faster than falsifiability.

## 4.3 The island example shows why qualitative labels can mislead mechanism inference

Island plant reproduction contains several processes capable of producing superficially similar states. Colonization filters can enrich islands for self-compatible lineages (Grossenbacher et al. 2017; Zell et al. 2025), local reproductive responses remain heterogeneous (Traveset & Navarro 2018; Whittaker et al. 2023), and interaction networks can reorganize through rewiring or alternative partners (Bascompte & Scheffer 2023; Marjakangas et al. 2025).

The ABM makes the resulting inverse problem explicit. Same-direction response is compatible with heterogeneous as well as uniform starting positions. Decline attenuation can arise from both local network context and autonomous assurance. Strong sign rescue is more discriminating but uncommon. Consequently, empirical labels such as “buffered” or “directional” may describe an outcome while providing little information about its cause.

The 13-system application should therefore be interpreted as a held-out **state-space challenge**. It demonstrates that the frozen vocabulary spans independent ecological examples; it does not establish that one synthetic mechanism explains all systems.

## 4.4 General use beyond the test case

State-separability analysis requires only intervention-defined mechanism contrasts and observable model states. It can therefore be applied to community assembly, fragmentation, epidemiological, social–ecological and other agent-based models. States can remain categorical, as in this demonstration, or be defined prospectively with continuous/probabilistic classifiers.

A fragmentation model, for example, could freeze collapse, persistence and compensation states; ablate dispersal, local redundancy and behavioural adaptation; and quantify whether persistence is specific to any one route. Disease models could do the same for extinction, endemic persistence and resurgence under contact-structure or immunity interventions.

## 4.5 Limitations

Sensitivity and specificity are model-conditional. They depend on the chosen intervention, scenario envelope and state definition. A high-specificity synthetic state can motivate an empirical test, but transport to natural systems requires separate evidence that the intervention corresponds to a measurable biological mechanism.

The demonstration uses simple event frequencies, which makes it transparent and compatible with already-frozen outputs. It does not yet provide uncertainty intervals, hierarchical pooling across parameter regions or continuous-state discrimination. These are extensions rather than prerequisites for the present workflow.

An absent mechanism in simulation is also not necessarily a biologically realistic counterfactual. Specificity should therefore always be reported relative to the declared absent/alternative intervention, not as if all mechanisms in nature were excluded.

Finally, external challenge quality remains limited by empirical source quality. Frozen state separability does not solve missing data; it prevents qualitative model compatibility from being mistaken for empirical mechanism identification.

# 5. Software and reproducibility

The reusable implementation is `channel_id/state_separability.py`. `StateDiagnostic` accepts event counts and reports sensitivity, false-negative rate, false-positive rate, specificity, Youden's J and a positive likelihood ratio. `diagnostic_from_frequencies` provides the same transformation for already-aggregated simulation outputs. A descriptive ranking function is included for comparing diagnostics within one declared study.

The island demonstration is fully source-traceable through frozen JSON results, exact-regeneration tests and deterministic figure exporters. The source-level Supplementary matrix documents all 13 strict external systems and their interpretation boundaries.

# 6. Conclusions

Flexible ecological simulations need two evaluations: **can the model generate the observed state, and does that state identify the mechanism?** Frozen state-separability analysis makes the second question explicit using the model's own interventions. In the demonstration, mixed-sign branching and strong sign rescue were specific but insensitive, whereas same-direction response and magnitude attenuation were poor mechanism discriminators.

Combining frozen state definitions, intervention-derived diagnostic rates, independently replicated causal boundaries and protected external failures provides a reproducible way to constrain interpretation without sacrificing the generative strengths of agent-based models. The method is complementary to pattern-oriented modelling and transferable beyond the ecological test case used here.

# References

Bascompte, J. & Scheffer, M. (2023). The Resilience of Plant–Pollinator Networks. *Annual Review of Entomology*, 68, 363–380. DOI: 10.1146/annurev-ento-120120-102424.

Grimm, V., Revilla, E., Berger, U., Jeltsch, F., Mooij, W.M., Railsback, S.F., Thulke, H.-H., Weiner, J., Wiegand, T. & DeAngelis, D.L. (2005). Pattern-oriented modeling of agent-based complex systems: lessons from ecology. *Science*, 310, 987–991. DOI: 10.1126/science.1116681.

Grimm, V. & Railsback, S.F. (2012). Pattern-oriented modelling: a ‘multi-scope’ for predictive systems ecology. *Philosophical Transactions of the Royal Society B*, 367, 298–310. DOI: 10.1098/rstb.2011.0180.

Grossenbacher, D.L. et al. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. DOI: 10.1111/nph.14534.

Marjakangas, E.-L., Dalsgaard, B. & Ordonez, A. (2025). Fundamental Interaction Niches: Towards a Functional Understanding of Ecological Networks' Resilience. *Ecology Letters*, 28, e70146. DOI: 10.1111/ele.70146.

Sirén, J., Somervuo, P. & Ovaskainen, O. (2025). Agent-based versus correlative models of species distributions: Evaluation of predictive performance with real and simulated data. *Methods in Ecology and Evolution*, 16, 1295–1307. DOI: 10.1111/2041-210X.70016.

Traveset, A. & Navarro, L. (2018). Plant reproductive ecology and evolution in the Mediterranean islands: state of the art. *Plant Biology*, 20(Suppl. 1), 63–77. DOI: 10.1111/plb.12636.

Whittaker, R.J., Fernández-Palacios, J.M. & Matthews, T.J. (2023). Island evolutionary syndromes in—and involving—plants. In *Island Biogeography*, 3rd ed., pp. 283–308. Oxford University Press. DOI: 10.1093/oso/9780198868569.003.0011.

Zell, A.N., Miranda, C.H., Grady, E.L., Grossenbacher, D.L. & Igić, B. (2025). Island colonization in flowering plants is determined by the interplay of breeding system, lifespan, floral symmetry, and arrival opportunity. *New Phytologist*, 245, 420–432. DOI: 10.1111/nph.20234.
