# From state generation to mechanism identification: a frozen separability framework for agent-based ecological models

## Methods in Ecology and Evolution — method-first draft

### Running example

Island plant–pollinator responses under functional biotic simplification

---

## Abstract

1. **Agent-based models can reproduce multiple ecological patterns, but model flexibility creates an inverse problem: generating an observed state does not establish which mechanism generated it.** Pattern-oriented modelling addresses equifinality by confronting bottom-up models with multiple patterns, yet state compatibility is still often interpreted more strongly than the intervention structure of the model warrants.

2. We introduce a **frozen state-separability workflow** for agent-based ecological models. The workflow (i) freezes an observable state vocabulary before external challenge, (ii) uses matched mechanism interventions or ablations to estimate the frequency with which each state is expressed when a candidate mechanism is present versus absent or replaced, (iii) converts these frequencies to diagnostic sensitivity, false-positive rate and specificity, (iv) independently replicates the highest-value intervention boundary under a predeclared stochastic design, and (v) challenges the frozen state vocabulary with external systems while protecting prediction failures and state-space misses from post-hoc model extension.

3. We demonstrate the workflow using a frozen plant–pollinator ABM motivated by island biotic simplification. Removing pre-existing lineage functional-position heterogeneity eliminated within-run response-sign branching in both the original and independently seeded blocks (mixed-sign frequency 0.4167 → 0 in each), whereas other residual single-factor ablations retained branching. Local network context rescued reproductive sign in 16/96 eligible declines but worsened 11/96, while autonomous assurance attenuated 207/216 declines but produced 0/216 sign rescues and 0/525 across a broadened envelope.

4. These interventions revealed strong **diagnostic asymmetry**. Mixed-sign branching was specific (1.0) but insensitive (0.4167) for initial functional-position heterogeneity. Same-direction response produced a 0.5833 false-positive rate when used to infer trait uniformity. Strong sign rescue was specific (1.0) but insensitive (0.1667) for network context against the tested assurance route, whereas magnitude attenuation had specificity only 0.1146 because both routes commonly generated it.

5. In a held-out qualitative application, 11 generative cases among 13 strict island systems were covered or sign-compatible with the already-frozen state vocabulary; one reproductive-axis-decoupling constraint and one failed signed prediction were retained rather than absorbed into the model. **Frozen state separability therefore distinguishes forward generative adequacy from inverse mechanism identification and supplies explicit failure rules for flexible ecological simulations.** The diagnostic API and reproducible workflow are independent of the island application and can be applied wherever simulation interventions generate overlapping macroscopic states.

**Keywords:** agent-based model; model validation; equifinality; pattern-oriented modelling; sensitivity; specificity; ecological networks; falsification

---

# 1. Introduction

Agent-based and individual-based models are widely used to study ecological systems in which population- or community-level patterns emerge from interactions among heterogeneous entities. Their strength is also a central inferential difficulty. Because an ABM may contain multiple interacting mechanisms and stochastic pathways, the same macroscopic pattern can often arise from different internal configurations. Conversely, an important mechanism may produce its most diagnostic macroscopic pattern only in a subset of realizations. A model may therefore be **generatively adequate**—capable of reproducing an observed state—without that state being **mechanistically identifying**.

Pattern-oriented modelling (POM) provides a foundational strategy for constraining bottom-up ecological models through multiple empirical patterns rather than a single fitted target (Grimm et al. 2005; Grimm & Railsback 2012). POM is explicitly motivated by the need to reduce structural uncertainty and equifinality. Yet an additional inverse question remains useful after a model has generated a set of candidate patterns: **how informative is a particular observable state about a particular model mechanism?** In many modelling studies, this distinction is handled qualitatively. A pattern is described as “consistent with” or “supporting” a mechanism because the model can produce it. But forward compatibility alone does not quantify how often the same pattern would appear if that mechanism were removed or replaced.

Here we formulate this inverse question as an intervention-derived diagnostic problem. Suppose a frozen model contains an observable state `S` and a declared mechanism contrast `M=1` versus `M=0`. Repeated matched simulations estimate `P(S|M=1)` and `P(S|M=0)`. The first quantity is analogous to sensitivity: how often does the model express the state when the mechanism is present? The second is a synthetic false-positive rate: how often does the same state appear when the mechanism is absent or when a declared alternative is active? Their combination quantifies **state separability** within the model family. High specificity with low sensitivity implies that a state is informative when observed but cannot be required in every realization. High sensitivity with low specificity implies that the state is easy to generate but weak for identifying mechanism.

The framework adds three safeguards. First, the state vocabulary, intervention contrasts and stochastic envelope are frozen before held-out external challenges are scored, preventing external cases from redefining the model after inspection. Second, the strongest causal boundary is independently replicated under a predeclared seed or seed-generation rule and a stop rule that accepts the first scientific result. Third, failures are protected: a failed signed prediction or a new external state outside the frozen vocabulary is recorded before model extension. The goal is not to replace POM but to add an explicit **forward-state / inverse-separability layer** to models already evaluated through interventions and patterns.

We demonstrate the workflow using a plant–pollinator ABM motivated by island systems. This is a useful stress test because island reproductive ecology contains recurrent broad patterns—such as non-random breeding-system representation and altered pollination systems—while individual island systems display heterogeneous downstream effects (Grossenbacher et al. 2017; Traveset & Navarro 2018; Whittaker et al. 2023; Zell et al. 2025). Network resilience theory further predicts that partner loss may be compensated through rewiring or alternative interactions rather than propagating monotonically to function (Bascompte & Scheffer 2023; Marjakangas et al. 2025). The resulting empirical vocabulary naturally contains branching, same-direction propagation, attenuation and buffering, precisely the kinds of overlapping states for which forward compatibility can be mistaken for mechanism identification.

We ask four methodological questions. **(1)** Can a state vocabulary be frozen from the model before external challenge? **(2)** Which interventions generate, eliminate or reallocate those states? **(3)** What sensitivity and specificity does each state have for its candidate mechanism contrast? **(4)** Does the frozen vocabulary remain useful when challenged by independent ecological systems without refitting? We show that the answer to the final question can be positive even when the inverse identification problem remains weak, and argue that this distinction should be reported explicitly in flexible simulation studies.

---

# 2. Method: frozen state-separability analysis

## 2.1 Step 1 — freeze the state vocabulary

Let an ecological simulation model `M` map an initial condition, parameter vector and stochastic stream to an outcome `Y`. A state classifier `C(Y)` assigns an observable state `S`. Before inspecting a held-out challenge set, investigators freeze:

- the model version;
- the parameter or scenario envelope under study;
- the state classifier and all zero/directional boundaries;
- the intervention contrasts to be interpreted mechanistically;
- the stochastic replication design for any confirmatory boundary.

The state classifier can be categorical or derived from continuous outcomes. The island implementation uses events such as within-run mixed-sign branching, same-direction response, sign rescue, magnitude attenuation and worsening.

Freezing is important because a flexible state vocabulary can absorb nearly any external case. A newly observed state may motivate a later model extension, but it should first be labelled a **state-space miss** under the frozen model.

## 2.2 Step 2 — create mechanism contrasts through intervention

For each candidate mechanism, define a mechanism-present intervention and a mechanism-absent or declared-alternative intervention. The intervention need not be binary in biological reality; it is a model experiment used to estimate whether an observable state separates specified mechanism settings.

For state `S`, record:

\[
p_1=P(S=1\mid M=1)
\]

and

\[
p_0=P(S=1\mid M=0).
\]

The current implementation reports:

\[
\text{sensitivity}=p_1,
\quad
\text{false-positive rate}=p_0,
\quad
\text{specificity}=1-p_0,
\quad
\text{false-negative rate}=1-p_1.
\]

We additionally expose Youden's `J = sensitivity + specificity - 1` and a positive likelihood ratio as descriptive summaries. These quantities are conditional on the simulation interventions and should not be interpreted as empirical diagnostic accuracies unless transport to natural systems is independently justified.

The reusable implementation is `channel_id/state_separability.py`. It accepts either event counts (`StateDiagnostic`) or already-frozen intervention frequencies (`diagnostic_from_frequencies`).

## 2.3 Step 3 — distinguish generation, allocation and attenuation

A mechanism can affect the model at different logical levels. We distinguish:

- **state generation:** removal eliminates the state boundary of interest;
- **state/branch allocation:** removal changes which units occupy which state without eliminating the state family;
- **magnitude modification:** removal changes response strength but rarely qualitative state;
- **non-discriminating mechanism:** removal has little effect in the tested conditional model.

This distinction avoids labelling every factor that changes an outcome as the “cause” of the state class.

## 2.4 Step 4 — independently replicate the strongest boundary

If one intervention supports the main causal claim, a new stochastic block is frozen before execution. Investigators specify the seed or seed-generation rule, replicate count, parameter envelope, state classifier, decision categories and stop rule. The first scientific result is accepted. Software failures occurring before scientific execution can be repaired without changing the frozen design, but must remain in provenance.

## 2.5 Step 5 — challenge externally without fitting

An optional external set `E` is then used to test whether independently observed ecological states fall inside the frozen state vocabulary. External states do not choose model parameters or mechanisms. Three outcomes remain distinct:

1. **state covered / compatible**;
2. **mechanism empirically identified**;
3. **state-space miss or prediction failure**.

Only the first follows from qualitative state compatibility.

## 2.6 Step 6 — protect falsification

Before external challenge, define observations that would weaken or reject candidate claims. Examples include persistence of a state after removal of a claimed necessary mechanism, matched worsening under a proposed universal buffer, failure of a sign-buffer mechanism to replicate, or a held-out signed response opposite to a frozen prediction. Model extension occurs only after the failure has been recorded under the frozen version.

---

# 3. Test-case model and interventions

The worked example uses a frozen plant–pollinator ABM in which multiple plant lineages experience a common shift in pollinator functional opportunity. Lineages occupy positions on a standardized functional matching axis and may differ in trait adjustment, local network support, pollinator dependency and reproductive assurance. The standardized axis is intentionally abstract and is not assigned post hoc to any single empirical floral trait.

The test case contains three intervention layers. A downstream factorial removes local support, dependency heterogeneity, assurance responsiveness and partner effectiveness to distinguish branch generation from reallocation. A residual factorial then removes initial trait-position heterogeneity, trait-adjustment heterogeneity and assurance-ceiling heterogeneity. Separate frozen blocks test network-context buffering and autonomous assurance. Detailed implementation and provenance are provided in the repository's frozen Methods and traceability files.

The external challenge was selected from a global screening denominator of 54 island/system units. Thirteen met strict state-challenge criteria. They were not used to calibrate the model.

---

# 4. Results

## 4.1 Intervention-defined branch generation

In the original residual block, mixed-sign branching occurred in 0.4167 of matched runs. Removing initial trait-position heterogeneity eliminated mixed-sign runs and reduced mean within-run branching balance to zero. Removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity individually did not collapse branching.

The central boundary replicated under the independently frozen seed `90260825`. Full-model mixed-sign frequency was 0.4167 and mean within-run balance 0.2917. Initial-trait removal again reduced both to zero and changed 44 paired lineage signs. The two other single residual ablations retained mixed-sign frequency 0.4167. Pre-existing lineage functional position was therefore the only tested residual factor whose removal eliminated within-run response-sign branching across both frozen blocks.

## 4.2 Branch allocation and buffering are distinct from generation

Two-sided branching persisted when the four tested downstream v11 modifiers were all fixed OFF. Nevertheless, local support strongly reallocated branch identity: its removal changed 105 of 288 paired signs, compared with 13 of 288 for partner effectiveness, one for assurance responsiveness and none for dependency heterogeneity.

In an independent network-context block, support ON produced sign rescue in 16 of 96 eligible negative reproductive contrasts and magnitude rescue in 85 of 96, but worsened 11 of 96. Thus local support has strong buffering capacity without being a monotonic protective mechanism.

Autonomous assurance occupied a different response region. In an independent block it attenuated 207 of 216 service-decline responses but produced no strong sign rescues. A broadened envelope likewise produced zero sign rescues in 525 eligible contrasts.

## 4.3 Forward state coverage did not imply inverse separability

The intervention frequencies produced strongly asymmetric diagnostics.

| observable state | mechanism contrast | sensitivity | false-positive rate | specificity | interpretation |
|---|---|---:|---:|---:|---|
| mixed-sign branching | initial heterogeneity ON vs OFF | 0.4167 | 0.0000 | 1.0000 | specific but insensitive |
| same-direction response | uniformity vs heterogeneity ON | 1.0000 | 0.5833 | 0.4167 | weak inverse diagnostic |
| strong sign rescue | network context vs assurance | 0.1667 | 0.0000 | 1.0000 | specific but insensitive |
| magnitude attenuation | assurance vs network context | 0.9583 | 0.8854 | 0.1146 | largely non-separable |

Thus the most frequent state was not necessarily the most informative. Same-direction responses occurred commonly even while the necessary branching generator was present. Magnitude attenuation was generated readily by more than one downstream route.

## 4.4 Held-out ecological states tested coverage, not mechanism identity

Thirteen island systems entered the strict external challenge. Eleven were generative targets—three branching, six same-direction and two buffering/alternative cases—and every one was covered or sign-compatible with an already-frozen state class. One additional system was retained as a reproductive-axis-decoupling constraint. A frozen signed-position prediction for Dominica failed and remained failed.

No external case changed a model parameter, seed, mechanism or state label. The external challenge therefore demonstrated qualitative state-space reach while preserving the distinction between coverage and mechanism identification.

---

# 5. Discussion

## 5.1 The methodological problem is inverse, not merely generative

Ecological ABMs are often evaluated by asking whether they reproduce an observed pattern. That question is necessary but incomplete. Our test case shows that a mechanism can be essential for a state family while its most distinctive state appears in fewer than half of stochastic runs. Conversely, a visually compelling but common state can be generated under multiple mechanisms. Forward success therefore has different evidential value depending on the intervention-derived separability of the state.

This distinction complements pattern-oriented modelling. POM uses multiple patterns to constrain bottom-up models and reduce equifinality (Grimm et al. 2005; Grimm & Railsback 2012). Frozen state separability asks an additional conditional question after interventions are available: **how much does observing each state change what the model permits us to infer about mechanism?** Expressing the answer through sensitivity and specificity makes two common modelling errors visible: treating absence of an insensitive state as evidence against a mechanism, and treating presence of a nonspecific state as evidence for it.

## 5.2 Freezing protects flexible models from absorbing failures

The second methodological contribution is procedural. State labels, intervention boundaries and confirmatory stochastic designs were fixed before external challenge. The strongest causal boundary was replicated under a predeclared independent seed and stop rule. The external challenge retained both an axis-decoupling constraint and a failed signed prediction. This prevents the common failure mode in which a flexible model is successively reinterpreted until every case becomes compatible.

The approach is intentionally conservative. It does not prevent later model extension; it imposes an ordering. A miss is first a miss under version `M_t`. A new mechanism can then define `M_{t+1}` and face its own frozen challenge. That versioned structure is especially useful for ABMs because adding plausible local rules can otherwise increase explanatory flexibility faster than falsifiability.

## 5.3 Island pollination illustrates why separability matters

Island plant reproduction provides a useful example because several distinct ecological processes can produce superficially similar outcomes. Macrocomparative studies support colonization filters favouring self-compatible or otherwise establishment-capable lineages (Grossenbacher et al. 2017; Zell et al. 2025), while reviews describe heterogeneous within-island reproductive and pollination shifts (Traveset & Navarro 2018; Whittaker et al. 2023). Pollination-network theory adds rewiring and alternative functional partners as possible routes to resilience (Bascompte & Scheffer 2023; Marjakangas et al. 2025).

In the ABM, this heterogeneity becomes a diagnostic problem. Same-direction response is compatible with several starting-state configurations. Decline attenuation can arise from both local network context and autonomous assurance. Strong sign rescue is more discriminating but uncommon. Therefore, describing an empirical island as “buffered” or “directionally responding” gives less mechanistic information than the labels may suggest.

The external island series should accordingly be interpreted as a demonstration of the method's **state-space challenge**, not as proof that one synthetic mechanism explains 13 real systems. This is an advantage rather than a weakness of the framework: it states exactly where an ecological application ends and where empirical mechanism mapping must begin.

## 5.4 Generalisation beyond islands

Nothing in the separability calculation requires islands or pollination. The same workflow can be applied whenever a simulation contains intervention-defined mechanisms and observable macroscopic states. Examples include alternative stable states in community models, epidemiological regimes, fragmentation responses, social–ecological adaptation, metacommunity assembly and urban ecological networks.

For a habitat-fragmentation ABM, for example, an investigator might freeze states such as collapse, persistence and functional compensation; ablate dispersal, local redundancy and behavioural adaptation; then ask whether persistence is a sensitive or specific diagnostic of any one route. In disease models, the states could be epidemic extinction, endemic persistence and resurgence, with interventions on contact structure or immunity. The method does not require the state classifier to remain qualitative: continuous outcomes can be thresholded prospectively or replaced by probabilistic state classifiers, provided their definitions are frozen before challenge.

## 5.5 Limitations

The framework quantifies **model-conditional** separability. Sensitivity and specificity are functions of the chosen stochastic envelope, intervention contrast and state definition. They are not empirical diagnostic accuracies. A high-specificity synthetic state can motivate an empirical test, but transport to nature requires separate evidence that the model intervention corresponds to a measurable biological mechanism.

The current demonstration uses simple event frequencies. This makes the method transparent and suitable for already-frozen simulation outputs, but it does not yet provide uncertainty intervals, hierarchical pooling across parameter regions or continuous-state discrimination. Those are natural methodological extensions, not requirements for the present proof of concept.

Likewise, an absent mechanism in a simulation is not necessarily a biologically realistic counterfactual. Separability is always relative to the declared intervention family. Investigators should therefore state the alternative intervention explicitly rather than report specificity as if all natural mechanisms had been excluded.

Finally, external challenge quality still depends on empirical source quality. The current island application deliberately separates qualitative state coverage from source-native mechanism mapping. The method does not solve data limitations; it prevents model compatibility from obscuring them.

---

# 6. Practical workflow and software

The reusable implementation is provided in `channel_id/state_separability.py`.

Minimal use:

```python
from channel_id.state_separability import StateDiagnostic

row = StateDiagnostic(
    state="mixed_sign_branching",
    mechanism_present="heterogeneity_on",
    mechanism_absent_or_alternative="heterogeneity_off",
    present_state_events=5,
    present_total=12,
    absent_state_events=0,
    absent_total=12,
)

print(row.sensitivity)
print(row.false_positive_rate)
print(row.specificity)
```

Recommended full workflow:

```text
freeze model + state classifier
        ↓
run matched mechanism interventions
        ↓
construct mechanism × observable-state table
        ↓
compute sensitivity / FPR / specificity
        ↓
replicate the strongest boundary independently
        ↓
challenge frozen states externally without refitting
        ↓
retain failures and state-space misses
```

A descriptive ranking by Youden's J is provided for comparing candidate diagnostics inside the same declared study. This ranking should not be used as a substitute for biological judgment or as an empirical model-selection score.

---

# 7. Conclusions

Flexible ecological simulations need two evaluations: **can the model generate the observed state, and does that state identify the mechanism?** Frozen state-separability analysis makes the second question explicit using the model's own interventions. In the island plant–pollinator demonstration, the strongest forward states were not always the strongest inverse diagnostics: mixed-sign branching and strong sign rescue were specific but insensitive, while same-direction response and magnitude attenuation were poor mechanism discriminators.

By combining frozen state definitions, intervention-derived diagnostic rates, independently replicated causal boundaries and protected external failures, the workflow provides a reproducible way to constrain interpretation without sacrificing the generative strengths of agent-based models. The method is complementary to pattern-oriented modelling and is applicable beyond the ecological test case used here.

---

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

---

## Submission-boundary note

For an MEE submission, the method-first version is preferred over the ecology-first draft. Do not add new simulations before editorial review. The next work is software/API documentation, exact-regeneration CI, source-level Supplementary references for the island challenge, and prose shortening to journal length.
