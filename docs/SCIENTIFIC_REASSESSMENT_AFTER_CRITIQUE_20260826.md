# Scientific reassessment after manuscript critique

Updated: 2026-08-26

## Decision

The current Journal of Ecology Research Article framing is **not submission-ready**. The scientific outputs remain useful, but the manuscript overstates model-internal decompositions as discoveries and overstates qualitative external-state coverage as validation.

The Chapter 2 programme is therefore reopened for scientific reframing. No result is deleted; claim roles are reassigned.

## 1. H2: not a pure tautology, but oversold

The exact v12 endpoint identity is

`sign(Delta reproduction) = sign(Delta service) = sign(Delta functional opportunity)`.

This means downstream transforms do not create response sign. However, switching initial trait-position heterogeneity OFF does **not** make every lineage mathematically identical: trait-adjustment heterogeneity remains ON in that ablation, so lineages can still follow different trait trajectories and can in principle finish with different functional-opportunity contrasts. The observed collapse of branching is therefore not forced solely by the endpoint identity.

Nevertheless, the correct interpretation is narrower than `replicated_minimal_generator` suggests. The ablation shows that, **under the declared parameterization and tested residual factor ranges**, initial functional position dominates the other tested heterogeneity sources in generating sign-crossing opportunity contrasts. The independent seed block is a stochastic robustness check of that model-specific dominance, not independent evidence for a new algebraic principle.

### Required manuscript change

- Remove H2 as the headline discovery.
- Remove `replicated_minimal_generator` language from the main text.
- Present the sign identity as model structure and the ablation as a sensitivity/decomposition result.
- If a Research Article is retained, replace the headline with a nontrivial question about the parameter/geometry conditions under which response sign changes.

## 2. H5: qualitative coverage is not strong validation

The current external vocabulary contains branching, same-direction propagation, buffering/alternative response, and axis decoupling. These broad classes cover much of the possible sign-level outcome space. Therefore `11/11 covered or sign-compatible` has weak falsifiability and should not be reported as validation of the response architecture.

Dominica is a genuine retained failure of a **more specific signed-position projection**, but it does not falsify the broad state vocabulary.

### Required manuscript change

- Remove H5 as a supported validation hypothesis.
- Retain the 13 systems as comparative grounding / examples of ecological response diversity.
- Retain Dominica as a failed specific empirical projection.
- Do not report 11/11 coverage as evidence of generality.

## 3. Numerical reporting and uncertainty

The headline mixed-sign result is 5/12 runs, not a stable population-frequency estimate. Reporting `0.4167` implies unwarranted precision. The same issue applies to 16/96, 11/96 and related capability counts when presented without their design context.

### Required manuscript change

- Report integer counts first (`5 of 12`) rather than four-decimal proportions.
- Do not interpret these design frequencies as natural prevalence.
- If frequencies remain scientifically important, broaden the parameter/design envelope and report uncertainty/sensitivity across that envelope rather than treating one frozen design as a sampling population.

For reference only, a simple Wilson interval for 5/12 would be roughly 0.19–0.68; because the 12 runs span three saturation settings, even that interval should not be treated as an inferential population CI without a clearer sampling model.

## 4. Model description is currently insufficient

The model implementation contains concrete assumptions that are not exposed adequately in the manuscript.

### Core scenario values in v4

Mainland-like:
- pollinator types: 9
- partner arrival: 0.28
- partner loss: 0.015
- pollinator trait dispersion: 0.22
- generalist fraction: 0.35
- replacement fraction: 0.05

Oceanic-island:
- pollinator types: 4
- partner arrival: 0.12
- partner loss: 0.055
- pollinator trait dispersion: 0.16
- generalist fraction: 0.58
- replacement fraction: 0.22

Lineage defaults:
- initial functional trait: truncated Normal(mean 0.5, SD 0.18)
- pollinator dependency: Uniform(0.35, 0.95)
- assurance ceiling: Uniform(0.10, 0.90)
- assurance responsiveness: Uniform(0.004, 0.035)
- trait adjustment: Uniform(0.01, 0.055)

Matching:
- mismatch is absolute plant–pollinator trait distance
- match is Gaussian-like: `exp(-(mismatch / breadth)^2)`
- introduced partners receive a multiplicative 0.82 factor
- breadth is 0.42 for generalists and 0.16 otherwise

Fixed visit budget:
- service uses mean partner match rather than accumulating visitation with richness
- `pollination = 1 - exp(-saturation * mean_service)`

The manuscript must state these assumptions, explain which are empirical direction choices versus generic sensitivity settings, and stop implying that the model is reproducible from the prose when these values are omitted.

The ecological meanings of 24 lineages, 120 steps and saturation values 1/2/3 are not empirically identified. They should be described as design/sensitivity choices unless a source-based rationale is added.

## 5. Trait adjustment is weak in the current envelope

Removing trait-adjustment heterogeneity changed only 2/288 response signs in the original residual block and 5/288 in the independent block, while branching frequency was unchanged.

This does not invalidate a post-establishment ecological-response paper, but it means the current simulation does **not** provide meaningful evidence about in-situ evolutionary dynamics. Evolution should remain one of the conceptual three layers of island syndrome, while the model is explicitly restricted to the third layer: post-establishment ecological response.

## 6. Local context result needs semantic correction

The manuscript currently describes `support ON` as if local support is added. In v9, however, `support_strength` is a local-availability filtering/stress parameter: positive plant/resource rows are retained with probability `1 - support_strength`, followed by pollinator/pair support projection. Thus `support_strength = 0.5` means substantial local filtering, not an added beneficial support resource.

The rescue/worsening result is still potentially nontrivial: local realization/filtering can redistribute effective service so that some lineage contrasts improve and others worsen. But the ecological label must be changed from `additional local support` / `support ON` to neutral language such as **local context realization**, **local availability filtering**, or **interaction-context filtering**.

This bidirectionality is one of the stronger remaining simulation results.

## 7. Autonomous assurance is mostly a structural contrast, not a discovery

The model explicitly increases assurance when reproduction falls below 0.50 and caps it at a lineage-specific ceiling. Turning this route on while holding upstream service fixed is therefore designed to add a compensating reproductive route. Magnitude attenuation should not be presented as a surprising emergent discovery.

The informative result is narrower: within the tested parameterization, this compensating route rarely/never crosses the sign boundary, so **magnitude buffering and qualitative sign rescue are distinct properties**. That distinction is useful, but it is a model-structure/parameter result rather than empirical evidence for natural island assurance.

## 8. Procedural language should be reduced

Terms such as `frozen`, `predeclared`, `stop rule`, `protected falsification`, `claim boundary`, and `inference guard` are useful for provenance but currently dominate the scientific narrative.

Main text should retain only procedures that affect inference. Workflow failures and import-path repair belong in repository provenance, not Methods. The sentence describing the import-path failure and lack of further seed search should be removed from the manuscript.

## 9. Reference hygiene

Lord (2015) and Méndez (2025) currently appear in the reference list without a clear main-text citation. Either cite them where they contribute to the island-syndrome argument or remove them from the main reference list.

## 10. Positive contribution that survives the critique

The strongest defensible contribution is not `initial heterogeneity is the minimal generator` and not `11/11 external systems were covered`.

The surviving conceptual contribution is:

> **Island syndromes conflate three distinct processes—assembly filtering, in-situ evolution, and post-establishment interaction response—and the third process is conditional rather than monotonic: the effect of pollinator reorganization depends on plant–pollinator matching geometry and can be further redirected, in either direction, by local interaction context, while downstream reproductive assurance changes magnitude without necessarily changing sign.**

This is a useful ecological architecture, but the present Research Article needs one more nontrivial quantitative contribution to match the strength of the conceptual framing.

## 11. Recommended Research Article recovery route

Do not add more workflow machinery. Add scientific content only where it changes inference.

Highest-value route:

1. Replace H2 with a **response-geometry question**: under what combinations of plant starting position and pollinator-community change does the sign of functional-opportunity response switch?
2. Derive/plot the response surface or threshold rather than treating the existence of initial-state dependence as a discovery.
3. Sweep the parameters that define the island perturbation and matching geometry (trait dispersion, generalist fraction/breadth, replacement penalty/fraction, partner loss/arrival, saturation, initial trait dispersion, and trait-adjustment scale) to identify where bidirectional responses exist versus collapse to one direction.
4. Treat local context filtering as a second-stage perturbation and quantify when it changes sign versus only magnitude.
5. Treat assurance as a downstream structural modifier and quantify the parameter threshold for sign rescue, rather than counting attenuation as a discovery.
6. Use the 13 island systems only as ecological examples/boundaries, not as validation coverage.

If this response map yields a stable, interpretable region structure, the paper can again support a Research Article claim. If it does not, the better product is a conceptual Review/Mini-review centered on the three-layer island-syndrome decomposition.

## Submission status after reassessment

- Current Journal of Ecology Research Article: **not ready to submit**.
- Existing simulations: retained as exploratory/model-decomposition evidence.
- H2 headline: demote.
- H5 validation: demote.
- H3 local-context bidirectionality: retain after semantic correction and robustness check.
- H4 magnitude/sign distinction: retain as a structural distinction, not a headline discovery.
- Three-layer island-syndrome decomposition: retain as conceptual core.
- Next scientific gate: response-geometry / parameter-robustness analysis, not more manuscript packaging.
