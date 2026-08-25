# One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification

## Abstract

1. Island floras show recurrent reproductive syndromes, yet established plant lineages do not respond uniformly when pollinator function is simplified or reorganized. We asked whether one island-like perturbation must produce one post-establishment trajectory, or whether divergent outcomes can arise from a common ecological architecture.

2. We used a frozen agent-based model in which plant lineages experienced a common change in pollinator functional opportunity while differing in pre-existing functional position and downstream interaction or reproductive context. We decomposed the model by factorial and residual ablation, independently replicated the strongest branch-generator boundary under a predeclared stochastic design, and challenged the frozen response-state vocabulary against island plant–pollinator systems retained from a global screen of 54 geographic/system units. External outcomes were not used to tune parameters, choose seeds, add mechanisms or redefine states.

3. Mixed-sign branching occurred in 0.4167 of matched runs in both original and independent blocks, but disappeared when initial functional-position heterogeneity was removed. Local support changed 105/288 paired lineage response signs. Network context rescued reproductive sign in 16/96 eligible declines and attenuated 85/96, but worsened 11/96. Autonomous assurance attenuated 207/216 declines while producing no sign rescues in the independent block and none across a broadened 525-contrast envelope.

4. Thirteen strict external systems comprised three branching, six same-direction propagation, two buffering/alternative systems, one reproductive-axis-decoupling constraint and one retained falsification. All 11 generative challenges were covered or sign-compatible with response states generated before the final external challenge.

5. **Synthesis.** Island-associated biotic simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal plant trajectory. Aggregate island syndromes can coexist with lineage-level branching because colonization and persistence shape which states arrive, whereas functional starting state, local interaction context and reproductive filters shape how established lineages respond.

**Keywords:** agent-based model; ecological networks; functional traits; island biogeography; plant–pollinator interactions; reproductive assurance; resilience; response heterogeneity

## Data and code for peer review

All primary numerical claims derive from frozen simulation outputs and source-audited external-state assignments. For double-anonymous peer review, the code, frozen result summaries, figure-generation inputs, source-audit matrices and exact-regeneration tests will be supplied through an anonymized review archive or suitable private peer-review repository. No new unpublished field dataset is required for the primary claims. Public author-identifying repository information is withheld from the anonymous review manuscript and will be provided on the title page and in the final Data Availability statement.

# Introduction

Islands are natural experiments in colonization, ecological simplification and the reorganization of biotic interactions. Plant reproductive systems are especially sensitive to these changes because successful reproduction depends not only on abiotic conditions but also on mate availability and the abundance, identity and functional compatibility of pollinators. Comparative studies have consequently identified recurrent island-associated reproductive patterns, including over-representation of self-compatibility and interactions between breeding system, lifespan, floral traits and arrival opportunity (Grossenbacher et al., 2017; Zell et al., 2025). Broader syntheses likewise identify repeated shifts in floral traits, pollination systems and plant–animal interactions as candidate components of island evolutionary syndromes (Traveset & Navarro, 2018; Whittaker et al., 2023).

The term **island syndrome**, however, spans processes operating at different stages. Recent functional and regional syntheses distinguish insular assembly rules—biased dispersal, colonization and establishment—from evolutionary changes that occur after colonization (Schrader et al., 2021; Whittaker et al., 2023). This distinction is not merely semantic. Ciarle & Burns (2025) reviewed 21 globally proposed components of the plant island syndrome in New Zealand's outlying islands: 16 had been investigated regionally, but only four were considered well supported, nine remained tentative and limited evidence suggested that three were not syndrome components in that region. Thus, recurrent island-associated patterns are real, but their consistency and causal origin differ among traits.

The strongest reproductive example is Baker's law. Its modern scope is an **assembly prediction about the capacity for uniparental reproduction during colonization**, rather than a prediction of uniformly high realized selfing after establishment (Pannell et al., 2015; Pannell, 2015). Global comparative analyses support that filtering layer. Grossenbacher et al. (2017) found self-compatibility in 66% of island species versus 41% of mainland species across more than 1500 species in three flowering-plant families. Zell et al. (2025), using 3222 species from 169 families, likewise found strong effects of breeding system and arrival opportunity, with lifespan and generalized pollination contributing conditionally. These assembly effects can therefore create a macroecological reproductive syndrome before any lineage-specific post-establishment evolution is considered.

Floral morphology provides a contrasting case. Hetherington-Rauth & Johnson (2020) analysed 136 phylogenetically independent Pacific island–mainland sister contrasts and found no universal reduction in island flower size; direction varied among archipelagos and families. More recent analysis of 129 colonization events across ten Southwest Pacific archipelagos found size-dependent island-rule evolution in animal-pollinated flowers but gigantism in wind-pollinated flowers (Ciarle et al., 2025). These studies shift the question from whether flowers move in one island direction to **which starting states and functional contexts determine the direction of change**.

A similar conditionality appears at the interaction-network level. Across 52 quantitative pollination networks, oceanic island networks were generally smaller and topologically simplified, with lower interaction diversity and greater plant niche overlap, but network properties did not change uniformly (Traveset et al., 2016). On Yongxing Island, plants were visited by more pollinator species than classical pollination syndromes predicted and measured floral traits explained only a minority of visitor preference (Wang et al., 2020). Most directly for the present study, Hiraiwa & Ushimaru (2017, 2024) showed in Japanese continental and oceanic island networks that loss of pollinator **functional diversity**, especially long-tongued pollinators, reduced functional niche partitioning, flower–pollinator trait matching and pollination success more clearly than pollinator species diversity itself.

Such aggregate regularities therefore combine at least three processes that need not generate the same prediction: **colonization/assembly filtering**, **in-situ evolutionary change after colonization**, and **post-establishment ecological response to reorganized interactions**. A flora can be enriched for self-compatible or generalized strategies because of assembly while established lineages still exhibit decline, compensation, trait-specific divergence or little response when pollinator function changes. The current study focuses explicitly on that third layer.

The post-establishment problem becomes especially important when interaction identity changes. Pollination function is not determined by the presence or absence of a nominal pollinator group alone. Species loss, partner replacement, changes in relative abundance and interaction rewiring can redistribute function among remaining partners. Network-resilience theory highlights rewiring and interaction heterogeneity as possible routes through which ecological function can persist after perturbation, while functional-interaction approaches emphasize the difference between realized partners and the larger trait space of potential partners (Bascompte & Scheffer, 2023; Marjakangas et al., 2025). These perspectives imply that the same decline in global pollinator opportunity can propagate strongly in one lineage, be redirected by partner context in another, and be attenuated downstream by reproductive assurance in a third.

This motivates a different island-ecology question from asking whether plants become more selfing, less specialized or morphologically simplified on average: **why does a common island-associated change in pollinator function produce different downstream responses among established plant lineages?** We considered three conditional layers within the post-establishment response itself. First, lineages occupy different positions in plant–pollinator functional space before the environment changes. Second, local interaction context determines how changed global opportunity is redistributed. Third, reproductive filters such as autonomous assurance change how service loss propagates into reproduction. The resulting ecological logic is summarized in Fig. 1.

Agent-based models provide an experimental system for separating these layers because candidate mechanisms can be removed while holding the remainder of the architecture fixed. To avoid explaining each external system by post-hoc adjustment, the model architecture, stochastic envelopes, response-state definitions and falsification rules were frozen before the final external challenge. State-separability diagnostics were retained only as an inference guard: a simulated state can be ecologically compatible with a real system without uniquely identifying that system's causal mechanism.

We tested five linked hypotheses. **H1, the universal post-establishment response hypothesis**, predicts that a common island-like pollinator-functional perturbation pushes established lineages in one common downstream direction. **H2, the state-dependent branching hypothesis**, predicts that pre-existing functional-position heterogeneity is required for within-environment response branching. **H3, the context-dependent propagation hypothesis**, predicts that local interaction context reallocates branch identity and can either rescue or worsen individual lineage responses. **H4, the autonomous-assurance buffering hypothesis**, predicts that reproductive assurance reduces the downstream effect of service decline, with the stronger subprediction that it can reverse response sign. **H5, the cross-island recurrence hypothesis**, predicts that branching, same-direction propagation and buffering or alternative response states recur across independent island systems without system-specific retuning.

Together, these hypotheses distinguish an aggregate island syndrome from a universal within-lineage trajectory. The study does not test whether island syndromes exist. It tests whether one ecological perturbation must produce one post-establishment response and, if not, which conditional mechanisms generate the branching and propagation of outcomes.

# Materials and Methods

## Study design and frozen inference boundary

The study combined controlled simulation experiments with qualitative external island-system challenges. Primary numerical results came from frozen model outputs and matched ablations. External island outcomes were not used to choose model parameters, random seeds, state definitions or mechanisms. New field data were not an admission requirement for the primary simulation claim.

The model represented multiple plant lineages exposed to matched mainland-like and island-like pollinator environments. Pollination opportunity emerged from interaction between plant and pollinator functional traits under a fixed visit-budget formulation. Plant lineages could differ in initial standardized matching-trait position and, depending on the experimental layer, trait adjustment, local support, pollinator dependency, assurance ceiling, assurance responsiveness and partner effectiveness.

The standardized plant matching trait is an abstract relative functional coordinate. It is not assigned post hoc to corolla length, colour, nectar guides or any single empirical trait. Thus the model tests the ecological role of relative starting position without claiming that the same measured floral axis carries that position in every real system.

The model-development and challenge sequence was frozen before the final external comparison. External systems were used as state-level ecological challenges rather than parameter-fitting targets. The full experimental inventory, state definitions and stop rules are provided in Appendix S1–S3 of the Supporting Information.

## Experimental envelope and downstream factorial

The v11 downstream factorial toggled four mechanism families: local support, dependency heterogeneity, assurance responsiveness and partner effectiveness. The frozen design contained 16 factorial cells evaluated at saturation values 1, 2 and 3, with four replicates per saturation, 24 lineages per run and 288 lineage contrasts per cell. No empirical inputs or Izu target frequencies were loaded into this analysis.

For each factor configuration we recorded pooled positive, negative and equal lineage responses, mixed-sign run frequency, branching balance and paired lineage sign changes relative to matched reference states. The factorial was used to determine whether downstream modifiers were required to **generate** two-sided branching or instead altered branch identity after branching was already possible.

## H1: common perturbation versus universal response

Within-run mixed-sign branching was defined as the occurrence of both positive and negative lineage reproductive responses to the same matched mainland-like to island-like environmental contrast. A universal post-establishment response predicts that lineages within a matched run respond in the same direction. The frozen state atlas records branching, same-direction and buffering states generated without island-specific retuning (Table 1; Fig. 1).

## H2: residual ablation of the branch generator

Persistence of mixed-sign branching when all four v11 downstream factors were fixed off located the branch generator upstream of those modifiers. The v12 residual experiment therefore fixed those four modifiers off and manipulated three remaining lineage-level sources: initial trait-position heterogeneity, trait-adjustment heterogeneity and assurance-ceiling heterogeneity.

The v12 design contained eight cells evaluated at saturation values 1, 2 and 3, four replicates per saturation, 24 lineages per run and 288 lineage contrasts per cell, again without empirical inputs. A residual factor was treated as necessary within the declared model when removing it eliminated mixed-sign runs and reduced mean within-run branching balance to zero while other single-factor removals retained branching.

The strongest boundary was tested once in an independent frozen block using seed 90260825, four replicates per saturation, 24 lineages, 120 steps and saturation values 1, 2 and 3. The decision rule and stop rule were specified before execution. The result was classified as `replicated_minimal_generator` only if the independent full residual block contained branching, initial functional-position heterogeneity OFF eliminated both branching and within-run branching balance, and at least one other single residual ablation retained branching. The first workflow attempt failed before scientific execution because of an import-path error; only that path was repaired, and the first successfully executed scientific result was retained. No further seed search was performed.

## H3: local interaction context and branch allocation

Local network context was evaluated by comparing local support off versus on under matched opportunity networks while autonomous assurance was disabled. Strong-rescue analyses were restricted to lineages for which global opportunity declined and support-off reproduction was negative. A magnitude attenuation made an eligible decline less negative; a sign rescue moved the response to zero or above; and worsening made it more negative. Because rescue and worsening were both permitted outcomes, this experiment tested context-dependent branch allocation and buffering capacity rather than assuming monotonic protection.

## H4: autonomous assurance

Autonomous assurance was evaluated in matched simulations with the assurance route enabled versus disabled while upstream effective-service changes were identical. We distinguished magnitude attenuation from strong sign rescue. Stability was tested in an independent frozen block and a broadened local-support envelope. A sign rescue seen in an earlier stochastic block was retained historically but was not promoted unless it replicated.

## H5: external island-system challenge

A global literature screen retained 54 geographic/system units as the screening denominator. Thirteen systems met a strict state-challenge contract based on source-locked evidence. The strict set contained three branching systems, six same-direction propagation systems, two buffering or alternative systems, one reproductive-axis-decoupling constraint and one retained falsification. These are **strict challenge systems**, not a random sample from which prevalence can be estimated.

The branching systems were the Izu multi-taxon Hiraiwa–Ushimaru system, Caribbean Gesneriaceae and the Canary Islands Teide honeybee-network experiment (Hiraiwa & Ushimaru, 2017, 2024; Martén-Rodríguez et al., 2010, 2015; Valido et al., 2019). Same-direction systems were Ogasawara *Psychotria homalosperma*, New Zealand *Rhabdothamnus solandri*, the Guam–Saipan bird-loss natural experiment, Seychelles invasive-ant disruption, Mauritius *Roussea simplex* invasive-ant disruption and Bahamas *Pavonia bahamensis* after hurricane-associated pollination loss (Watanabe et al., 2018; Anderson et al., 2011; Mortensen et al., 2008; Costa et al., 2023; Hansen & Müller, 2009; Rathcke, 2000). Buffering or alternative systems were Hawaiian lobelioids following bird extinctions and California Channel Islands *Nicotiana glauca* (Case et al., 2026a,b; Schueller, 2004, 2007). Puerto Rico–Mona *Guaiacum sanctum* was retained as reproductive-axis decoupling (Fumero-Cabán et al., 2022). Dominica *Heliconia* was retained as a failed signed-position projection rather than retuned after failure (Martén-Rodríguez et al., 2011; Temeles et al., 2013).

The external comparison was qualitative at the state level. It tested whether the already-frozen response vocabulary encompassed recurrent ecological outcomes without parameter fitting. It did not treat 13 systems as independent demonstrations of one causal mechanism. Full source-level assignments and claim boundaries are given in Table 2 and Table S3.

## Supporting inference diagnostics and protected falsification

After the ecological mechanism tests were frozen, state-separability diagnostics quantified whether response states were unique to tested mechanism contrasts. These diagnostics are supporting rather than primary results. They prevent same-direction response from being interpreted as proof of homogeneous starting states and magnitude attenuation from being interpreted as unique evidence for autonomous assurance.

The falsification contract was also explicit. The branch-generator claim would fail if branching survived initial functional-position heterogeneity OFF; a universal network-buffer claim is rejected by matched worsening; robust assurance sign buffering requires replicated sign rescue; the Dominica signed-position mapping remains failed; and any future predeclared external state outside every frozen response class must be logged as a state-space miss before model extension (Table 3; Appendix S9).

## Reproducibility and figure generation

All headline results are stored in frozen JSON artifacts. Main figure inputs are exported deterministically from those artifacts. Fig. 1 summarizes the ecological architecture; Fig. 2 shows the original and independent branch-generator boundary; Fig. 3 separates network-context branch allocation from assurance attenuation; and Fig. 4 summarizes the strict external island challenge. State-separability diagnostics are reported only in Fig. S1 and Table S2. The complete reproducibility map is listed in Appendix S10.

# Results

## H1: one island-like perturbation did not force one plant response

The frozen model generated multiple downstream response classes under one architecture (Table 1; Fig. 1). In the original residual block, mixed-sign branching occurred in 5 of 12 matched runs, giving a mixed-sign run fraction of 0.4167; the remaining 7 of 12 runs were same-direction despite heterogeneous starting states. The independent robustness block reproduced the same full-model mixed-sign frequency of 0.4167. H1 was therefore rejected: a common island-like perturbation does not imply a universal post-establishment response direction.

## H2: pre-existing functional position was the replicated minimal branch generator

Two-sided branching persisted when local support, dependency heterogeneity, assurance responsiveness and partner effectiveness were all fixed off. These downstream mechanisms were not required to generate opposite response signs.

In the residual ablation, the full model had mixed-sign frequency 0.4167 and mean within-run branching balance 0.2569. Removing initial trait-position heterogeneity reduced both to zero and changed 37 paired lineage signs. Removing trait-adjustment heterogeneity retained mixed-sign frequency 0.4167 and the same branching balance, with only two paired sign changes. Removing assurance-ceiling heterogeneity likewise retained mixed-sign frequency 0.4167 and produced no paired sign changes.

The independent block reproduced the same boundary (Fig. 2; Table S1). Full-model mixed-sign frequency was 0.4167 with mean within-run balance 0.2917. Removing initial functional-position heterogeneity again reduced both quantities to zero and changed 44 paired lineage signs, whereas removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity retained mixed-sign frequency 0.4167. Across two independently seeded frozen blocks, pre-existing lineage functional position was the only tested residual factor whose removal eliminated within-run response-sign branching. H2 was supported within the declared model.

## H3 and H4: local context reallocated branches, whereas assurance mainly attenuated magnitude

Although local support was not the origin of branching, it strongly changed branch identity. Removing local support changed 105 of 288 paired lineage response signs, compared with 13 of 288 for partner effectiveness, one for assurance responsiveness and none for dependency heterogeneity (Fig. 3a).

In the independent network-context experiment, among 96 eligible negative support-off reproductive contrasts, support on attenuated 85, crossed the sign boundary in 16 and worsened 11 (Fig. 3b). H3 was therefore supported in a bidirectional form: local interaction context reallocates response branches and has buffering capacity, but can also amplify decline.

Autonomous assurance occupied a different regime. Among 216 lineages with upstream service decline, assurance reduced the magnitude of reproductive decline in 207 but produced no sign rescues. At saturation values 1, 2 and 3, attenuation occurred in 71/75, 73/76 and 63/65 declines, respectively, while sign rescue remained zero. A broadened support envelope likewise produced zero sign rescues among 525 eligible declines (Fig. 3b,c; Appendix S6). H4 was therefore partially supported: assurance robustly attenuated decline magnitude, but robust qualitative sign reversal was not supported.

## H5: response-state diversity recurred across island systems

The 54-unit global screen yielded 13 strict external systems. Eleven were generative challenges: three branching, six same-direction propagation and two buffering or alternative cases. All 11 were covered or sign-compatible with response classes already present in the frozen model (Fig. 4; Table 2; Table S3).

The branching systems provided examples in which shared or comparable island interaction change coexisted with divergent downstream plant responses. The propagation systems included bird functional loss, invasive-ant disruption, pollinator-access asymmetry and hurricane-associated pollination loss. Hawaiian lobelioids and Channel Islands *Nicotiana* provided buffering or alternative-response boundaries.

Two systems were intentionally not counted as generative successes. Puerto Rico–Mona *Guaiacum* retained a reproductive-axis-decoupling state because a large visitor-context difference coexisted with similar self/outcross seed-set indices while other reproductive axes differed (Fumero-Cabán et al., 2022). Dominica *Heliconia* retained a failed signed-position projection: the predeclared negative direction was not recovered and the mapping was not retuned (Martén-Rodríguez et al., 2011; Temeles et al., 2013). These protected exceptions are summarized in Table 3.

H5 was therefore supported at the response-state level. Branching, propagation and buffering recur in independent island ecological contexts, but this recurrence does not establish one shared empirical mechanism.

## Supporting inference boundary

State-separability analysis reinforced the claim boundary rather than supplying the main biological result (Fig. S1; Table S2). Mixed-sign branching was highly specific but insensitive for initial functional-position heterogeneity within the tested intervention family: specificity was 1.0 but sensitivity 0.4167. Same-direction response was weak evidence for uniform starting states because 0.5833 of heterogeneity-on runs were also non-mixed. Network-context sign rescue was similarly specific but rare, whereas magnitude attenuation occurred commonly under both network context and assurance. These diagnostics are retained as Supplementary inference guards.

# Discussion

## Aggregate island syndromes can coexist with lineage-level branching

The central ecological result is best interpreted against a three-layer view of the plant island syndrome. First, selective arrival and establishment generate **assembly syndromes**, such as enrichment of self-compatible or otherwise reproductively assured colonists. Second, established lineages can undergo **in-situ evolutionary change**, which comparative studies show may depend on mainland starting state, pollination mode, clade and archipelago. Third, established communities experience **ongoing interaction reorganization** as pollinator functional composition and partner structure change. The current model addresses this third, post-establishment layer while conditioning explicitly on differences among lineage starting states.

This decomposition resolves an apparent contradiction in the island literature. Strong aggregate syndromes do not require all established lineages to follow one evolutionary trajectory. Baker's law can bias which reproductive states arrive; subsequent selection can modify mating systems; flower-size evolution can change direction with starting size and pollination mode; and interaction networks can become simplified while retaining compensatory or specialist routes (Pannell et al., 2015; Hetherington-Rauth & Johnson, 2020; Traveset et al., 2016; Ciarle et al., 2025). The present results therefore reject a universal **post-establishment trajectory**, not the existence of recurrent island syndromes.

This framing is also consistent with the evidence hierarchy in recent reviews. Ciarle & Burns (2025) found that only a minority of proposed syndrome components were strongly supported across New Zealand's outlying islands, whereas many remained tentative or unsupported. Whittaker et al. (2023) likewise emphasize that comparative support varies among plant syndrome components. The island syndrome is therefore better understood as a composite outcome of repeated filters and conditional responses than as one deterministic phenotype.

## Functional starting state determines branch potential

The strongest mechanistic result is the replicated loss of branching when initial functional-position heterogeneity is removed. Response direction is therefore relational within the model: the effect of a changed pollinator environment depends not only on the perturbation but also on where a lineage already lies relative to functional opportunity.

This interpretation gains independent conceptual support from recent island-floral studies. Hetherington-Rauth & Johnson (2020) rejected a universal directional flower-size syndrome across Pacific island–mainland contrasts, whereas Ciarle et al. (2025) recovered an island-rule pattern in animal-pollinated flowers in which direction depended on mainland starting size. Those studies do not validate the ABM's synthetic functional coordinate, but they independently show that **starting state can determine the direction of island-associated trait change**. The current model extends that conditionality from a comparative morphological pattern to a controlled response mechanism.

The standardized coordinate is intentionally more general than any single floral trait. Corolla length, colour, phenology or multivariate floral architecture may carry relevant functional position in particular systems, but the current model does not identify one universal empirical axis. This is an explicit scope boundary: the external comparison is used to challenge response states, not to assign a named real-world trait to the synthetic coordinate.

This distinction also clarifies why the external challenge is most informative at the level of response architecture. If a real island system branches, the model demonstrates that heterogeneous initial state is a sufficient and, within the tested residual family, necessary synthetic route to such branching. It does not follow that the same empirical state variable or causal route has been identified in that system.

## Local interaction context governs propagation, whereas assurance mainly dampens it

The model separates branch generation from branch allocation. Local support can change the sign of individual lineage responses even though branching remains possible without it. Network reorganization and rewiring are often discussed as sources of resilience because altered interactions can preserve function after partner loss (Bascompte & Scheffer, 2023; Marjakangas et al., 2025). The island-network literature, however, already cautions against reading simplification as monotonic loss. Oceanic networks can be smaller and have lower interaction diversity while retaining generalized or compensatory interaction routes, and floral traits alone may poorly predict realized ecological specialization (Traveset et al., 2016; Wang et al., 2020).

The current results add a mechanistic qualification: additional local support rescued 16/96 eligible negative responses but worsened 11/96. Network context is therefore better described as a **bidirectional branch allocator with buffering capacity** than as a universal shield. Hiraiwa & Ushimaru (2024) provide a close empirical analogue because reduced pollinator functional diversity, rather than species diversity alone, decreased functional trait matching and pollination success across island–mainland coastal networks. This comparison motivates the functional framing but does not identify the same causal mechanism in every external system.

Autonomous assurance operates downstream in a different way. It repeatedly reduced decline magnitude but did not robustly convert negative responses into maintained or positive reproduction. This separates weak buffering—smaller decline—from strong sign rescue. The ecological ordering that emerges is hierarchical: pre-existing state generates branch potential, local interaction structure redistributes propagation, and reproductive assurance dampens downstream magnitude.

This hierarchy provides a more precise interpretation of apparent resilience in island plant reproduction. Similar endpoint states can arise through different routes, so endpoint similarity alone should not be treated as evidence for a unique mechanism.

## Cross-island recurrence supports a response architecture, not a universal mechanism

The external island series extends the relevance of the model beyond one focal archipelago. The strict systems include pollinator functional-diversity change in the Izu region (Hiraiwa & Ushimaru, 2017, 2024), pollination-system transitions in Caribbean Gesneriaceae (Martén-Rodríguez et al., 2010, 2015), managed-honeybee network disruption in the Canary Islands (Valido et al., 2019), bird functional loss in New Zealand and the Marianas (Anderson et al., 2011; Mortensen et al., 2008), invasive-ant disruption in Seychelles and Mauritius (Costa et al., 2023; Hansen & Müller, 2009), hurricane-associated pollination loss in the Bahamas (Rathcke, 2000), and post-extinction or alternative reproductive states in Hawaiʻi and the California Channel Islands (Case et al., 2026a,b; Schueller, 2004, 2007).

The comparison is not a prevalence estimate: the 13 systems entered through a strict evidence gate rather than random sampling. Nor does state compatibility show that the synthetic initial-position mechanism operates in all systems. A same-direction natural experiment can occupy the model's state space even when the real proximate cause is bird extinction, invasive ants or another system-specific process.

The external challenge is therefore architectural. Independent systems repeatedly occupy branching, propagation and buffering/alternative states, while *Guaiacum* and Dominica protect the analysis from becoming a success-only catalogue. *Guaiacum* prevents multiple reproductive axes from being collapsed into one buffered/unbuffered label, and the Dominica result shows that a predeclared empirical mapping can fail without triggering post-hoc retuning.

The ecological implication is not that islands share one mechanism, but that they can share a **conditional response architecture**. Different proximate disturbances may enter the same broad functional problem—changed pollinator opportunity—and then diverge because established lineages differ in starting state, local interaction context and downstream reproductive filters.

## Inference boundary

Observable response states are not equally informative about their generating mechanism. Mixed-sign branching is informative when present but need not appear in every heterogeneous run; same-direction response therefore cannot be used to infer homogeneous lineages. Likewise, attenuation alone cannot distinguish network-context compensation from autonomous assurance because both routes can reduce magnitude.

This is the appropriate role of state separability in the current paper: it prevents the ecological synthesis from becoming stronger than the evidence. The external challenge establishes recurrence of response states, not one-to-one causal identification across islands. Questions that require direct empirical mechanism identification are outside the scope of this study and are not part of the submitted research programme.

# Conclusion

Island-associated pollinator simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal post-establishment plant trajectory. In the frozen ABM, pre-existing lineage functional position is the replicated minimal generator of within-environment response branching. Local interaction context reallocates branch identity and can rescue or worsen propagation, whereas autonomous assurance mainly attenuates reproductive decline magnitude.

Independent island systems repeatedly occupy the same broad response classes without system-specific retuning. Those recurrences support a state-dependent island-response architecture, while the retained *Guaiacum* constraint and Dominica failure prevent a universal-mechanism interpretation.

The island-ecology synthesis is therefore conditional rather than syndrome-only: **aggregate island syndromes can coexist with lineage-level branching because colonization and persistence determine which states arrive, in-situ evolution can be starting-state dependent, and functional starting state plus local ecological context determine how established lineages respond after pollinator environments change.**

# References

Anderson, S.H., Kelly, D., Ladley, J.J., Molloy, S. & Terry, J. (2011). Cascading effects of bird functional extinction reduce pollination and plant density. *Science*, 331, 1068–1071. https://doi.org/10.1126/science.1199092

Bascompte, J. & Scheffer, M. (2023). The resilience of plant–pollinator networks. *Annual Review of Entomology*, 68, 363–380. https://doi.org/10.1146/annurev-ento-120120-102424

Case, S.B., Hagemann, M.E., Drake, D.R., Postelli, K., Pender, R.J., Millikin, P.W. & Rico-Guevara, A. (2026a). Bird extinctions shift bill–flower trait matching in Hawaiian lobelioids. *Functional Ecology*, early view. https://doi.org/10.1111/1365-2435.70415

Case, S.B., Drake, D.R., Epperly, K., Steinbronn, C., Kanakaokai, K., Hagemann, M.E., Kingsley, N.H., Gregory, S.B., Mounce, H.L. & Rico-Guevara, A. (2026b). Mutualism and antagonism in a post-extinction Hawaiian bird–lobelioid pollination system. *Ecology and Evolution*, 16, e74123. https://doi.org/10.1002/ece3.74123

Ciarle, R. & Burns, K.C. (2025). The island syndrome in plants on New Zealand's outlying islands: a review. *New Zealand Journal of Botany*, 63, 2300–2324. https://doi.org/10.1080/0028825X.2024.2377418

Ciarle, R., Burns, K.C. & Mologni, F. (2025). Flower size evolution in the Southwest Pacific. *Annals of Botany*, 136, 287–296. https://doi.org/10.1093/aob/mcaf005

Costa, A., Heleno, R., Font Freide, E., Dufrene, Y., Huckle, E. & Kaiser-Bunbury, C.N. (2023). Impacts of invasive ants on pollination of native plants are similar in invaded and restored plant communities. *Global Ecology and Conservation*, 42, e02413. https://doi.org/10.1016/j.gecco.2023.e02413

Fumero-Cabán, J.J., Meléndez-Ackerman, E.J. & Rojas-Sandoval, J. (2022). Pollination ecology and breeding system of the tropical tree *Guaiacum sanctum* on two Caribbean islands with contrasting pollinator assemblages. *Journal of Pollination Ecology*, 32, 139–153. https://doi.org/10.26786/1920-7603(2022)669

Grossenbacher, D.L. et al. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. https://doi.org/10.1111/nph.14534

Hansen, D.M. & Müller, C.B. (2009). Invasive ants disrupt gecko pollination and seed dispersal of the endangered plant *Roussea simplex* in Mauritius. *Biotropica*, 41, 202–208. https://doi.org/10.1111/j.1744-7429.2008.00473.x

Hetherington-Rauth, M.C. & Johnson, M.T.J. (2020). Floral Trait Evolution of Angiosperms on Pacific Islands. *The American Naturalist*, 196. https://doi.org/10.1086/709018

Hiraiwa, M.K. & Ushimaru, A. (2017). Low functional diversity promotes niche changes in natural island pollinator communities. *Proceedings of the Royal Society B*, 284, 20162218. https://doi.org/10.1098/rspb.2016.2218

Hiraiwa, M.K. & Ushimaru, A. (2024). Loss of functional diversity rather than species diversity of pollinators decreases community-wide trait matching and pollination function. *Functional Ecology*, 38, 1296–1308. https://doi.org/10.1111/1365-2435.14527

Lord, J.M. (2015). Patterns in floral traits and plant breeding systems on Southern Ocean Islands. *AoB PLANTS*, 7, plv095. https://doi.org/10.1093/aobpla/plv095

Marjakangas, E.-L., Dalsgaard, B. & Ordonez, A. (2025). Fundamental interaction niches: towards a functional understanding of ecological networks' resilience. *Ecology Letters*, 28, e70146. https://doi.org/10.1111/ele.70146

Martén-Rodríguez, S., Fenster, C.B., Agnarsson, I., Skog, L.E. & Zimmer, E.A. (2010). Evolutionary breakdown of pollination specialization in a Caribbean plant radiation. *New Phytologist*, 188, 403–417. https://doi.org/10.1111/j.1469-8137.2010.03330.x

Martén-Rodríguez, S., Kress, W.J., Temeles, E.J. & Meléndez-Ackerman, E. (2011). Plant–pollinator interactions and floral convergence in two species of *Heliconia* from the Caribbean Islands. *Oecologia*, 167, 1075–1083. https://doi.org/10.1007/s00442-011-2043-8

Martén-Rodríguez, S., Quesada, M., Castro, A.-A., Lopezaraiza-Mikel, M. & Fenster, C.B. (2015). A comparison of reproductive strategies between island and mainland Caribbean Gesneriaceae. *Journal of Ecology*, 103, 1190–1204. https://doi.org/10.1111/1365-2745.12457

Méndez, M. (2025). Does flower size follow the 'island rule'? A commentary on 'Flower size evolution in the Southwest Pacific'. *Annals of Botany*, 136, i–ii. https://doi.org/10.1093/aob/mcaf053

Mortensen, H.S., Dupont, Y. & Olesen, J.M. (2008). A snake in paradise: disturbance of plant reproduction following extirpation of bird flower-visitors on Guam. *Biological Conservation*, 141, 2146–2154. https://doi.org/10.1016/j.biocon.2008.06.014

Pannell, J.R. (2015). Evolution of the mating system in colonizing plants. *Molecular Ecology*, 24, 2018–2037. https://doi.org/10.1111/mec.13087

Pannell, J.R. et al. (2015). The scope of Baker's law. *New Phytologist*, 208, 656–667. https://doi.org/10.1111/nph.13539

Rathcke, B.J. (2000). Hurricane causes resource and pollination limitation of fruit set in a bird-pollinated shrub. *Ecology*, 81, 1951–1958. https://doi.org/10.1890/0012-9658(2000)081[1951:HCRAPL]2.0.CO;2

Schrader, J., Wright, I.J., Kreft, H. & Westoby, M. (2021). A roadmap to plant functional island biogeography. *Biological Reviews*, 96, 2851–2870. https://doi.org/10.1111/brv.12782

Schueller, S.K. (2004). Self-pollination in island and mainland populations of the introduced hummingbird-pollinated plant, *Nicotiana glauca* (Solanaceae). *American Journal of Botany*, 91, 672–681. https://doi.org/10.3732/ajb.91.5.672

Schueller, S.K. (2007). Island–mainland difference in *Nicotiana glauca* (Solanaceae) corolla length: a product of pollinator-mediated selection? *Evolutionary Ecology*, 21, 81–98. https://doi.org/10.1007/s10682-006-9125-9

Temeles, E.J., Rah, Y.J., Andicoechea, J., Byanova, K.L., Giller, G.S.J., Stolk, S.B. & Kress, W.J. (2013). Pollinator-mediated selection in a specialized hummingbird–*Heliconia* system in the Eastern Caribbean. *Journal of Evolutionary Biology*, 26, 347–356. https://doi.org/10.1111/jeb.12053

Traveset, A., Tur, C., Trøjelsgaard, K., Heleno, R., Castro-Urgal, R. & Olesen, J.M. (2016). Global patterns of mainland and insular pollination networks. *Global Ecology and Biogeography*. https://doi.org/10.1111/geb.12362

Traveset, A. & Navarro, L. (2018). Plant reproductive ecology and evolution in the Mediterranean islands: state of the art. *Plant Biology*, 20(Suppl. 1), 63–77. https://doi.org/10.1111/plb.12636

Valido, A., Rodríguez-Rodríguez, M.C. & Jordano, P. (2019). Honeybees disrupt the structure and functionality of plant-pollinator networks. *Scientific Reports*, 9, 4711. https://doi.org/10.1038/s41598-019-41271-5

Wang, X. et al. (2020). Plants are visited by more pollinator species than pollination syndromes predicted in an oceanic island community. *Scientific Reports*, 10, 13918. https://doi.org/10.1038/s41598-020-70954-7

Watanabe, K., Kato, H., Kuraya, E. & Sugawara, T. (2018). Pollination and reproduction of *Psychotria homalosperma*, an endangered distylous tree endemic to the oceanic Bonin (Ogasawara) Islands, Japan. *Plant Species Biology*, 33, 16–27. https://doi.org/10.1111/1442-1984.12183

Whittaker, R.J., Fernández-Palacios, J.M. & Matthews, T.J. (2023). Island evolutionary syndromes in—and involving—plants. In *Island Biogeography: Geo-environmental Dynamics, Ecology, Evolution, Human Impact, and Conservation*, pp. 283–308. Oxford University Press. https://doi.org/10.1093/oso/9780198868569.003.0011

Zell, A.N., Miranda, C.H., Grady, E.L., Grossenbacher, D.L. & Igić, B. (2025). Island colonization in flowering plants is determined by the interplay of breeding system, lifespan, floral symmetry, and arrival opportunity. *New Phytologist*, 245, 420–432. https://doi.org/10.1111/nph.20234

## External source note

The complete source ledger for all 13 strict systems, including secondary supporting sources not cited in the main text, remains controlled by the Supplementary Reference Matrix. Inclusion in that matrix supports observed-state assignment only and does not imply cross-system causal equivalence.
