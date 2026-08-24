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

Such aggregate regularities combine at least two processes that need not generate the same prediction. Reproductive and life-history traits can influence **which lineages colonize, establish or persist on islands**, whereas already-established lineages can subsequently respond to altered pollinator function. The first is a filtering problem; the second is a post-establishment response problem. A flora can therefore be enriched for self-compatible or generalized strategies while individual established lineages still exhibit decline, compensation, trait-specific divergence or little response.

The post-establishment problem becomes especially important when interaction identity changes. Pollination function is not determined by the presence or absence of a nominal pollinator group alone. Species loss, partner replacement, changes in relative abundance and interaction rewiring can redistribute function among remaining partners. Network-resilience theory highlights rewiring and interaction heterogeneity as possible routes through which ecological function can persist after perturbation, while functional-interaction approaches emphasize the difference between realized partners and the larger trait space of potential partners (Bascompte & Scheffer, 2023; Marjakangas et al., 2025). These perspectives imply that the same decline in global pollinator opportunity can propagate strongly in one lineage, be redirected by partner context in another, and be attenuated downstream by reproductive assurance in a third.

This motivates a different island-ecology question from asking whether plants become more selfing, less specialized or morphologically simplified on average: **why does a common island-associated change in pollinator function produce different downstream responses among established plant lineages?** We considered three conditional layers. First, lineages occupy different positions in plant–pollinator functional space before the environment changes. Second, local interaction context determines how changed global opportunity is redistributed. Third, reproductive filters such as autonomous assurance change how service loss propagates into reproduction.

Agent-based models provide an experimental system for separating these layers because candidate mechanisms can be removed while holding the remainder of the architecture fixed. To avoid explaining each external system by post-hoc adjustment, the model architecture, stochastic envelopes, response-state definitions and falsification rules were frozen before the final external challenge. State-separability diagnostics were retained only as an inference guard: a simulated state can be ecologically compatible with a real system without uniquely identifying that system's causal mechanism.

We tested five linked hypotheses. **H1, the universal post-establishment response hypothesis**, predicts that a common island-like pollinator-functional perturbation pushes established lineages in one common downstream direction. **H2, the state-dependent branching hypothesis**, predicts that pre-existing functional-position heterogeneity is required for within-environment response branching. **H3, the context-dependent propagation hypothesis**, predicts that local interaction context reallocates branch identity and can either rescue or worsen individual lineage responses. **H4, the autonomous-assurance buffering hypothesis**, predicts that reproductive assurance reduces the downstream effect of service decline, with the stronger subprediction that it can reverse response sign. **H5, the cross-island recurrence hypothesis**, predicts that branching, same-direction propagation and buffering or alternative response states recur across independent island systems without system-specific retuning.

Together, these hypotheses distinguish an aggregate island syndrome from a universal within-lineage trajectory. The study does not test whether island syndromes exist. It tests whether one ecological perturbation must produce one post-establishment response and, if not, which conditional mechanisms generate the branching and propagation of outcomes.

# Materials and Methods

## Study design and frozen inference boundary

The study combined controlled simulation experiments with qualitative external island-system challenges. Primary numerical results came from frozen model outputs and matched ablations. External island outcomes were not used to choose model parameters, random seeds, state definitions or mechanisms. New field data were not an admission requirement for the primary simulation claim.

The model represented multiple plant lineages exposed to matched mainland-like and island-like pollinator environments. Pollination opportunity emerged from interaction between plant and pollinator functional traits under a fixed visit-budget formulation. Plant lineages could differ in initial standardized matching-trait position and, depending on the experimental layer, trait adjustment, local support, pollinator dependency, assurance ceiling, assurance responsiveness and partner effectiveness.

The standardized plant matching trait is an abstract relative functional coordinate. It is not assigned post hoc to corolla length, colour, nectar guides or any single empirical trait. Thus the model tests the ecological role of relative starting position without claiming that the same measured floral axis carries that position in every real system.

## H1: common perturbation versus universal response

Within-run mixed-sign branching was defined as the occurrence of both positive and negative lineage reproductive responses to the same matched mainland-like to island-like environmental contrast. A universal post-establishment response predicts that lineages within a matched run respond in the same direction. The frozen state atlas records branching, same-direction and buffering states generated without island-specific retuning.

## H2: residual ablation of the branch generator

A downstream factorial first toggled four mechanism families: local support, dependency heterogeneity, assurance responsiveness and partner effectiveness. Persistence of mixed-sign branching when all four were fixed off located the branch generator upstream of those modifiers.

The residual experiment then fixed the four downstream modifiers off and manipulated three remaining lineage-level sources: initial trait-position heterogeneity, trait-adjustment heterogeneity and assurance-ceiling heterogeneity. A residual factor was treated as necessary within the declared model when removing it eliminated mixed-sign runs and reduced mean within-run branching balance to zero while other single-factor removals retained branching.

The strongest boundary was tested once in an independent frozen block using seed 90260825, four replicates per saturation, 24 lineages, 120 steps and saturation values 1, 2 and 3. The design, decision rule and stop rule were specified before execution. No external target or empirical input selected the seed, and further seed searching was closed after the first successfully executed scientific result.

## H3: local interaction context and branch allocation

Local network context was evaluated by comparing local support off versus on under matched opportunity networks while autonomous assurance was disabled. Strong-rescue analyses were restricted to lineages for which global opportunity declined and support-off reproduction was negative. We distinguished magnitude attenuation, sign rescue and worsening. Because rescue and worsening were both permitted outcomes, this experiment tested context-dependent branch allocation and buffering capacity rather than assuming monotonic protection.

## H4: autonomous assurance

Autonomous assurance was evaluated in matched simulations with the assurance route enabled versus disabled while upstream effective-service changes were identical. We distinguished magnitude attenuation from strong sign rescue. Stability was tested in an independent frozen block and a broadened local-support envelope. A sign rescue seen in an earlier stochastic block was retained historically but was not promoted unless it replicated.

## H5: external island-system challenge

A global literature screen retained 54 geographic/system units as the screening denominator. Thirteen systems met a strict state-challenge contract based on source-locked evidence. The strict set contained three branching systems, six same-direction propagation systems, two buffering or alternative systems, one reproductive-axis-decoupling constraint and one retained falsification. These are **strict challenge systems**, not a random sample from which prevalence can be estimated.

The branching systems were the Izu multi-taxon Hiraiwa–Ushimaru system, Caribbean Gesneriaceae and the Canary Islands Teide honeybee-network experiment (Hiraiwa & Ushimaru, 2017, 2024; Martén-Rodríguez et al., 2010, 2015; Valido et al., 2019). Same-direction systems were Ogasawara *Psychotria homalosperma*, New Zealand *Rhabdothamnus solandri*, the Guam–Saipan bird-loss natural experiment, Seychelles invasive-ant disruption, Mauritius *Roussea simplex* invasive-ant disruption and Bahamas *Pavonia bahamensis* after hurricane-associated pollination loss (Watanabe et al., 2018; Anderson et al., 2011; Mortensen et al., 2008; Costa et al., 2023; Hansen & Müller, 2009; Rathcke, 2000). Buffering or alternative systems were Hawaiian lobelioids following bird extinctions and California Channel Islands *Nicotiana glauca* (Case et al., 2026a,b; Schueller, 2004, 2007). Puerto Rico–Mona *Guaiacum sanctum* was retained as reproductive-axis decoupling (Fumero-Cabán et al., 2022). Dominica *Heliconia* was retained as a failed signed-position projection rather than retuned after failure (Martén-Rodríguez et al., 2011; Temeles et al., 2013).

The external comparison was qualitative at the state level. It tested whether the already-frozen response vocabulary encompassed recurrent ecological outcomes without parameter fitting. It did not treat 13 systems as independent demonstrations of one causal mechanism.

## Supporting inference diagnostics

After the ecological mechanism tests were frozen, state-separability diagnostics quantified whether response states were unique to tested mechanism contrasts. These diagnostics are supporting rather than primary results. They prevent same-direction response from being interpreted as proof of homogeneous starting states and magnitude attenuation from being interpreted as unique evidence for autonomous assurance.

# Results

## H1: one island-like perturbation did not force one plant response

The frozen model generated multiple downstream response classes under one architecture. In the original residual block, mixed-sign branching occurred in 5 of 12 matched runs, giving a mixed-sign run fraction of 0.4167; the remaining 7 of 12 runs were same-direction despite heterogeneous starting states. The independent robustness block reproduced the same full-model mixed-sign frequency of 0.4167. H1 was therefore rejected: a common island-like perturbation does not imply a universal post-establishment response direction.

## H2: pre-existing functional position was the replicated minimal branch generator

Two-sided branching persisted when local support, dependency heterogeneity, assurance responsiveness and partner effectiveness were all fixed off. These downstream mechanisms were not required to generate opposite response signs.

In the residual ablation, the full model had mixed-sign frequency 0.4167 and mean within-run branching balance 0.2569. Removing initial trait-position heterogeneity reduced both to zero and changed 37 paired lineage signs. Removing trait-adjustment heterogeneity retained mixed-sign frequency 0.4167 and the same branching balance, with only two paired sign changes. Removing assurance-ceiling heterogeneity likewise retained mixed-sign frequency 0.4167 and produced no paired sign changes.

The independent block reproduced the same boundary. Full-model mixed-sign frequency was 0.4167 with mean within-run balance 0.2917. Removing initial functional-position heterogeneity again reduced both quantities to zero and changed 44 paired lineage signs, whereas removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity retained mixed-sign frequency 0.4167. Across two independently seeded frozen blocks, pre-existing lineage functional position was the only tested residual factor whose removal eliminated within-run response-sign branching. H2 was supported within the declared model.

## H3 and H4: local context reallocated branches, whereas assurance mainly attenuated magnitude

Although local support was not the origin of branching, it strongly changed branch identity. Removing local support changed 105 of 288 paired lineage response signs, compared with 13 of 288 for partner effectiveness, one for assurance responsiveness and none for dependency heterogeneity.

In the independent network-context experiment, among 96 eligible negative support-off reproductive contrasts, support on attenuated 85, crossed the sign boundary in 16 and worsened 11. H3 was therefore supported in a bidirectional form: local interaction context reallocates response branches and has buffering capacity, but can also amplify decline.

Autonomous assurance occupied a different regime. Among 216 lineages with upstream service decline, assurance reduced the magnitude of reproductive decline in 207 but produced no sign rescues. At saturation values 1, 2 and 3, attenuation occurred in 71/75, 73/76 and 63/65 declines, respectively, while sign rescue remained zero. A broadened support envelope likewise produced zero sign rescues among 525 eligible declines. H4 was therefore partially supported: assurance robustly attenuated decline magnitude, but robust qualitative sign reversal was not supported.

## H5: response-state diversity recurred across island systems

The 54-unit global screen yielded 13 strict external systems. Eleven were generative challenges: three branching, six same-direction propagation and two buffering or alternative cases. All 11 were covered or sign-compatible with response classes already present in the frozen model.

The branching systems provided examples in which shared or comparable island interaction change coexisted with divergent downstream plant responses. The propagation systems included bird functional loss, invasive-ant disruption, pollinator-access asymmetry and hurricane-associated pollination loss. Hawaiian lobelioids and Channel Islands *Nicotiana* provided buffering or alternative-response boundaries. Full system-level source assignments and claim boundaries are reported in Table 2 and the Supplementary Reference Matrix.

Two systems were intentionally not counted as generative successes. Puerto Rico–Mona *Guaiacum* retained a reproductive-axis-decoupling state because a large visitor-context difference coexisted with similar self/outcross seed-set indices while other reproductive axes differed (Fumero-Cabán et al., 2022). Dominica *Heliconia* retained a failed signed-position projection: the predeclared negative direction was not recovered and the mapping was not retuned (Martén-Rodríguez et al., 2011; Temeles et al., 2013).

H5 was therefore supported at the response-state level. Branching, propagation and buffering recur in independent island ecological contexts, but this recurrence does not establish one shared empirical mechanism.

## Supporting inference boundary

State-separability analysis reinforced the claim boundary rather than supplying the main biological result. Mixed-sign branching was highly specific but insensitive for initial functional-position heterogeneity within the tested intervention family: specificity was 1.0 but sensitivity 0.4167. Same-direction response was weak evidence for uniform starting states because 0.5833 of heterogeneity-on runs were also non-mixed. Network-context sign rescue was similarly specific but rare, whereas magnitude attenuation occurred commonly under both network context and assurance. These diagnostics are retained as Supplementary inference guards.

# Discussion

## Aggregate island syndromes can coexist with lineage-level branching

The central ecological result is that one island-like functional perturbation does not require one post-establishment plant trajectory. Opposite lineage responses arise in the frozen model under the same matched environmental shift, and the source of branching is pre-existing functional position rather than downstream dependency or reproductive assurance.

This result complements rather than contradicts island reproductive syndromes. Self-compatibility is over-represented in several island floras, and global analyses show that breeding system, lifespan, floral traits and arrival opportunity affect island occurrence (Grossenbacher et al., 2017; Zell et al., 2025). Island plant syntheses also document recurrent shifts in reproductive traits and pollination systems (Traveset & Navarro, 2018; Whittaker et al., 2023). These patterns can reflect colonization, establishment and persistence filters. The present study addresses a different layer: conditional on lineages being present, how does a changed pollinator-functional environment propagate through plants that begin in different states?

The distinction resolves an apparent tension. An island flora can show aggregate enrichment of self-compatible or generalized reproductive strategies while particular established lineages show decline, compensation, trait-specific divergence or little response. The present results reject a universal **post-establishment trajectory**, not recurrent island syndromes themselves.

## Functional starting state determines branch potential

The strongest mechanistic result is the replicated loss of branching when initial functional-position heterogeneity is removed. Response direction is therefore relational within the model: the effect of a changed pollinator environment depends not only on the perturbation but also on where a lineage already lies relative to functional opportunity.

This interpretation is intentionally more general than any single floral trait. Corolla length, colour, phenology or multivariate floral architecture may carry relevant functional position in particular systems, but the standardized coordinate is not empirically identified as one universal axis. A direct empirical test must therefore freeze a source-native signed plant position relative to a pollinator functional centre before downstream outcome inspection. Existing morphology comparisons are directionally consistent with starting-state dependence, but their measurement-error and errors-in-variables limits preclude direct causal validation.

## Local interaction context governs propagation, whereas assurance mainly dampens it

The model separates branch generation from branch allocation. Local support can change the sign of individual lineage responses even though branching remains possible without it. Network reorganization and rewiring are often discussed as sources of resilience because altered interactions can preserve function after partner loss (Bascompte & Scheffer, 2023; Marjakangas et al., 2025). The current results add an important qualification: additional local support rescued 16/96 eligible negative responses but worsened 11/96. Network context is therefore better described as a **bidirectional branch allocator with buffering capacity** than as a universal shield.

Autonomous assurance operates downstream in a different way. It repeatedly reduced decline magnitude but did not robustly convert negative responses into maintained or positive reproduction. This separates weak buffering—smaller decline—from strong sign rescue. The ecological ordering that emerges is hierarchical: pre-existing state generates branch potential, local interaction structure redistributes propagation, and reproductive assurance dampens downstream magnitude.

## Cross-island recurrence supports a response architecture, not a universal mechanism

The external island series extends the relevance of the model beyond one focal archipelago. The strict systems include pollinator functional-diversity change in the Izu region (Hiraiwa & Ushimaru, 2017, 2024), pollination-system transitions in Caribbean Gesneriaceae (Martén-Rodríguez et al., 2010, 2015), managed-honeybee network disruption in the Canary Islands (Valido et al., 2019), bird functional loss in New Zealand and the Marianas (Anderson et al., 2011; Mortensen et al., 2008), invasive-ant disruption in Seychelles and Mauritius (Costa et al., 2023; Hansen & Müller, 2009), hurricane-associated pollination loss in the Bahamas (Rathcke, 2000), and post-extinction or alternative reproductive states in Hawaiʻi and the California Channel Islands (Case et al., 2026a,b; Schueller, 2004, 2007).

The comparison is not a prevalence estimate: the 13 systems entered through a strict evidence gate rather than random sampling. Nor does state compatibility show that the synthetic initial-position mechanism operates in all systems. A same-direction natural experiment can occupy the model's state space even when the real proximate cause is bird extinction, invasive ants or another system-specific process.

The external challenge is therefore architectural. Independent systems repeatedly occupy branching, propagation and buffering/alternative states, while *Guaiacum* and Dominica protect the analysis from becoming a success-only catalogue. *Guaiacum* prevents multiple reproductive axes from being collapsed into one buffered/unbuffered label, and the Dominica result shows that a predeclared empirical mapping can fail without triggering post-hoc retuning.

## Unresolved empirical translation is the next programme, not a submission prerequisite

Three empirical questions follow directly from the current result. First, the synthetic functional starting position requires an outcome-blind, source-native real-world mapping. Second, the network-context route requires matched visitor-specific rate and direct effectiveness so that effective pollination is not inferred from visitation, identity or richness alone. Third, no current external system closes the full chain from pollinator functional change through effective service and dependency/assurance to downstream response on compatible units.

These are next-observation questions rather than missing pieces of the current synthetic claim. They should be tested prospectively rather than filled with proxies or post-hoc mappings. None requires reopening the frozen simulation programme before submission.

## Inference boundary

Observable response states are not equally informative about their generating mechanism. Mixed-sign branching is informative when present but need not appear in every heterogeneous run; same-direction response therefore cannot be used to infer homogeneous lineages. Likewise, attenuation alone cannot distinguish network-context compensation from autonomous assurance because both routes can reduce magnitude.

This is the appropriate role of state separability in the current paper: it prevents the ecological synthesis from becoming stronger than the evidence. The external challenge establishes recurrence of response states, not one-to-one causal identification across islands.

# Conclusion

Island-associated pollinator simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal post-establishment plant trajectory. In the frozen ABM, pre-existing lineage functional position is the replicated minimal generator of within-environment response branching. Local interaction context reallocates branch identity and can rescue or worsen propagation, whereas autonomous assurance mainly attenuates reproductive decline magnitude.

Independent island systems repeatedly occupy the same broad response classes without system-specific retuning. Those recurrences support a state-dependent island-response architecture, while the retained *Guaiacum* constraint and Dominica failure prevent a universal-mechanism interpretation.

The island-ecology synthesis is therefore conditional rather than syndrome-only: **aggregate island syndromes can coexist with lineage-level branching because colonization and persistence determine which states arrive, while functional starting state and local ecological context determine how established lineages respond after pollinator environments change.**

# References

Anderson, S.H., Kelly, D., Ladley, J.J., Molloy, S. & Terry, J. (2011). Cascading effects of bird functional extinction reduce pollination and plant density. *Science*, 331, 1068–1071. https://doi.org/10.1126/science.1199092

Bascompte, J. & Scheffer, M. (2023). The resilience of plant–pollinator networks. *Annual Review of Entomology*, 68, 363–380. https://doi.org/10.1146/annurev-ento-120120-102424

Case, S.B., Hagemann, M.E., Drake, D.R., Postelli, K., Pender, R.J., Millikin, P.W. & Rico-Guevara, A. (2026a). Bird extinctions shift bill–flower trait matching in Hawaiian lobelioids. *Functional Ecology*, early view. https://doi.org/10.1111/1365-2435.70415

Case, S.B., Drake, D.R., Epperly, K., Steinbronn, C., Kanakaokai, K., Hagemann, M.E., Kingsley, N.H., Gregory, S.B., Mounce, H.L. & Rico-Guevara, A. (2026b). Mutualism and antagonism in a post-extinction Hawaiian bird–lobelioid pollination system. *Ecology and Evolution*, 16, e74123. https://doi.org/10.1002/ece3.74123

Costa, A., Heleno, R., Font Freide, E., Dufrene, Y., Huckle, E. & Kaiser-Bunbury, C.N. (2023). Impacts of invasive ants on pollination of native plants are similar in invaded and restored plant communities. *Global Ecology and Conservation*, 42, e02413. https://doi.org/10.1016/j.gecco.2023.e02413

Fumero-Cabán, J.J., Meléndez-Ackerman, E.J. & Rojas-Sandoval, J. (2022). Pollination ecology and breeding system of the tropical tree *Guaiacum sanctum* on two Caribbean islands with contrasting pollinator assemblages. *Journal of Pollination Ecology*, 32, 139–153. https://doi.org/10.26786/1920-7603(2022)669

Grossenbacher, D.L. et al. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. https://doi.org/10.1111/nph.14534

Hansen, D.M. & Müller, C.B. (2009). Invasive ants disrupt gecko pollination and seed dispersal of the endangered plant *Roussea simplex* in Mauritius. *Biotropica*, 41, 202–208. https://doi.org/10.1111/j.1744-7429.2008.00473.x

Hiraiwa, M.K. & Ushimaru, A. (2017). Low functional diversity promotes niche changes in natural island pollinator communities. *Proceedings of the Royal Society B*, 284, 20162218. https://doi.org/10.1098/rspb.2016.2218

Hiraiwa, M.K. & Ushimaru, A. (2024). Loss of functional diversity rather than species diversity of pollinators decreases community-wide trait matching and pollination function. *Functional Ecology*, 38, 1296–1308. https://doi.org/10.1111/1365-2435.14527

Marjakangas, E.-L., Dalsgaard, B. & Ordonez, A. (2025). Fundamental interaction niches: towards a functional understanding of ecological networks' resilience. *Ecology Letters*, 28, e70146. https://doi.org/10.1111/ele.70146

Martén-Rodríguez, S., Fenster, C.B., Agnarsson, I., Skog, L.E. & Zimmer, E.A. (2010). Evolutionary breakdown of pollination specialization in a Caribbean plant radiation. *New Phytologist*, 188, 403–417. https://doi.org/10.1111/j.1469-8137.2010.03330.x

Martén-Rodríguez, S., Kress, W.J., Temeles, E.J. & Meléndez-Ackerman, E. (2011). Plant–pollinator interactions and floral convergence in two species of *Heliconia* from the Caribbean Islands. *Oecologia*, 167, 1075–1083. https://doi.org/10.1007/s00442-011-2043-8

Martén-Rodríguez, S., Quesada, M., Castro, A.-A., Lopezaraiza-Mikel, M. & Fenster, C.B. (2015). A comparison of reproductive strategies between island and mainland Caribbean Gesneriaceae. *Journal of Ecology*, 103, 1190–1204. https://doi.org/10.1111/1365-2745.12457

Mortensen, H.S., Dupont, Y. & Olesen, J.M. (2008). A snake in paradise: disturbance of plant reproduction following extirpation of bird flower-visitors on Guam. *Biological Conservation*, 141, 2146–2154. https://doi.org/10.1016/j.biocon.2008.06.014

Rathcke, B.J. (2000). Hurricane causes resource and pollination limitation of fruit set in a bird-pollinated shrub. *Ecology*, 81, 1951–1958. https://doi.org/10.1890/0012-9658(2000)081[1951:HCRAPL]2.0.CO;2

Schueller, S.K. (2004). Self-pollination in island and mainland populations of the introduced hummingbird-pollinated plant, *Nicotiana glauca* (Solanaceae). *American Journal of Botany*, 91, 672–681. https://doi.org/10.3732/ajb.91.5.672

Schueller, S.K. (2007). Island–mainland difference in *Nicotiana glauca* (Solanaceae) corolla length: a product of pollinator-mediated selection? *Evolutionary Ecology*, 21, 81–98. https://doi.org/10.1007/s10682-006-9125-9

Temeles, E.J., Rah, Y.J., Andicoechea, J., Byanova, K.L., Giller, G.S.J., Stolk, S.B. & Kress, W.J. (2013). Pollinator-mediated selection in a specialized hummingbird–*Heliconia* system in the Eastern Caribbean. *Journal of Evolutionary Biology*, 26, 347–356. https://doi.org/10.1111/jeb.12053

Traveset, A. & Navarro, L. (2018). Plant reproductive ecology and evolution in the Mediterranean islands: state of the art. *Plant Biology*, 20(Suppl. 1), 63–77. https://doi.org/10.1111/plb.12636

Valido, A., Rodríguez-Rodríguez, M.C. & Jordano, P. (2019). Honeybees disrupt the structure and functionality of plant-pollinator networks. *Scientific Reports*, 9, 4711. https://doi.org/10.1038/s41598-019-41271-5

Watanabe, K., Kato, H., Kuraya, E. & Sugawara, T. (2018). Pollination and reproduction of *Psychotria homalosperma*, an endangered distylous tree endemic to the oceanic Bonin (Ogasawara) Islands, Japan. *Plant Species Biology*, 33, 16–27. https://doi.org/10.1111/1442-1984.12183

Whittaker, R.J., Fernández-Palacios, J.M. & Matthews, T.J. (2023). Island evolutionary syndromes in—and involving—plants. In *Island Biogeography: Geo-environmental Dynamics, Ecology, Evolution, Human Impact, and Conservation*, pp. 283–308. Oxford University Press. https://doi.org/10.1093/oso/9780198868569.003.0011

Zell, A.N., Miranda, C.H., Grady, E.L., Grossenbacher, D.L. & Igić, B. (2025). Island colonization in flowering plants is determined by the interplay of breeding system, lifespan, floral symmetry, and arrival opportunity. *New Phytologist*, 245, 420–432. https://doi.org/10.1111/nph.20234

## External source note

The complete source ledger for all 13 strict systems, including secondary supporting sources not cited in the main text, remains controlled by the Supplementary Reference Matrix. Inclusion in that matrix supports observed-state assignment only and does not imply cross-system causal equivalence.
