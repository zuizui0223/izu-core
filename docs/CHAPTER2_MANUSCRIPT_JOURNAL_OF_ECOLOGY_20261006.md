# Reproductive assurance can precede without causing floral investment decline under pollinator isolation

## Abstract

1. Pollinator limitation on islands is often associated with increased reproductive assurance and reduced floral attraction, but temporal order alone cannot show whether one evolutionary change causes the other. We tested whether a selfing-associated response that appears first is also required for later reduction in pollinator-facing floral investment.

2. We used one explicit plant–pollinator eco-evolutionary model in which visitor functional types determine pollen transfer, plants reproduce through outcrossing and autonomous selfing, offspring inherit three diploid traits, and finite recruitment determines realized evolutionary change. Fixed-plant assays measured reproductive returns before plant evolution; maintained-isolation trajectories measured evolutionary order; and a matched intervention prevented reproductive-assurance evolution while leaving realized selfing responsive. The primary temporal result was prospectively replicated with 64 new visitor histories and eight new nested demographic repeats.

3. At the same plant state, stronger visitor limitation reversed the marginal reproductive contribution of floral investment from +0.5793 to −0.7004 in the delayed-selfing setting as the outcross component fell from +1.6523 to +0.0854. Reproductive assurance reached the preregistered 0.05 sustained-change threshold first in 51/64 new visitor histories (proportion 0.797; 95% history-bootstrap 0.688–0.891).

4. Blocking assurance evolution did not prevent investment decline: in the independent fixed-assurance replication, far-population investment changed by −0.3060 [−0.3181, −0.2941], and the far-minus-near contrast was −0.4354 [−0.4533, −0.4172]. The assurance-first sequence was not universal: under prior selfing with positive mutation only 30/64 histories were assurance-first at the same threshold.

5. **Synthesis.** Pollinator isolation can make reproductive assurance change before floral attraction while reducing attraction through a partly parallel ecological route. Evolutionary sequence therefore does not by itself identify causal necessity. Distinguishing what changes first from what is required for change sharpens how island selfing syndromes and other multivariate ecological responses should be interpreted.

## Keywords

floral evolution; island ecology; plant–pollinator interactions; reproductive assurance; selfing syndrome; temporal sequence; visitor limitation

# Introduction

Pollinator-community change does not act on floral traits directly. Visitors differ in functional fit and effectiveness, those differences alter pollen transfer and mating opportunity, reproductive success determines which alleles enter the next generation, and demographic persistence determines whether an evolutionary response is realized. A contemporary pollinator assemblage and a contemporary floral phenotype are therefore separated by several biological stages.

Island plant–pollinator systems make this distinction especially important. Oceanic-island pollination networks can be smaller and simpler than mainland networks, and network size is associated with isolation (Traveset et al., 2016). Self-compatibility is over-represented among island species in several plant families (Grossenbacher et al., 2017). Yet comparative evidence does not support one universal floral response: a Pacific sister-taxon analysis found no overall reduction in flower size, with substantial differences among archipelagos and families (Hetherington-Rauth & Johnson, 2020), while coastal-island work links changes in pollinator functional diversity to trait matching and pollination function (Hiraiwa & Ushimaru, 2017, 2024). Repeated ecological pressure therefore need not imply one serial pathway or one floral endpoint.

A common interpretation of pollinator loss is sequential. When pollinators become unreliable, autonomous selfing can provide reproductive assurance; traits that improve selfing may evolve rapidly, and reduced investment in attraction may follow. Experimental evolution in *Mimulus guttatus* already supports rapid evolution after pollinator loss and motivated a sequential selfing-syndrome interpretation (Bodbyl Roels & Kelly, 2011; Busch et al., 2022). Experimental pollination regimes can also drive joint divergence in mating-system and floral traits (Gervasi & Schiestl, 2017), and theory has long treated allocation to attraction and selfing as coupled reproductive decisions (Sakai, 1995).

However, observing that one trait changes first does not establish that its evolution is required for a later response. Visitor limitation can simultaneously create unfertilized ovules that autonomous selfing can rescue and reduce the marginal outcross return to floral attraction. If the latter route is strong enough, floral investment could decline even when reproductive-assurance capacity is prevented from evolving. In that case, a selfing-associated response may be temporally first while the two traits remain partly parallel consequences of the same ecological change.

We test that distinction with one explicit plant–pollinator eco-evolutionary model. The model links visitor replenishment and loss to functional pollen transfer, outcrossing, autonomous selfing, inbreeding depression, Mendelian inheritance and finite recruitment. We separate three questions that are often compressed into one narrative: (1) does visitor limitation change the reproductive return to floral investment before plant evolution; (2) which inherited response reaches a declared change threshold first; and (3) is evolution of the first-changing trait necessary for the second response? A final reproductive assay asks whether a smaller pollen deficit necessarily implies greater viable offspring production.

The central prediction is deliberately asymmetric. If a strict serial selfing pathway explains reduced floral investment, preventing reproductive-assurance evolution should remove or greatly weaken investment decline. If visitor limitation also lowers the outcross return to attraction directly, investment can decline even when assurance evolution is blocked. We test this prediction first in a discovery cohort and then under a prospectively frozen replication using entirely new visitor histories and demographic repeats.

# Materials and Methods

## Eco-evolutionary model

The model represents a focal plant population embedded in an externally supported visitor environment. Plants carry three inherited diploid traits on bounded 0–1 scales: an access/matching position, floral investment and reproductive-assurance capacity. Visitor functional types determine finite compatible pollen transfer. Outcrossing contributes maternal and paternal gametes; autonomous selfing can fertilize ovules according to the declared reproductive setting; inbreeding depression reduces viable selfed offspring; and Mendelian inheritance precedes finite recruitment and adult survival.

The primary population starts with 48 plants and four visitor functional types. Plant immigration is absent. Visitor types are replenished from an external source and can disappear through a common per-type loss process. Isolation is represented by reduced successful visitor establishment, not by island area. In the exponential-arrival parameterization, expected successful establishment per reproductive update is
`lambda = 0.24 exp(-d)`, where `d` is a synthetic dispersal coordinate. The near and far environments use `d = 0` and `d = 3`, respectively. These coordinates are not kilometres, and one reproductive update is not calibrated to a natural year.

We analyse two reproductive settings separately. The focal primary setting uses delayed selfing with reproductive-assurance cost 0.5. A second setting uses prior selfing with zero assurance cost and serves as an explicit scope comparison. Both use inbreeding depression 0.5. Their contrast therefore changes selfing timing and assurance cost jointly and is not interpreted as an isolated timing effect.

## Fixed-plant reproductive-return assay

To identify an ecological route before plant evolution, we held the plant state fixed and changed only visitor exposure. Each assay used the same 48-plant state with reproductive-assurance capacity 0.5 and compared paired near and far visitor histories at prespecified snapshots. Floral-investment values were perturbed locally while the current resident pollen environment was held fixed. Reproductive contribution included maternal outcross production, paternal outcross success and viable selfed offspring, together with the declared investment cost.

The primary readout is the marginal contribution of floral investment to total viable reproduction, decomposed into outcross and viable-selfed components. Because visitor amount and composition both change between near and far histories, this is an isolation-generated visitor-environment contrast rather than a richness-only experiment.

## Maintained-isolation evolutionary sequence

The discovery cohort followed sustained near and far visitor environments for 1,000 reproductive updates. It used 64 independent visitor histories and eight nested demographic repeats per history. The plant traits were inherited and allowed to evolve. The primary sequence cell used delayed selfing, assurance cost 0.5 and mutation probability 0.01 per transmitted allele; the prior-selfing setting and mutation probability 0 were retained as scope and sensitivity cells.

For each visitor history, trait trajectories were first averaged across the eight demographic repeats among occupied populations. The primary event definition was a founder-relative change of 0.05 sustained for 20 consecutive updates. Reproductive assurance was evaluated for an increase and floral investment for a decrease. Events within five updates were classed as near-simultaneous. Thresholds 0.025 and 0.10 were retained as sensitivity analyses. Unreached events were censored rather than assigned an artificial crossing time.

The ecological inference unit is the visitor history. Demographic repeats quantify within-history realization but do not increase the independent denominator from 64 to 512.

## Fixed-assurance intervention

Temporal precedence was separated from causal necessity with a matched intervention. All founders began with reproductive-assurance capacity 0.5 and no standing variation at the assurance locus. In the fixed mode, capacity remained 0.5 and mutation was disabled at that locus; matching and investment inheritance and mutation were unchanged. In the evolving mode, assurance could mutate and respond. Realized selfing could still vary in the fixed mode because pollen supply and mating opportunities changed, so this intervention tests the necessity of **assurance evolution**, not the absence of selfing and not a complete mediation fraction.

The original campaign crossed near and far visitor exposure, both reproductive settings, mutation probabilities 0 and 0.01, 64 histories and eight repeats. The main causal readouts at update 1,000 were investment change from founders within the far arm and the paired far-minus-near investment contrast.

## Prospectively frozen independent confirmation

After the discovery sequence and fixed-assurance results were known, but before confirmatory outcomes were generated, we froze an independent replication design. Discovery histories 76001–76064 and demographic repeats 7101–7108 were not reused. The confirmation used 64 new visitor histories (26100601–26100664) and eight new demographic repeats (26101601–26101608), while retaining the original founder specification and biological model.

The temporal component contained 2,048 far-arm trajectories crossing two reproductive settings, two mutation probabilities, 64 histories and eight repeats. The causal-necessity component contained 2,048 fixed-assurance trajectories crossing both reproductive settings, positive mutation, near/far exposure, 64 histories and eight repeats. Thus the complete confirmatory campaign contained 4,096 trajectories.

The preregistered primary cell was delayed selfing, assurance cost 0.5 and mutation probability 0.01. Assurance-first success required a proportion greater than 0.50 across all 64 histories and a lower 95% visitor-history bootstrap bound greater than 0.50 at the 0.05 threshold. Near-simultaneous, investment-first and censored histories counted as not assurance-first in this binary success proportion. The 0.025 and 0.10 thresholds were frozen sensitivity analyses.

For the fixed-assurance confirmation, both the far investment change from founders and the far-minus-near investment contrast at update 1,000 had to be negative, with both upper 95% history-bootstrap bounds below zero. Each arm also had to retain at least 90% occupancy and at least 60 of 64 histories had to remain estimable. No seed extension, threshold retuning, tie-window change, outcome substitution or biological parameter adjustment was allowed after execution began. Secondary cells were reported regardless of direction but could not rescue the primary adjudication.

## Pollen-deficit and viable-offspring assay

A separate fixed-trait assay evaluated whether a lower pollen deficit necessarily meant greater viable reproductive output. Within the same visitor environment, investment and reproductive-assurance capacity were manipulated across fixed values while plant reproduction was recalculated without allowing evolution. The assay retained selfing timing, investment costs and inbreeding depression. We report both the fractional viable pollen deficit and absolute viable maternal offspring because the two quantities need not move together.

## Statistical summaries and claim boundary

Intervals are descriptive visitor-history bootstrap intervals unless otherwise stated. Trait values after extinction are undefined rather than coded as zero, and occupancy is reported separately. The confirmatory decision uses the frozen success and admissibility criteria above.

The model is designed to test sufficiency and causal separation under declared synthetic conditions. It is not calibrated to named islands, natural kilometres, natural evolutionary time, measured flower colour or a particular corolla dimension. Additional replenishment-rate surfaces, reciprocal-selection diagnostics, deterministic genotype-density calculations, mutation/history experiments and natural-system confrontations are reported in Supporting Information and do not alter the primary confirmatory decision.

# Results

## Visitor limitation reduced the return to floral investment before plant evolution

At the same fixed plant state and reproductive-assurance capacity 0.5, the visitor environment changed the marginal reproductive contribution of floral investment. In the delayed-selfing setting, the mean total investment contribution derivative was +0.5793 under near exposure and −0.7004 under far exposure. The outcross component fell from +1.6523 to +0.0854. The viable-selfed component shifted in the opposite direction and partly offset, rather than generated, the decline in the total return to investment. The investment-cost coefficient itself was unchanged.

Thus the model contains an upstream ecological route from visitor limitation to reduced attraction investment that is present before reproductive-assurance capacity or floral investment has evolved.

## Reproductive assurance changed first in the focal delayed-selfing regime

In the discovery cohort, reproductive assurance crossed the primary 0.05 sustained-change threshold before investment in 51 of 64 far-history means in the delayed-selfing, assurance-cost 0.5, positive-mutation cell; the remaining 13 histories were near-simultaneous. The same qualitative ordering persisted at thresholds 0.025 and 0.10.

The prospectively frozen replication produced the same primary classification count on entirely new visitor histories: 51/64 were assurance-first and 13/64 were near-simultaneous. The assurance-first proportion was 0.7969, with a 95% visitor-history bootstrap interval of 0.6875–0.8906. The frozen criterion requiring both a majority and a lower interval bound above 0.50 therefore passed.

The threshold sensitivity was also preserved in the independent cohort. Assurance was first in 48/64 histories at threshold 0.025 (95% interval 0.6406–0.8445), 51/64 at 0.05 (0.6875–0.8906) and 59/64 at 0.10 (0.8438–0.9844).

However, the ordering was setting-specific. In the independent prior-selfing, positive-mutation cell, only 30/64 histories were assurance-first at the primary 0.05 threshold and 34/64 were near-simultaneous; the assurance-first interval was 0.3438–0.5938. The confirmed sequence is therefore restricted to the delayed-selfing, costly-assurance regime rather than interpreted as a universal selfing-syndrome law.

## Assurance evolution was not required for investment decline

The original fixed-assurance intervention showed that far populations still reduced floral investment when assurance capacity was held at 0.5. In the delayed-selfing setting, the far investment change from founders was −0.3099, with a descriptive 95% interval wholly below zero. The prior-selfing setting showed the same sign.

The preregistered new-history intervention independently confirmed this result. In the delayed-selfing primary cell, far investment changed by −0.3060 [−0.3181, −0.2941], and the far-minus-near investment contrast was −0.4354 [−0.4533, −0.4172]. All 64 histories were eligible and terminal occupancy was 1.0 in both near and far arms. Both frozen negative-effect criteria therefore passed.

The secondary prior-selfing cell also retained negative effects: far investment changed by −0.3316 [−0.3418, −0.3210] from founders and the far-minus-near contrast was −0.3094 [−0.3246, −0.2942]. This broader sign consistency in the intervention does not broaden the sequence claim, because the temporal ordering itself differed among reproductive settings.

Together, the fixed-plant and fixed-assurance results separate the causal structure. Visitor limitation can directly lower the reproductive return to attraction, and investment decline can proceed without evolution of assurance capacity even in a regime where assurance often reaches the declared evolutionary threshold first.

## A smaller pollen deficit did not guarantee greater viable reproduction

In the delayed-selfing far-environment assay, increasing floral investment from 0.25 to 0.75 at assurance capacity 0.5 reduced the fractional viable pollen deficit by 0.0104 but reduced viable maternal offspring by 15.72 per 48 plants. Investment can therefore improve a proportional pollen-deficit measure while reducing absolute viable reproduction once allocation cost, mating route and inbreeding depression are retained.

This result is used as a reproductive consequence of the model mechanism rather than as a claim that pollen-limitation metrics are generally invalid. Previous empirical and synthetic work already shows that pollen-supplementation responses depend on response variable, resource reallocation and the viability of selfed offspring (Ashman et al., 2004; Knight et al., 2005, 2006; Van Etten et al., 2015).

# Discussion

## Evolutionary sequence is not causal necessity

The central result is a separation that is easy to lose in multivariate evolutionary narratives. Reproductive assurance often changed first in the focal delayed-selfing regime, and that temporal pattern was independently reproduced under a prospectively frozen design. Yet floral investment still declined when assurance evolution was blocked. A first-changing trait is therefore not automatically a necessary cause of a later trait response.

The fixed-plant reproductive assay shows why. Stronger visitor limitation sharply reduced the outcross return on additional floral investment and reversed its total marginal reproductive contribution before any plant trait evolved. Autonomous selfing partly buffered the loss of outcross return but did not generate it. Isolation can therefore act on the reproductive economics of attraction directly.

This distinction changes how a sequential selfing syndrome should be interpreted. Rapid reproductive-assurance evolution after pollinator loss is well established experimentally (Bodbyl Roels & Kelly, 2011; Busch et al., 2022), and divergent pollinator regimes can jointly alter floral signals and autonomous self-pollination (Gervasi & Schiestl, 2017). Our result does not replace that literature with an alternative universal sequence. Instead, it shows that even when a selfing-associated trait clearly changes first, the later floral response can remain supported by a partly parallel ecological route.

## The sequence is conditional on reproductive context

The independent replication also identifies the domain of the result. The assurance-first majority was strong across all three preregistered thresholds in the delayed-selfing, assurance-cost setting, but it was absent at the primary threshold under prior selfing with positive mutation. The two settings differ jointly in selfing timing and assurance cost, so the contrast does not isolate one parameter. Its value is instead to prevent an overgeneralized conclusion.

A setting-specific result is informative because island floral evolution is itself heterogeneous. Comparative work does not support a universal reduction in flower size across islands (Hetherington-Rauth & Johnson, 2020), and island pollinator systems differ in functional composition and trait matching (Hiraiwa & Ushimaru, 2017, 2024). The model suggests one reason why a repeated ecological problem need not generate a single temporal syndrome: the same visitor limitation is filtered through the resident mating system and allocation structure.

The result also cautions against reading geographic effect size as the amount of evolution. In an exploratory secondary analysis, allowing assurance to evolve narrowed the near–far investment contrast because investment changed in both environments. That interaction was not included in the independent confirmatory campaign and remains supporting evidence, but it illustrates the broader point that between-environment divergence and within-population evolutionary change are different estimands.

## Pollination, inheritance and finite realization are distinct stages

The model preserves a causal order from visitor environment to pollen transfer, mating, viable reproduction, inheritance and finite recruitment. A fixed-state reproductive return is therefore not identical to an inherited response, and an expected inherited response is not identical to a realized finite-population trajectory. This layered structure matters for interpretation even though the primary paper does not require the unresolved high-resolution deterministic comparison.

Finite populations determine which variants persist, which histories remain occupied and which expected responses are realized. The confirmatory design therefore treats the 64 visitor histories as the independent ecological units and the eight demographic repeats as nested realizations. The exact agreement in the final assurance-first count between discovery and replication does not imply copied trajectories: the new histories produced different crossing-time patterns across the 1,000-update horizon.

The model does not establish a universal finite-population correction or a converged finite-versus-continuum effect. Those numerical questions remain separate. The ecological inference here requires only that the same finite individual-based rules were applied under a frozen design and independently reproduced the declared sequence and intervention results.

## Reproductive consequence is not captured by pollen deficit alone

The pollen assay reinforces the need to distinguish process measures from demographic consequence. A smaller proportional viable pollen deficit can coexist with fewer viable offspring when greater attraction investment carries an allocation cost and selfed offspring experience inbreeding depression. This is consistent with the broader pollen-limitation literature, which has long emphasized dependence on resources, response variable and post-fertilization performance (Ashman et al., 2004; Knight et al., 2005, 2006; Van Etten et al., 2015).

For island studies, this means that evidence for pollen limitation and evidence for selection on floral investment are related but not interchangeable. A field supplementation experiment can diagnose one component of reproductive opportunity without reconstructing the net marginal value of attraction. The model provides a controlled example of how that separation can arise from familiar reproductive processes rather than from an additional hidden mechanism.

## Ecological scope and empirical tests

The model is ecologically explicit but deliberately uncalibrated. Visitor types are functional agents rather than measured species abundances; distance is a synthetic dispersal coordinate; time is measured in reproductive updates; floral investment and matching are abstract traits; and inbreeding depression is fixed rather than dynamically purged. We therefore infer mechanism and sufficiency, not natural effect size, evolutionary rate or the history of a named island population.

Natural systems nevertheless contain the relevant ingredients. Island networks differ in size and functional organization (Traveset et al., 2016), self-compatibility is over-represented in some island floras (Grossenbacher et al., 2017), and functional changes in pollinator communities can alter matching and pollination function (Hiraiwa & Ushimaru, 2017, 2024). What is rarely observed on the same populations is the full longitudinal chain from visitor exposure to effective pollen transfer, mating route, viable reproductive return and inherited trait change.

The strongest empirical test is therefore transition-linked rather than purely comparative. Populations experiencing a measured change in pollinator replenishment should be followed through functional visitor exposure, effective pollen transfer, autonomous reproduction, viable offspring production and inherited floral change. The model predicts that reproductive assurance may change before attraction declines without being a necessary mediator of that decline, and that this ordering should depend on reproductive context.

# Conclusion

Under sustained visitor-replenishment limitation, reproductive assurance can reach a declared evolutionary threshold before floral investment declines, yet assurance evolution is not required for that decline. The same ecological change can simultaneously increase the value of reproductive insurance and reduce the outcross return to attraction.

The independently confirmed result is therefore not a universal selfing-first law. It is a bounded demonstration that **temporal precedence and causal necessity are different biological questions**. Separating them provides a more precise way to interpret island selfing syndromes and other multivariate evolutionary responses to changing ecological interactions.

# Figure captions

**Figure 1. Visitor limitation reduces the reproductive return to floral investment before plant evolution.** At the same fixed plant state and reproductive-assurance capacity 0.5, near and far visitor exposures are compared for outcross, viable-selfed and total reproductive-contribution slopes. In the delayed-selfing setting, the total investment contribution changes from +0.5793 to −0.7004 as the outcross component falls from +1.6523 to +0.0854. The viable-selfed component partly offsets the decline. The assay measures current reproductive return and does not include plant evolution.

**Figure 2. Evolutionary sequence and causal necessity are different questions.** Panel A shows discovery history-level crossing times and the prospectively frozen independent replication. In the delayed-selfing, costly-assurance positive-mutation cell, reproductive assurance is first in 51/64 histories in both cohorts; the replication 95% history-bootstrap interval for the assurance-first proportion is 0.6875–0.8906. The prior-selfing positive-mutation cell is shown as a scope boundary rather than pooled with the primary result. Panel B shows the fixed-assurance intervention. In the independent replication, far investment change is −0.3060 [−0.3181, −0.2941] and far-minus-near investment is −0.4354 [−0.4533, −0.4172]. Fixed assurance blocks assurance evolution but not realized selfing.

**Figure 3. Lower pollen deficit need not mean greater viable reproduction.** Within fixed visitor environments, floral investment and reproductive-assurance capacity are manipulated while reproduction is recalculated. In the delayed-selfing far-environment comparison, increasing investment from 0.25 to 0.75 at assurance capacity 0.5 reduces the fractional viable pollen deficit by 0.0104 while reducing viable maternal offspring by 15.72 per 48 plants. The panel separates a proportional pollen-deficit measure from absolute viable reproductive output.

# Data availability

The confirmatory design, result summary and history-level statistical exports are preserved in the project repository. The complete raw confirmatory bundle has been assembled and privately preserved with a frozen SHA-256 digest. A DOI-backed public deposit is pending and must be inserted here before submission. No manuscript claim depends on the unresolved high-resolution deterministic/PDE branch.

# References

Grossenbacher, D.L., Brandvain, Y., Auld, J.R., Burd, M., Cheptou, P.-O., Conner, J.K., Grant, A.G., Hovick, S.M., Pannell, J.R., Pauw, A., Petanidou, T., Randle, A.M., Rubio de Casas, R., Vamosi, J.C., Winn, A.A., Igić, B., Busch, J.W., Kalisz, S. & Goldberg, E.E. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. https://doi.org/10.1111/nph.14534

Hetherington-Rauth, M.C. & Johnson, M.T.J. (2020). Floral trait evolution of angiosperms on Pacific islands. *The American Naturalist*, 196, 87–100. https://doi.org/10.1086/709018

Hiraiwa, M.K. & Ushimaru, A. (2017). Low functional diversity promotes niche changes in natural island pollinator communities. *Proceedings of the Royal Society B*, 284, 20162218. https://doi.org/10.1098/rspb.2016.2218

Hiraiwa, M.K. & Ushimaru, A. (2024). Loss of functional diversity rather than species diversity of pollinators decreases community-wide trait matching and pollination function. *Functional Ecology*, 38, 1296–1308. https://doi.org/10.1111/1365-2435.14527

Traveset, A., Tur, C., Trøjelsgaard, K., Heleno, R., Castro-Urgal, R. & Olesen, J.M. (2016). Global patterns of mainland and insular pollination networks. *Global Ecology and Biogeography*, 25, 880–890. https://doi.org/10.1111/geb.12362

Bodbyl Roels, S.A. & Kelly, J.K. (2011). Rapid evolution caused by pollinator loss in *Mimulus guttatus*. *Evolution*, 65, 2541–2552. https://doi.org/10.1111/j.1558-5646.2011.01326.x

Gervasi, D.D.L. & Schiestl, F.P. (2017). Real-time divergent evolution in plants driven by pollinators. *Nature Communications*, 8, 14691. https://doi.org/10.1038/ncomms14691

Ashman, T.-L., Knight, T.M., Steets, J.A., Amarasekare, P., Burd, M., Campbell, D.R., Dudash, M.R., Johnston, M.O., Mazer, S.J., Mitchell, R.J., Morgan, M.T. & Wilson, W.G. (2004). Pollen limitation of plant reproduction: ecological and evolutionary causes and consequences. *Ecology*, 85, 2408–2421. https://doi.org/10.1890/03-8024

Knight, T.M., Steets, J.A., Vamosi, J.C., Mazer, S.J., Burd, M., Campbell, D.R., Dudash, M.R., Johnston, M.O., Mitchell, R.J. & Ashman, T.-L. (2005). Pollen limitation of plant reproduction: pattern and process. *Annual Review of Ecology, Evolution, and Systematics*, 36, 467–497. https://doi.org/10.1146/annurev.ecolsys.36.102403.115320

Knight, T.M., Steets, J.A. & Ashman, T.-L. (2006). A quantitative synthesis of pollen supplementation experiments highlights the contribution of resource reallocation to estimates of pollen limitation. *American Journal of Botany*, 93, 271–277. https://doi.org/10.3732/ajb.93.2.271

Van Etten, M.L., Tate, J.A., Anderson, S.H., Kelly, D., Ladley, J.J. & Merrett, M.F. (2015). The compounding effects of high pollen limitation, selfing rates and inbreeding depression leave a New Zealand tree with few viable offspring. *Annals of Botany*, 116, 409–418. https://doi.org/10.1093/aob/mcv118

Busch, J.W., Bodbyl-Roels, S., Tusuubira, S. & Kelly, J.K. (2022). Pollinator loss causes rapid adaptive evolution of selfing and dramatically reduces genome-wide genetic variability. *Evolution*, 76, 2130–2144. https://doi.org/10.1111/evo.14572

Sakai, S. (1995). Evolutionarily stable selfing rates of hermaphroditic plants in competing and delayed selfing modes with allocation to attractive structures. *Evolution*, 49, 557–564. https://doi.org/10.1111/j.1558-5646.1995.tb02287.x
