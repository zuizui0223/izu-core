# Journal positioning — simulation manuscript

Updated: 2026-08-24

## Decision

### First target: Methods in Ecology and Evolution — conditional YES

The current manuscript is potentially suitable for **Methods in Ecology and Evolution (MEE)** only if the paper is framed as a general methodological contribution rather than primarily as an ecological application to island pollination.

MEE's current scope states that the emphasis is on the **description and analysis of new methods and methodological approaches, not the results of applying existing or new methods**. Methods may be analytical, practical or conceptual. A recent MEE paper (Sirén, Somervuo & Ovaskainen 2025; DOI `10.1111/2041-210X.70016`) explicitly used agent-based simulations to evaluate when mechanistic versus correlative models are informative, confirming that ABM-based methodological evaluation is within scope.

The island-pollination application should therefore function as the worked ecological test bed, not as the sole novelty.

## The methodological contribution to foreground

Working name:

> **Frozen state-separability analysis for agent-based ecological models**

The method has four linked components:

1. **Freeze the forward state vocabulary before external challenge.**
   - Define which qualitative outcome classes the model already generates.
   - Prevent external cases from redefining states or choosing parameters after inspection.

2. **Use interventions/ablations to create a mechanism-to-state matrix.**
   - Ask which factors generate a state, which only reallocate state identity, and which only change magnitude.
   - Independently replicate the central intervention boundary with a predeclared stochastic block.

3. **Quantify inverse state separability.**
   - Treat an observable state as a diagnostic test of an intervention-defined mechanism.
   - Report sensitivity, false-positive rate and specificity.
   - Explicitly show that forward model coverage does not imply inverse mechanism identification.

4. **Protect external falsification and state-space misses.**
   - Challenge the frozen vocabulary with independent empirical systems without numerical fitting.
   - Retain failed predictions.
   - Predeclare that a future state outside the vocabulary is a state-space miss before any model extension.

This is broader than the island application. It can be applied to ABMs of fragmentation, mutualistic networks, disease, community assembly, social–ecological systems or other complex systems whenever several mechanisms can generate overlapping macroscopic states.

## What is actually new relative to pattern-oriented modelling

Pattern-oriented modelling (POM) already advocates using multiple empirical patterns to constrain bottom-up models and reduce equifinality. The present manuscript should **not** claim to invent multi-pattern ABM validation.

The narrower methodological addition is:

> convert the model's intervention structure into explicit **observation-to-mechanism diagnostic performance** after forward state generation has been frozen.

POM asks whether multiple patterns constrain model structure. The proposed state-separability layer additionally asks:

- if a model generates pattern/state `S`, how sensitive is `S` to the mechanism intervention?
- how often does `S` arise while the candidate mechanism is present versus absent?
- which commonly observed states are non-identifying despite being model-compatible?
- which failed external states or signed predictions remain protected rather than being absorbed into the model?

Thus the methodological novelty is **forward coverage + inverse diagnostic separability + protected falsification**, not ABM simulation itself.

## Required manuscript reframing for MEE

### Title

Preferred MEE-facing title:

> **From state generation to mechanism identification: a frozen separability framework for agent-based ecological models**

Application-bearing alternative:

> **From state generation to mechanism identification in agent-based ecology: an island plant–pollinator test case**

The current ecological title can remain as an alternative for a non-methods journal.

### Abstract

Lead with the method problem:

> Flexible ABMs can reproduce multiple ecological patterns, but reproducing a pattern does not establish which mechanism generated it.

Then introduce the four-step framework, with island pollination as the worked test case. The numerical island results become validation of the framework rather than the paper's opening novelty.

### Introduction

The preferred order is:

1. ABM flexibility and equifinality / POM;
2. unresolved inverse problem: state compatibility versus mechanism identification;
3. proposed frozen state-separability workflow;
4. island plant–pollinator responses as a demanding test bed because they contain branching, propagation and buffering states.

This is the reverse of the current ecology-first draft.

### Methods

Add an explicit general algorithm independent of the island model:

```text
Input:
  frozen ABM M
  mechanism interventions I_1...I_k
  state classifier C
  optional external challenge set E

1. Freeze C and the stochastic/parameter envelope.
2. Generate matched outcomes under each intervention.
3. Estimate P(S | mechanism present) and P(S | mechanism absent).
4. Convert to sensitivity / FPR / specificity for each state-mechanism pair.
5. Independently replicate the highest-value causal boundary.
6. Challenge frozen state vocabulary against E without refitting.
7. Record prediction failures and state-space misses before extension.
```

The current code already implements these steps; no new simulation is required.

### Results

Order results as method demonstrations:

1. Frozen state atlas.
2. Intervention-based mechanism separation.
3. State diagnostic asymmetry.
4. Independent robustness of the strongest causal boundary.
5. External held-out challenge and retained falsification.

The 13-system island series should move later than the diagnostic-separability result.

### Discussion

The primary claim should be methodological:

> A state may be easy for a model to generate yet poor for identifying mechanism. Separability must therefore be measured rather than inferred from model fit.

Island biology becomes the ecological interpretation and demonstration of why the distinction matters.

## MEE-specific strengths

- Fully reproducible frozen outputs and deterministic figure generation.
- Explicit ablations rather than post-hoc narrative mechanism attribution.
- Independent stochastic replication of the central causal boundary.
- Failure-retaining design, including Dominica.
- Quantitative separability metrics from an ABM's own intervention structure.
- Generalisable beyond the focal island system.
- No requirement for a new field dataset to demonstrate the method.

## MEE-specific risks

1. **Perceived as an application paper.**
   - Highest risk.
   - Mitigation: ecology becomes the test case; separability workflow is the headline.

2. **Perceived as a repackaging of POM/equifinality.**
   - Mitigation: explicitly credit Grimm et al. 2005 and Grimm & Railsback 2012; define the incremental method as intervention-derived diagnostic sensitivity/specificity plus frozen external falsification.

3. **State classifier is qualitative.**
   - Mitigation: be explicit that this first implementation operates on sign/state classes. State classifiers can be continuous or probabilistic in future implementations. Do not imply the current framework is already a general statistical estimator.

4. **External challenge is not formal quantitative validation.**
   - Mitigation: call it held-out qualitative state challenge, not validation of mechanism.

5. **Potential model-specificity of the sensitivity/specificity values.**
   - Mitigation: the values are test-case results; the reusable contribution is the procedure for deriving them from interventions.

## Alternative journals

### Ecological Modelling — strongest scope fit, lower framing risk

If MEE rejects the conceptual-method novelty, **Ecological Modelling** is the most natural fallback. The journal routinely publishes ABM methodology, replication protocols and theoretical/simulation analyses. The current ecology-first draft would need much less reframing.

Recommended framing there:

> State-dependent response and identifiability in a frozen agent-based island pollination model.

### Ecology Letters — high-risk conceptual option

Potential only if the paper is condensed around the general ecological insight that **state-dependent response plus diagnostic asymmetry** resolves why comparable biotic simplification produces divergent outcomes. The current qualitative external validation and abstract trait coordinate probably make this substantially higher risk than MEE or Ecological Modelling.

### Frontiers in Ecology and Evolution — Models in Ecology and Evolution

Clear scope fit for simulation and theoretical ecology, but not preferred over MEE/Ecological Modelling if the objective is methodological visibility.

## Recommended submission sequence

1. **Methods in Ecology and Evolution** — after method-first restructuring, no new analysis.
2. **Ecological Modelling** — if editors judge the separability layer insufficiently novel as a general method.
3. Broader modelling/theoretical outlet only after considering reviewer/editor feedback rather than adding simulations pre-emptively.

## No-analysis rule

Journal positioning does **not** reopen the simulation programme. Before first submission, do not:

- add more random seeds;
- fit the 13 island systems numerically;
- add generic mechanisms;
- collect field data for the primary claim;
- rescue Dominica;
- search for extra external success cases.

Editorial work should first test whether the existing frozen analysis already communicates the general method clearly enough.

## References for journal positioning

Grimm, V. et al. (2005). Pattern-oriented modeling of agent-based complex systems: lessons from ecology. *Science* 310:987–991. DOI `10.1126/science.1116681`.

Grimm, V. & Railsback, S.F. (2012). Pattern-oriented modelling: a ‘multi-scope’ for predictive systems ecology. *Philosophical Transactions of the Royal Society B* 367:298–310. DOI `10.1098/rstb.2011.0180`.

Sirén, J., Somervuo, P. & Ovaskainen, O. (2025). Agent-based versus correlative models of species distributions: Evaluation of predictive performance with real and simulated data. *Methods in Ecology and Evolution* 16:1295–1307. DOI `10.1111/2041-210X.70016`.
