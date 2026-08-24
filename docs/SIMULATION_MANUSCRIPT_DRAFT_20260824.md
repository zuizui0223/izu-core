# State-dependent branching and asymmetric mechanism identifiability in island plant–pollinator responses

## Working manuscript draft — 2026-08-24

### Alternative title

**One perturbation, multiple island response states: a frozen agent-based test of branching, buffering and identifiability**

---

## Abstract

Island plant reproduction is often discussed in terms of recurrent syndromes, including increased self-compatibility, generalized pollination and altered plant–pollinator interactions. Yet island systems also show strikingly different downstream outcomes under apparently similar losses or reorganizations of pollinator function. This raises a mechanistic problem: can a common perturbation generate divergent reproductive response states without fitting a different model to every island, and how much can an observed state reveal about the mechanism that generated it?

We addressed these questions with an agent-based model whose mechanism stack, parameter envelopes and stochastic tests were frozen before external island-system challenge. We separated forward state generation from inverse mechanism identification using factorial and drop-one ablations, independently seeded robustness blocks, and a qualitative external challenge drawn from a global screen of 54 island/system units. No external island outcome was used to select parameters, random seeds or mechanisms.

Within the declared residual model, pre-existing lineage position in functional trait space was the only tested factor whose removal eliminated within-run response-sign branching. Mixed-sign branching occurred in 0.4167 of matched runs in both the original and independently seeded blocks, but fell to zero when initial trait-position heterogeneity was removed in both blocks. Local network context acted as a strong but bidirectional branch allocator: in an independent block it rescued reproductive sign in 16 of 96 eligible declines, attenuated 85 of 96, and worsened 11 of 96. Autonomous assurance occupied a different synthetic regime, attenuating 207 of 216 declines but producing 0 of 216 sign rescues; sign rescue also remained absent across a broadened 525-contrast envelope. Consequently, state observations were asymmetrically diagnostic: mixed-sign branching and strong sign rescue were high-specificity but low-sensitivity signals, whereas same-direction responses and magnitude attenuation were weak mechanism discriminators.

Thirteen strict external island systems were retained after global screening. Eleven were generative state challenges—three branching, six same-direction propagation and two buffering/alternative cases—and all were qualitatively covered or sign-compatible with an already-frozen model state. One system was retained as a reproductive-axis-decoupling constraint and one frozen signed-position prediction failed and was retained as a falsification.

These results support a state-dependent rather than syndrome-only view of island pollination responses. A common functional perturbation can generate divergent outcomes because lineages enter the perturbation from different functional positions, while downstream network context and reproductive filters modify propagation. At the same time, qualitative state compatibility cannot by itself identify the real-world causal mechanism. The framework therefore joins forward generative testing with explicit limits on inverse inference.

**Keywords:** agent-based model; island biogeography; plant–pollinator networks; reproductive assurance; interaction rewiring; equifinality; pattern-oriented modelling; ecological resilience

---

# 1. Introduction

Islands have long served as natural laboratories for understanding how colonization, ecological simplification and altered biotic interactions reshape plant reproduction. Classic and contemporary comparative studies show that reproductive traits are non-randomly represented on islands: self-compatible species are over-represented in several major flowering-plant clades, and recent global analyses indicate that breeding system interacts with lifespan, floral traits and arrival opportunity to influence island colonization (Grossenbacher et al. 2017; Zell et al. 2025). Reviews of island plant evolution likewise identify recurrent shifts in breeding systems, floral traits and pollination mechanisms as candidate components of broader island evolutionary syndromes (Whittaker et al. 2023). These macroevolutionary patterns are important, but they mix at least two distinct processes. Some traits may act as **filters on which lineages colonize or persist on islands**, whereas other changes arise **after an established lineage experiences a changed pollinator environment**. The two processes need not produce the same predictions. Indeed, empirical reviews of island reproductive ecology emphasize substantial heterogeneity among taxa, islands and response axes rather than a single universal reproductive trajectory (Traveset & Navarro 2018).

A second source of heterogeneity lies in the interaction network itself. Pollination function is not determined solely by the presence or absence of a nominal pollinator guild. Species loss, abundance change, partner replacement, altered interaction strength and the emergence of novel interactions can reorganize ecological networks without necessarily producing proportional loss of ecosystem function. Network theory therefore increasingly treats resilience as a property of the interacting system, with rewiring, heterogeneity and redundancy among the mechanisms capable of maintaining function under perturbation (Bascompte & Scheffer 2023). Recent functional-network frameworks extend this idea by distinguishing realized interactions from the broader functional interaction space within which new partners can emerge (Marjakangas et al. 2025). Such perspectives make a simple prediction difficult: the same decline in global pollinator opportunity may propagate strongly in one plant lineage, be absorbed by altered partner allocation in another, and be attenuated downstream by reproductive assurance in a third.

This creates a modelling problem as well as a biological one. Bottom-up agent-based models are attractive because they can represent heterogeneous lineages, interaction networks and adaptive or reproductive feedbacks explicitly. However, a model that can reproduce many patterns is not automatically explanatory. Pattern-oriented modelling was developed partly to address this problem by confronting bottom-up models with multiple independent patterns rather than calibrating to a single target (Grimm et al. 2005; Grimm & Railsback 2012). A central difficulty is **equifinality**: different mechanisms can generate the same macroscopic pattern, while a genuinely important mechanism may generate its diagnostic pattern only in a subset of stochastic realizations. Consequently, there are two different inferential questions. The forward question is whether a frozen mechanism can generate an observed state. The inverse question is whether observing that state identifies the mechanism. Conflating the two risks interpreting qualitative model compatibility as causal evidence.

Here we use island plant–pollinator responses to separate these questions explicitly. We first freeze a minimal agent-based architecture in which a common shift in pollinator functional opportunity acts on plant lineages occupying different positions in a standardized functional trait space. We then use factorial and residual ablations to ask which implemented factors generate within-environment response branching and which instead reallocate branch identity or attenuate downstream reproductive effects. Central mechanism claims are subjected to independently seeded robustness blocks, with failure states specified before inspection. Only after this synthetic state structure is frozen do we challenge it with external island systems selected from a global literature screen.

We address three questions. **First**, can one frozen model architecture generate recurrent island-response classes—branching, same-direction propagation and buffering—without system-specific retuning? **Second**, which mechanism axes minimally generate those states or move lineages among them? **Third**, how informative is an observed state about the mechanism that produced it? We make a deliberately asymmetric prediction: some observations should be highly specific but insensitive diagnostics, whereas others should be common outputs of multiple mechanisms and therefore weak for inverse identification. External island systems are used only as qualitative held-out state challenges, not as calibration targets. This design allows state-space coverage, mechanism separability and falsification to remain distinct claims.

---

# 2. Methods

## 2.1 Study boundary and preregistered logic

The study was designed as a simulation analysis with qualitative external island-system challenges. All primary manuscript numbers trace to frozen model outputs listed in `data/design/simulation_manuscript_methods_traceability.json`. External island outcomes were not used to choose random seeds, tune parameter values, add mechanisms, redefine state classes or rescue failed projections. New field data and the separate empirical visitor-rate × per-visit-effectiveness mapping programme were not admission requirements for the primary simulation analysis.

The full source-traceable Methods text is frozen in `docs/SIMULATION_MANUSCRIPT_METHODS_FROZEN_20260824.md`. The sections below provide the manuscript-level summary.

## 2.2 Frozen model architecture

The model represents multiple plant lineages exposed to matched mainland-like and oceanic-like pollinator environments. Pollination opportunity emerges from interactions between lineage state and pollinator traits under a fixed visit-budget formulation. Plant lineages can differ in their initial standardized matching-trait position and, depending on the experimental layer, in trait adjustment, local support, pollinator dependency, assurance ceiling, assurance responsiveness and partner effectiveness.

The standardized matching trait is an abstract functional coordinate. We do not equate it with any one observed floral character. This prevents an empirical trait such as corolla length, colour, nectar guide or a composite functional score from being assigned to the model axis after its downstream response is known.

## 2.3 Downstream factorial: generation versus branch allocation

The v11 factorial toggled four downstream mechanism families—local support, dependency heterogeneity, assurance responsiveness and partner effectiveness—across matched stochastic runs. We summarized positive, negative and equal island–mainland reproductive contrasts, mixed-sign run frequency, branching balance and paired lineage sign changes. Persistence of mixed-sign responses with all four factors OFF was interpreted as evidence that downstream heterogeneity was not required to generate branching, whereas paired sign changes under drop-one ablations quantified branch reallocation.

## 2.4 Residual ablation of the branch generator

The v12 residual experiment fixed the four v11 downstream modifiers OFF and factorially manipulated three remaining lineage-level sources: initial trait-position heterogeneity, trait-adjustment heterogeneity and assurance-ceiling heterogeneity. The primary branching criterion was the occurrence of both positive and negative lineage responses within the same matched stochastic run. A residual factor was considered necessary within this declared gate if removing it eliminated mixed-sign runs and reduced mean within-run branching balance to zero while other single-factor removals retained branching.

## 2.5 Independent replication of the central v12 boundary

Before an independent robustness run, we froze seed `90260825`, four replicates at each saturation, 24 lineages, 120 steps and saturations 1, 2 and 3. No external target values or empirical observations were loaded. The independent outcome was preclassified as: (i) replicated minimal generator if full-model branching occurred, initial-trait removal eliminated it, and at least one other single ablation retained it; (ii) inconclusive if the full independent block itself did not branch; or (iii) contradicted if initial-trait removal retained within-run branching.

The first workflow attempt failed before scientific execution because of an import-path error. Only that software error was corrected; the frozen seed and design remained unchanged. The first successfully executed scientific result was retained, and further seed searching was closed.

## 2.6 Network-context buffering

Network-context buffering was tested with local support OFF versus ON while autonomous assurance was disabled and the underlying opportunity networks were held matched. Analyses of sign rescue were restricted to cases in which global opportunity declined and the support-OFF reproductive response was negative. We distinguished magnitude rescue (a less negative response), sign rescue (crossing to zero or positive) and worsening (a more negative response). Because both rescue and worsening are possible, the experiment tests buffering **capacity**, not an assumption of monotonic protection.

## 2.7 Autonomous assurance

The assurance analysis compared matched simulations with the assurance route enabled versus disabled while preserving identical upstream effective-service changes. We distinguished magnitude attenuation from strong sign rescue. Stability was tested in an independent frozen block and a broadened local-support envelope. A non-replicating sign rescue in an earlier stochastic block was retained as a historical result but not promoted to the stable mechanism claim.

## 2.8 State separability

We quantified observation-to-mechanism diagnostics from the frozen intervention frequencies rather than training a classifier on external island labels. Mixed-sign branching was evaluated as a diagnostic of initial trait-position heterogeneity; same-direction response was evaluated as a candidate diagnostic of trait uniformity. Network-context sign rescue was compared against the implemented assurance route, and assurance-associated magnitude attenuation was compared against attenuation generated by network context. We report sensitivity, false-positive rate and specificity within the declared model family.

## 2.9 External island-system challenge

A global literature screen retained 54 geographic/system units as the screening denominator. Thirteen systems satisfied the strict external state-challenge contract. Their source-supported state classes were frozen before comparison with the model-state vocabulary. The strict set comprised three branching systems, six same-direction propagation systems, two buffering/alternative systems, one reproductive-axis-decoupling constraint and one retained falsification.

The 11 generative cases were evaluated only for qualitative state coverage or sign-class compatibility. We did not compute a fitted effect size, optimize model parameters to external targets or treat qualitative compatibility as empirical mechanism identification. System-specific source details and citations remain in the source-audit and global-screen Supplementary layer.

## 2.10 Falsification rules

Five falsification rules were frozen (`data/results/simulation_manuscript_falsification_table_frozen.json`). The minimal branch-generator claim would fail if initial-trait removal retained mixed-sign branching. A universal network-buffer claim is rejected by any matched worsening. A robust assurance sign-buffer claim requires replicated sign rescue. The failed Dominica signed-position projection is retained without remapping. Any future predeclared external generative target outside every frozen state class must first be recorded as a state-space miss before model extension.

---

# 3. Results

## 3.1 One architecture generated several response-state classes

The frozen model produced branching, same-direction and buffering states without system-specific retuning. In the original v12 residual block, mixed-sign responses occurred in 5 of 12 matched runs (0.4167), leaving 7 of 12 runs (0.5833) with a single response direction despite heterogeneous starting trait positions. Same-direction response is therefore a genuine output of the heterogeneous model rather than evidence of lineage uniformity.

Network context produced strong buffering in a subset of eligible declines. In an independently seeded block, support ON moved 16 of 96 negative support-OFF reproductive contrasts to the zero boundary or above. It attenuated 85 of 96 declines, but worsened 11 of 96. By contrast, autonomous assurance attenuated 207 of 216 declines while producing 0 of 216 strong sign rescues; a broadened 525-contrast envelope also contained no strong assurance sign rescue.

## 3.2 Pre-existing functional position was the replicated minimal branch generator

In the original v12 residual block, the full model had a mixed-sign run fraction of 0.4167 and mean within-run branching balance of 0.2569. Removing initial trait-position heterogeneity reduced both quantities to zero. Removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity individually did not collapse branching.

The same state boundary occurred in the prespecified independent block. Full-model mixed-sign frequency was again 0.4167 and mean branching balance was 0.2917. Initial-trait removal again reduced mixed-sign frequency and branching balance to zero, changing 44 paired lineage signs. Trait-adjustment heterogeneity OFF retained mixed-sign frequency 0.4167 and balance 0.2847; assurance-ceiling heterogeneity OFF retained 0.4167 and 0.2917, respectively. Across two independently seeded blocks, initial functional-position heterogeneity was therefore the only tested residual factor whose removal eliminated within-run response-sign branching.

## 3.3 Downstream mechanisms altered branch identity differently

In the v11 drop-one factorial, removing local support changed 105 of 288 paired lineage response signs, compared with 13 of 288 for partner effectiveness, one for assurance responsiveness and none for dependency heterogeneity. Yet two-sided branching persisted with all four tested downstream modifiers OFF. This separates the origin of branching from later branch allocation: pre-existing lineage state generates the possibility of opposite responses, whereas local context substantially changes which lineage occupies which branch.

Network context was not a monotonic buffer. Its independent sign-rescue frequency was 16/96, but its worsening frequency was 11/96. The appropriate model-level interpretation is therefore a bidirectional branch allocator with buffering capacity. Assurance occupied a narrower response regime: attenuation remained frequent at all three saturation values while strong sign rescue remained absent.

## 3.4 State observations had asymmetric diagnostic value

Mixed-sign branching was a high-specificity but low-sensitivity diagnostic of heterogeneous initial lineage position. Within the original frozen gate, specificity was 1.0 and sensitivity was 0.4167. Thus the presence of branching strongly discriminated the tested heterogeneous versus uniform intervention, but its absence did not imply uniform starting states.

Same-direction response was weak for inverse inference. Although all initial-trait-uniform runs were non-mixed, 0.5833 of heterogeneity-ON runs were also non-mixed, yielding a false-positive rate of 0.5833 and specificity of only 0.4167 if same-direction response is used to infer trait uniformity.

Network-context sign rescue was similarly specific but insensitive relative to the tested assurance route: specificity was 1.0 and sensitivity 0.1667. Magnitude attenuation showed the opposite problem. Assurance attenuation sensitivity was 0.9583, but network context also attenuated 0.8854 of eligible declines, leaving specificity against network context at only 0.1146. Attenuation alone is therefore nearly non-identifying between the two implemented routes.

## 3.5 External island systems challenged the state vocabulary without fitting it

The global screen contained 54 geographic/system units, of which 13 entered the strict external challenge. Eleven were generative cases: three branching, six same-direction propagation and two buffering/alternative systems. All 11 were qualitatively covered or sign-compatible with an already-frozen state class.

The other two strict systems were retained precisely because they did not support a simple success count. Puerto Rico–Mona *Guaiacum* was treated as a reproductive-axis-decoupling constraint rather than being relabelled as whole-reproduction buffering. Dominica *Heliconia* remained a failed frozen signed-position projection and was not retuned after failure.

The external series therefore broadens the relevance of the model state space but does not establish that the same empirical mechanism operates in every system.

---

# 4. Discussion

## 4.1 A state-dependent alternative to a single island response syndrome

The central result is that a common functional perturbation does not require a common downstream sign. Within the declared ABM, opposite reproductive responses arise when lineages encounter the same pollinator-environment shift from different positions in functional trait space. This boundary survived an independently seeded replication: branching remained in the full and other single-ablation models but disappeared when initial lineage-position heterogeneity was removed. The relevant form of heterogeneity is therefore not merely noise around a universal island response. It is part of the mechanism by which a common perturbation becomes lineage-specific.

This framing complements rather than contradicts evidence for island reproductive syndromes. Global comparative studies show that self-compatibility and other traits affect the probability of island colonization (Grossenbacher et al. 2017; Zell et al. 2025), and syntheses identify repeated island-associated shifts in reproductive traits and pollination systems (Whittaker et al. 2023). Those patterns describe an important **filtering layer**: lineages with some reproductive strategies are more likely to arrive, establish or persist. Our model addresses a different layer: conditional on lineages being present, how does an altered functional pollination environment propagate through heterogeneous plants? A colonization filter can bias the set of states entering an island without eliminating state-dependent response after establishment.

This distinction also helps reconcile apparently conflicting empirical narratives. An island flora can be enriched for self-compatible species at the macroevolutionary scale while particular island–mainland lineage comparisons show unchanged assurance, stronger pollen limitation, altered morphology, interaction rewiring or divergent reproductive effects. Reviews of Mediterranean island plants already emphasize that the empirical literature is heterogeneous in both taxonomic coverage and reproductive outcomes (Traveset & Navarro 2018). The present model suggests that such heterogeneity should not automatically be treated as failure to discover the correct universal syndrome.

## 4.2 Network context is a branch allocator with buffering capacity, not a shield

The second major result concerns ecological-network context. Pollination networks can reorganize after partner loss, invasion or abundance shifts, and network resilience theory emphasizes rewiring, heterogeneity and redundancy as potential mechanisms that preserve ecological function (Bascompte & Scheffer 2023). Functional-interaction approaches likewise argue that realized interactions are only a subset of the partners a species may be able to use, so community reorganization may maintain function even when interaction identity changes (Marjakangas et al. 2025).

Our synthetic result is consistent with that general perspective but imposes an important qualification. Increasing local support did not monotonically improve outcomes. It rescued reproductive sign in 16 of 96 eligible declines but worsened 11 of 96. This is exactly why we describe network context as a **bidirectional branch allocator with buffering capacity**. The same mechanism family that compensates one lineage can redirect another into a poorer local interaction configuration. Resilience should therefore not be inferred from the presence of network rewiring alone; the functional consequences of the reallocated partners matter.

This also separates two meanings of “buffering.” Strong buffering changes the qualitative response state by preventing a negative upstream perturbation from reaching a negative reproductive outcome. Weak buffering merely reduces the magnitude of loss. The model shows that these are not interchangeable observables. Network context can occasionally cross the sign boundary, whereas autonomous assurance reliably reduces decline magnitude without robustly crossing that boundary. Lumping both patterns into a single category of “resilience” would erase the mechanism contrast that the ablations reveal.

## 4.3 The inverse problem is the main methodological result

A model that can reproduce multiple states is flexible; flexibility becomes informative only when we ask which observations exclude alternatives. This is where the state-separability analysis changes the interpretation of the ABM. Mixed-sign branching is highly specific among the tested residual interventions, but it is insensitive: more than half of heterogeneous full-model runs remain same-direction. Conversely, same-direction response is therefore poor evidence for homogeneous starting states. The model can contain the necessary generator without expressing its most diagnostic state in every stochastic realization.

The same asymmetry appears for buffering. Strong sign rescue is highly specific against the tested assurance route but occurs in only a minority of eligible network-context cases. Magnitude attenuation is common under assurance but almost equally common under network context. The most frequently observed pattern is therefore not necessarily the most mechanistically informative.

This result connects naturally to pattern-oriented modelling. Pattern-oriented approaches seek multiple independent patterns that constrain bottom-up models rather than asking a single flexible model to match one target (Grimm et al. 2005; Grimm & Railsback 2012). Our contribution is to make the inverse side explicit at the response-state level. A frozen model may pass a **forward coverage test**—it can generate the state—while still fail an **inverse identification test**—the state can be generated by more than one mechanism. In this sense, equifinality is not merely a caveat to append to the Discussion. It is an estimable property of the model’s intervention structure.

This distinction is especially important when model results are compared with qualitative natural-history states. A same-direction empirical response is compatible with the model but has little power to identify the lineages’ initial functional distribution. A buffered empirical response demonstrates that the frozen state space is sufficiently broad, but it does not identify local network support as the biological cause. Mechanism claims require either more diagnostic observations or direct empirical mapping of the mechanism itself.

## 4.4 What the external island series does—and does not—validate

The global island screen was intentionally separated from model calibration. The 13 strict systems contain multiple independent forms of perturbation, including pollinator loss, partner replacement, invasive-ant disruption, honeybee-associated network change and hurricane-associated loss. The 11 generative systems span branching, same-direction propagation and buffering/alternative response states, all of which occur within the previously frozen synthetic vocabulary. This broadens the ecological relevance of the state atlas beyond the Izu calibration context.

However, the external challenge is not a numerical posterior-predictive test, and it should not be described as 13 independent validations of a single mechanism. The six same-direction cases are particularly instructive: same-direction response has low mechanism specificity in the ABM, so repeated empirical observation of that state expands state-space relevance without telling us whether the same causal route operates across systems. The two buffering/alternative cases similarly show that strong-response preservation is an empirically meaningful target class, while the model itself warns that attenuation and rescue can arise through different routes.

The two non-generative strict cases prevent the comparison from becoming a success-only catalogue. Guaiacum is retained as an axis-decoupling constraint because different components of reproduction do not justify a single whole-system buffering label. The Dominica signed-position projection remains a direct failure. Retaining that failure matters methodologically: if the external comparison were allowed to redefine signed position after inspecting the outcome, the model would lose falsifiability.

Macroecological colonization studies form a complementary outer test rather than another replicate of the same process. The strong association between self-compatibility and island occurrence reported by Grossenbacher et al. (2017), and the broader trait-by-arrival framework of Zell et al. (2025), address which lineages reach and establish on islands. Our 13-system state challenge addresses how functional pollination change propagates after lineages are present. Bringing those layers together could eventually yield a hierarchical island theory in which colonization filters shape the distribution of initial states and local ecological dynamics determine how those states respond to subsequent interaction change.

## 4.5 Limits and claim boundaries

Several limitations are central to the interpretation rather than incidental technical caveats. First, the lineage matching trait is standardized and abstract. The model identifies the importance of **relative initial functional position**, not the identity of the empirical trait that carries that position in a particular species. Mapping it onto corolla morphology, colour, nectar guides, timing or a multivariate trait axis remains a separate empirical task.

Second, the external island challenge is qualitative. State-class compatibility is weaker than estimating a shared quantitative effect distribution across systems. We deliberately avoid cross-system effect-size pooling because the empirical axes, units and designs are not commensurate across all 13 strict systems. The analysis therefore supports state-space validity, not a universal coefficient for island pollination response.

Third, the model tests a declared mechanism family rather than all biologically plausible mechanisms. Other downstream filters—resource limitation, demography, mating-system architecture, phenology or unmodelled interaction traits—could produce similar natural patterns. Our response to this limitation is not to add generic hidden parameters after every mismatch. Instead, new mechanisms should be opened as separately frozen questions when a predeclared state-space miss or independent empirical evidence requires them.

Fourth, complete empirical mapping from network context to rate-weighted effective service remains unavailable in the current retrospective portfolio. A separate five-gate audit found zero of 12 candidate systems with all source-native components needed for `Σ V_k E_k` mapping on the same context hierarchy. This prevents us from claiming that the synthetic local-support parameter is empirically identified in a particular island system. It does **not** invalidate the model-internal state and separability results, and it is not a prerequisite for the primary simulation claim.

Finally, stochastic replication should not become another route to post-hoc optimization. The central branch-generator result was replicated once using a seed and decision rule frozen before execution, and further seed search was explicitly closed. This protects the distinction between demonstrating robustness and searching until a favorable frequency appears.

## 4.6 Implications and next tests

The most informative future empirical test is not simply to document another island with reduced visitation or another lineage with high autonomous reproduction. The model predicts that evidence value depends on the observed state. Mixed-sign responses among lineages experiencing a matched functional perturbation are more discriminating for heterogeneous initial position than same-direction responses. Strong sign rescue following a documented service decline is more discriminating among the tested buffering routes than a modest reduction in loss. Future field designs can therefore be chosen to target **diagnostic states**, not merely convenient response variables.

A second extension is to connect the filtering and response layers. If colonization filters enrich islands for particular breeding systems or generalized interaction capacities, then the distribution of starting states entering the post-colonization ABM should itself be non-random. That would turn the present model from a conditional response framework into a hierarchical colonization-to-response framework. Such an extension should be treated as a new model question, because it changes the generative problem rather than refining the current fit.

A third extension is comparative transfer beyond islands. Habitat fragmentation, urbanization and other forms of biotic simplification can also reduce partner diversity while creating opportunities for interaction rewiring. The current mechanism logic therefore makes a testable cross-domain prediction: different fragmentation processes may converge on similar functional-response states even when their proximate causes differ. The relevant comparison is not “island versus city” but whether different systems occupy the same state-dependent functional-fragmentation regime.

---

# 5. Conclusion

A single island perturbation does not imply a single island response. In the frozen ABM, lineages exposed to the same pollinator-functional shift can move in opposite reproductive directions because they begin from different functional positions. That branching boundary replicated independently. Local network context then acts as a strong but bidirectional branch allocator, while autonomous assurance mainly attenuates decline magnitude. These mechanisms generate overlapping observable states, so forward model compatibility and inverse causal identification must be separated.

The global island challenge shows that branching, same-direction propagation and buffering are not peculiar outputs of one focal system, while the retained Guaiacum constraint and Dominica failure prevent the comparison from collapsing into a universal success claim. The resulting contribution is therefore neither a universal island syndrome nor a claim that one ABM mechanism explains all islands. It is a **frozen state-space framework** in which recurrent ecological outcomes, mechanism interventions, diagnostic asymmetry and falsification are analyzed together.

---

# References used for conceptual positioning

Bascompte, J. & Scheffer, M. (2023). The Resilience of Plant–Pollinator Networks. *Annual Review of Entomology*, 68, 363–380. https://doi.org/10.1146/annurev-ento-120120-102424

Grimm, V., Revilla, E., Berger, U., Jeltsch, F., Mooij, W.M., Railsback, S.F., Thulke, H.-H., Weiner, J., Wiegand, T. & DeAngelis, D.L. (2005). Pattern-oriented modeling of agent-based complex systems: lessons from ecology. *Science*, 310, 987–991. https://doi.org/10.1126/science.1116681

Grimm, V. & Railsback, S.F. (2012). Pattern-oriented modelling: a ‘multi-scope’ for predictive systems ecology. *Philosophical Transactions of the Royal Society B*, 367, 298–310. https://doi.org/10.1098/rstb.2011.0180

Grossenbacher, D.L., Brandvain, Y., Auld, J.R., Burd, M., Cheptou, P.-O., Conner, J.K., Grant, A.G., Hovick, S.M., Pannell, J.R., Pauw, A., Petanidou, T., Randle, A.M., Rubio de Casas, R., Vamosi, J., Winn, A., Igic, B., Busch, J.W., Kalisz, S. & Goldberg, E.E. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. https://doi.org/10.1111/nph.14534

Marjakangas, E.-L., Dalsgaard, B. & Ordonez, A. (2025). Fundamental Interaction Niches: Towards a Functional Understanding of Ecological Networks' Resilience. *Ecology Letters*, 28, e70146. https://doi.org/10.1111/ele.70146

Traveset, A. & Navarro, L. (2018). Plant reproductive ecology and evolution in the Mediterranean islands: state of the art. *Plant Biology*, 20(Suppl. 1), 63–77. https://doi.org/10.1111/plb.12636

Whittaker, R.J., Fernández-Palacios, J.M. & Matthews, T.J. (2023). Island evolutionary syndromes in—and involving—plants. In *Island Biogeography: Geo-environmental Dynamics, Ecology, Evolution, Human Impact, and Conservation* (3rd ed.), pp. 283–308. Oxford University Press. https://doi.org/10.1093/oso/9780198868569.003.0011

Zell, A.N., Miranda, C.H., Grady, E.L., Grossenbacher, D.L. & Igić, B. (2025). Island colonization in flowering plants is determined by the interplay of breeding system, lifespan, floral symmetry, and arrival opportunity. *New Phytologist*, 245, 420–432. https://doi.org/10.1111/nph.20234

---

## Draft-completion notes

- Methods and Results in this draft must remain subordinate to the frozen canonical files; editorial shortening must not change numerical values or claim boundaries.
- System-specific references for the 13 strict island cases should be inserted from the source-audit registry into the final Supplementary state matrix rather than reconstructed from memory.
- No new simulation is required to complete the current manuscript draft.
- The next editorial decision is journal positioning and how strongly to foreground the **diagnostic asymmetry / equifinality** contribution versus the island-pollination application.
