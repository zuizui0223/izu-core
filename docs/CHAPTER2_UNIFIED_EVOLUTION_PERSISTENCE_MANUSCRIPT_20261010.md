# Floral-investment divergence and demographic persistence respond differently to reproductive assurance under pollinator limitation

**Article type:** Ecology Letters Letter — one unified original research manuscript (word limits met; data deposit pending)  
**Target journal:** Ecology Letters (Letter) first; a higher-impact ecology/evolution journal is conditional on new causal validation, not on reframing existing data  
**Scope:** EL-format draft ~3310-word main text and 142-word abstract; four main figures; science/data gates remain  
**Status:** one unified scientific working draft, not submitted or peer reviewed; two original drafts retained as source provenance  
**Model family:** one explicit Model 3; two separate interventions with distinct inference units and horizons  
**Figures:** 4 main evidence figures; older deterministic figure retained as supplement  
**Tables:** numerical effect table in supporting documents; cohort rank retained

## Abstract

Pollinator limitation often coincides with greater reproductive assurance and reduced floral attraction, but this association does not establish their causal order. In a genetically explicit plant–pollinator model, a preregistered experiment (64 independent visitor histories; four reproductive settings) showed that floral investment declined with lower visitor replenishment even when assurance evolution was prevented. Allowing assurance to evolve instead compressed environmental investment differences (+0.101 to +0.220), chiefly through additional decline in the higher-replenishment population. Both environments remained pollen-limited. A distinct finite-population experiment found modest demographic-capacity moderation of occupancy sensitivity to imposed reproductive-expression order and viable selfed seeds (+0.00775; 95% history-bootstrap interval +0.00250 to +0.01302). This imposed schedule did not test naturally arising mutation order or establish a pathway from evolved floral investment to extinction. Reproductive assurance can therefore alter divergence without being required for floral reduction; its demographic consequences depend on additional, unresolved mechanisms.

## Keywords

island ecology; floral evolution; reproductive assurance; pollinator limitation; plant–pollinator interactions; mating systems; demographic stochasticity; pollen delivery; finite populations; genetic inheritance

# Introduction

Pollinator loss may favour autonomous reproduction and reduced investment in floral attraction. A familiar explanation is serial: pollinator limitation first selects for reproductive assurance, after which selfing relaxes selection on structures serving outcrossing. Theory and experimental evolution support interactions between mating systems and floral display (Sakai 1995; Bodbyl Roels & Kelly 2011; Sicard et al. 2011; Gervasi & Schiestl 2017). Yet neither correlation nor temporal order proves that assurance evolution is *required* for floral reduction.

An alternative is parallel selection. Pollinator limitation may directly lower maternal and paternal outcross returns to attraction while independently favouring reproductive insurance. If attraction already has little value when pollination is severely limited, increasing assurance might displace comparatively little remaining outcross return there. The same assurance evolution could reduce floral investment more strongly where pollen-dependent benefits remain available, thereby **compressing** rather than widening environmental divergence.

This question matters for island ecology. Island floras commonly include self-compatible species, yet their floral phenotypes and pollination networks do not respond uniformly to isolation (Traveset et al. 2016; Grossenbacher et al. 2017; Hetherington-Rauth & Johnson 2020; Hiraiwa & Ushimaru 2017, 2024). Contemporary trait patterns may also reflect colonization, establishment and persistence filtering rather than within-lineage evolutionary change alone.

A separate issue is demographic: an evolved reproductive phenotype may increase expected seeds without guaranteeing offspring recruitment or local population persistence. We therefore ask two linked, deliberately non-equivalent questions in one explicit plant–pollinator model. **First**, is assurance evolution necessary for reduced floral investment under visitor limitation, and does allowing assurance evolution increase or decrease investment divergence? **Second**, can viable selfed-seed output and finite demographic capacity modify the occupancy consequences of *experimentally assigned* assurance-first versus investment-first expression? The first uses inherited evolution over 1,000 updates; the second uses distinct cohorts and controlled 80-update schedules. Their juxtaposition is **not a natural mediation analysis** of evolved floral traits on extinction.

# Materials and Methods

## Reproductive model and invasion accounting

Model 3 follows a finite population of diploid plants with inherited visitor-matching, floral-investment and reproductive-assurance loci. Visitor functional types arrive and disappear stochastically; their optimum, breadth and effectiveness determine pollen removal and receipt. Floral investment increases affinity and pollen export but reduces the available ovule budget. Outcross fertilization saturates with pollen receipt; autonomous selfing can occur before or after outcrossing, and selfed offspring experience inbreeding depression. Separate maternal and paternal gametes, Mendelian segregation, adult survival, density-limited recruitment and seed immigration govern finite inheritance.

We contrasted higher ('near') with lower ('far') visitor replenishment while holding plant capacity and the other ecological rules fixed. These labels are **synthetic replenishment conditions, not mainland/island distances or pollen-sufficiency classes**. Both environments began with the same visitor source state. The four predefined reproductive settings were cost-free delayed selfing, prior selfing, pollen discount (lost male outcross export as assurance increases) and a direct assurance allocation cost. Cost-free delayed assurance is structurally beneficial if unfilled ovules and viable selfed offspring remain; it is a permissive control rather than an equally demanding test of the direct costs of assurance.

For a rare mutant in a held-fixed resident pollen environment, expected parental-genome contribution is `W=F/2+P/2+S`: maternal outcross `F`, paternal outcross `P`, and viable selfing `S`. We used corrected rare-mutant rather than whole-population investment derivatives and partitioned selection into maternal outcross, paternal export, selfing displacement and ovule allocation cost. Fixed-state local gradients are mechanistic diagnostics, not estimators of dynamic genetic mediation.

## Preregistered evolutionary intervention

The primary frozen experiment used **64 independent new visitor histories**, eight nested demographic repeats per history, 1,000 reproductive updates, near/far replenishment, fixed/evolving assurance and all four reproductive settings: **8,192 trajectories** under positive mutation probability 0.01. Plants began with the identical 48-founder matching/investment distribution, and both assurance alleles were set to 0.5. In fixed mode, assurance capacity remained 0.5 while matching and investment inherited and mutated; in evolving mode assurance also inherited and mutated. Blocking *capacity evolution* does **not** block realized selfing.

The two preregistered estimands were (i) fixed-assurance terminal far-minus-near investment and (ii) the matched four-cell interaction `[(far−near)_evolving−(far−near)_fixed]`, using demographic repeats occupied in all four cells. Each setting passed only if the first history-bootstrap 95% interval was wholly negative and the second wholly positive; the global rule required all four settings, at least 60/64 admissible visitor histories and 90% occupancy per arm. The eight repeats were averaged *within* visitor histories, which were the independent resampling units. Extinct phenotypes were missing, never zero. A zero-mutation control required fixed and evolving matched traces to be exactly identical: 128/128 pairs passed.

After confirmation, we decomposed the interaction algebraically into the evolving-minus-fixed near and far effects, without claiming natural mediation fractions. At snapshot 400, a separate matched-history fixed-resident diagnostic changed assurance from 0.25 to 0.75 and recomputed the four investment-gradient components. A distinct frozen temporal-order cohort defined trait change as a founder-relative threshold crossing sustained 20 updates; temporal precedence was not treated as a necessity test. Separate fixed-state assays compared fractional pollen deficit with absolute viable maternal seeds.

## Independent finite-population experiment

The demographic study uses authenticated diploid states after 400 prehistory updates, followed by **80 updates** under separately assigned, equal-cumulative-dose *phenotypic expression schedules*: assurance first (A-first) or investment first (I-first). These schedules do **not** impose the sequence in which inherited alleles arose. Each future branch records whether any plants remain. A postzygotic intervention halves viable selfed-seed contribution while leaving outcross production unchanged at the intervention point.

The original population capacity parameter `K` also appeared in a pollen-recipient background denominator, confounding demographic space with pollination. An independently checked control therefore replaced that denominator by a distinct fixed pollen-background `B`, allowing `K8` versus `K48` comparisons at **B48** and identical up-to-eight diploid founder genotypes. Define `D(K,B,g)` as the A-first minus I-first 80-update occupancy contrast under viable-selfed-seed treatment `g`; `tau(K,B)=D(K,B,baseline)−D(K,B,half-selfed)`. The registered primary estimand was `tau(K8,B48)−tau(K48,B48)`.

A separately preregistered cohort used 64 previously unused visitor-history identities, with branches and nested repeats averaged within history, and 9,999 paired history-bootstrap draws. Support required an absolute effect at least 0.005 and a two-sided percentile 95% interval excluding zero. The earlier inconclusive K or B primaries, near/far assigned-order equivalence, resource-window failure and later inconclusive early-versus-late timing test were retained. Two other cohorts' similar K contrasts are **secondary/descriptive**, not additional confirmatory successes or a pooled meta-analysis. The demographic experiments share a reproductive framework but differ in endpoints, intervention assignments, sample identities and some K/B biology from the 1,000-update evolutionary experiment. Neither identifies an evolutionary-investment-to-persistence mediator. The original four-setting campaign had terminal occupancy 1.0 in every arm.

# Results

## Visitor limitation reduces the reproductive return to attraction before plant evolution

At the same fixed plant state, low visitor replenishment sharply reduced the return to floral investment (Fig. 1). In the delayed-selfing setting at snapshot 400, the total investment-contribution derivative changed from +0.579 under near exposure to −0.700 under far exposure. The outcross contribution fell from +1.652 to +0.085, whereas the viable-selfed component partly offset rather than generated the decline. The intrinsic investment-cost coefficient was unchanged across environments. Thus visitor limitation can make reduced attraction favourable before any evolution of reproductive assurance.

## Assurance evolution is not required for investment decline

The prospective four-setting test passed its frozen non-necessity criterion in every setting (Fig. 2A). For the cost-free delayed-selfing control, direct assurance benefits are structurally positive whenever ovules remain unfilled; passing this control does not provide the same test of assurance trade-offs as the cost, prior-selfing and pollen-discount regimes. With assurance held fixed at 0.5, far-minus-near investment was −0.4413 [−0.4564, −0.4262] under delayed control, −0.3018 [−0.3172, −0.2866] under prior selfing, −0.3305 [−0.3461, −0.3151] with pollen discount and −0.4337 [−0.4501, −0.4171] with direct assurance cost. All four near/far arms retained terminal occupancy 1.0 and all 64 histories were eligible.

Reduced investment under low replenishment therefore did not require assurance-capacity evolution under any of the four declared reproductive rules. Because fixed capacity still permits realized selfing, this result excludes a requirement for assurance evolution, not all reproductive consequences of selfing.

## Assurance evolution consistently compresses environmental divergence

Allowing assurance to evolve reduced the magnitude of the near–far investment contrast in all four settings (Fig. 2B). These settings test a broader range of **investment responses** to assurance evolution, not four equally discriminating tests of whether assurance can invade: cost-free delayed selfing already favours assurance when ovules remain unfilled. Evolving-minus-fixed interactions were +0.1605 [0.1418, 0.1789] under delayed control, +0.2200 [0.2025, 0.2383] under prior selfing, +0.1915 [0.1762, 0.2069] with pollen discount and +0.1007 [0.0842, 0.1177] with assurance cost. All four settings therefore passed the preregistered attenuation criterion.

The arm decomposition showed that this attenuation was not primarily rescue of far-side investment (Fig. 2C). Relative to fixed assurance, allowing assurance to evolve changed near-side investment by −0.1253 [−0.1395, −0.1112], −0.1985 [−0.2137, −0.1838], −0.1699 [−0.1831, −0.1563] and −0.0789 [−0.0931, −0.0646] across delayed control, prior selfing, pollen discount and assurance cost. Far-side effects were much smaller and positive: +0.0352 [0.0233, 0.0471], +0.0215 [0.0116, 0.0315], +0.0216 [0.0110, 0.0327] and +0.0218 [0.0120, 0.0312]. Consequently, 78.1%, 90.2%, 88.7% and 78.3% of the interaction, respectively, was localized to additional investment decline in the high-replenishment arm.

## The direct selection effect is stronger where outcross returns remain available

The corrected rare-mutant diagnostic resolved the same environmental asymmetry at a fixed plant state (Fig. 2D). The near label denotes **higher visitor replenishment**, not pollen sufficiency. The independent fixed-plant snapshot-400 assay found mean raw deficit 0.3901 near versus 0.4948 far, and mean viable-seed deficit 0.5852 near versus 0.7423 far, in its delayed-timing assurance-cost setting across 64 visitor histories and fixed 48-plant states. Here the *raw* deficit is measured **after** autonomous selfing: with delayed assurance fixed at a=0.5, the source equation is d_raw=(1−a)(1−F/O), so mean outcross fertilization fractions F/O are approximately 0.2197 near and 0.0103 far. The 39% near deficit is NOT a claim that only 39% of ovules remain without outcross pollen. These fixed-state fractions are not terminal unfertilized-ovule fractions in evolved populations. Increasing assurance from 0.25 to 0.75 made the investment gradient more negative in both environments, but the effect was much stronger near than far. At snapshot 400, the near-minus-far assurance effect on the investment gradient was −0.3794 [−0.4376, −0.3170] under delayed control, −0.5231 [−0.6041, −0.4361] under prior selfing, −0.4661 [−0.5389, −0.3876] with pollen discount and −0.3794 [−0.4369, −0.3177] with assurance cost.

Maternal outcross and paternal pollen-export components supplied most of these differences. In delayed control and assurance cost, their near-minus-far contributions were −0.125 and −0.135, respectively; under prior selfing they were −0.214 and −0.235; with pollen discount they were −0.179 and −0.198. Selfing-displacement and allocation-cost components acted in the same direction, except that selfing displacement is structurally zero under prior selfing.

Under low replenishment, attraction-dependent outcross return was already small. Increasing assurance therefore removed relatively little additional attraction value. Under high replenishment, substantial maternal and paternal return remained, so the same assurance increase more strongly reduced selection for investment.

## Temporal order is setting-specific and does not establish necessity

The independent temporal-order replication recovered an assurance-first sequence in the delayed-selfing, direct-cost setting: 51 of 64 histories were assurance-first at the primary 0.05 threshold and 13 were near-simultaneous (proportion 0.797; 95% history-bootstrap interval 0.688–0.891). The same criterion did not generalize to prior selfing, where 30 of 64 histories were assurance-first and the interval spanned 0.5.

Thus assurance can change before investment, but this sequence is narrower than the four-setting non-necessity and attenuation results. Temporal precedence is neither universal nor required for the investment response.

## Pollen-deficit and viable-output responses are not equivalent

The reproductive-output intervention showed that apparent compensation in a fractional pollen-deficit metric need not correspond to higher viable offspring production (Fig. 3). In the delayed/far assay at snapshot 400, increasing investment from 0.25 to 0.75 at assurance 0.5 reduced fractional viable pollen deficit by 0.0104 while reducing viable maternal offspring by 15.72 per 48 plants. Reproductive assurance, pollen deficit and absolute viable production are therefore distinct quantities.

Finite-population and deterministic comparisons further delimit realization rather than the primary causal result (Supplementary Fig. S1). They show that expected inherited response and finite genetic realization need not coincide exactly; they do not alter the four-setting intervention conclusion.

## Conditional demographic consequences of assigned reproductive expression history

The experiments here are separate from the evolving-assurance trajectories above. In particular, 'assurance first' is imposed temporarily as an expression schedule; it does not mean spontaneous assurance alleles mutated or spread first. The analysis retains all failed and inconclusive preregistered primaries as well as the one supported capacity-moderation primary (Fig. 4).

### 1. Order effects were small and not specific to geographic visitor history

The original assigned-expression-order near/far difference-in-differences passed the preregistered **practical-equivalence** bound ±0.05. The independently predeclared 3/4-ovule-budget-window follow-up **failed**. Thus the original prediction of a distinctive far-environment or resource-window rescue effect was not supported. A small absolute A-first-minus-I-first occupancy advantage still appeared in some bottlenecked conditions, but this is not a universal precedence effect and is not the original positive primary.

### 2. A controlled selfed-seed intervention changed the small schedule advantage

In an eight-founder/capacity-eight stress regime, a predeclared postzygotic intervention halving viable selfed-seed contribution reduced the A-first-minus-I-first occupancy difference from **+0.01209** at baseline to **+0.00394**. Sensitivity was **+0.008145**, 95% history-bootstrap **[+0.003708,+0.012773]**, satisfying its original frozen threshold. A matched outcross-seed viability contrast did not resolve a nonzero effect. The postzygotic manipulation identifies a **controlled response to viable selfed seeds**, not natural genetic mediation.

### 3. The first capacity contrasts were either confounded or inconclusive

Comparing F8/K8 with a full-founding-population/K48 regime suggested a positive moderator, but that was **post-outcome exploratory** and simultaneously changed founding abundance, genomic sampling, demographic K and the pollen-delivery denominator. A new independently sampled matched-founder experiment changed K8 to K48 with eight founder genomes held fixed. Its registered primary sensitivity contrast was **+0.001848**, 95% **[−0.003458,+0.007337]**, **inconclusive**. A full subsequent two-lever experiment separated K and B; its **preregistered primary** B8 versus B48 at fixed K8 was **−0.001753**, 95% **[−0.006334,+0.002872]**, also **inconclusive**. Its K effect at fixed B48 was positive, but remained **secondary/descriptive** and motivated the next study.

### 4. An independent predeclared test supported demographic K moderation at fixed B48

With fresh visitor histories, matched founding genotypes and an explicit constant pollen-background denominator, the registered K8–K48 contrast was:

| Registered fixed-B48 quantity | Occupancy effect | 95% paired history bootstrap |
|---|---:|---:|
| `tau(K8,B48)` | +0.009977 | [+0.006340,+0.013613] |
| `tau(K48,B48)` | +0.002231 | [−0.001599,+0.006151] |
| **Primary: K8 minus K48** | **+0.007746** | **[+0.002497,+0.013015]** |

The registered mean exceeds 0.005 and the entire interval is positive; **43 of 64 history clusters** contributed positive contrasts. Its machine verdict is `supported_controlled_demographic_K_moderation_at_fixed_B48`. This is **about 0.775 occupancy percentage points** of interaction sensitivity, not the overall effect of K on persistence.

**Figure 4:** [Original K-at-B48 cohort estimates and unpooled intervals](../figures/chapter2_k_at_B48_three_cohort_original_intervals_20261010.svg), generated without refitting by `scripts/render_chapter2_capacity_companion_evidence_figure.py`. Its square denotes the *one* preregistered primary; circles denote descriptive secondaries.

Two other **independently generated** 64-history cohorts had directionally concordant estimates of this same full-period contrast: **+0.013430** (four-arm K×B cohort) and **+0.008580** (timed-viability cohort). Both were *secondary descriptive* measures selected in experiments with **different registered primaries**. Across the three original JSONs the unweighted numerical mean **+0.009919** is **descriptive only**; no pooled interval, formal equivalence or threefold confirmatory success is claimed. See `docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md` and Figure 4.

### 5. A later prospective timing contrast did not resolve early versus late importance

After exploratory extinction-time diagnostics suggested later response, an independent **four-gate** experiment used another unused 64 histories and 229,376 futures. Selfed viable seeds were halved during updates **0–39**, **40–79**, or **0–79**, with an unchanged baseline. Its registered primary, the **difference between late-only and early-only K moderation**, was **−0.002965**, history-bootstrap **[−0.007263,+0.001317]**: **inconclusive**, neither nonzero support nor practical equivalence. The full-period K contrast (+0.008580) is a *descriptive secondary*, not a successful test of the timing hypothesis. Different interval crossings for early and late alone cannot identify when the causal mechanism acts.

# Discussion

Pollinator limitation did not need to change reproductive-assurance capacity before floral investment could decline. Under fixed assurance, reduced visitor replenishment lowered the return to attraction, and inherited investment fell across all four preregistered reproductive settings. But allowing assurance to evolve did not magnify that reduction in the more limited environment. Instead, it **compressed** the difference between environments, predominantly by reducing investment in the higher-replenishment population. This separates a mechanism's necessity for floral decline from its effect on the amount of observable divergence.

The asymmetry is consistent with the corrected maternal/paternal invasion accounting. Severe visitor limitation removes much of the opportunity for outcross mating before assurance changes. Where some outcross returns remain, assurance evolution has more investment value to displace. Crucially, the higher-replenishment arm was **not well pollinated**: a separate static, fixed-plant snapshot-400 assay estimated outcross fertilization of about 22% of ovules there, compared with about 1% in the lower-replenishment arm. Its 39% 'raw deficit' is the shortfall **after** autonomous selfing, not the fraction lacking outcross pollen. Even an exploratory 16-fold pollen-budget feasibility test failed the defined near-sufficiency criterion. We therefore cannot generalize this interaction to a saturated mainland comparator.

The four settings are mechanistically distinct but not four equally difficult demonstrations that assurance itself is favoured. Delayed selfing without cost or pollen discount has a structural assurance advantage whenever ovules remain unfilled and viable selfing is possible. The assurance-cost setting was more discriminating and had the smallest attenuation (+0.1007). Nor does blocking assurance evolution remove the possibility of *realized* autonomous selfing. The 78–90% near-side localization is a **post-confirmation arithmetic decomposition**, not a direct/indirect causal fraction.

Demographic regulation provides an additional qualification, not an explanation that can be read directly from trait divergence. In the separate assigned-order experiment, the original geographic-order contrast was practically equivalent within its registered margin, and the restricted-resource hypothesis failed. Only after separately controlling pollen-background dilution did an independent registered study detect a small K-dependent moderation of the selfed-seed viability sensitivity of the order contrast. This is an interaction of **imposed expression history, engineered seed viability and demographic capacity**, not proof that autonomous evolution follows the prescribed order, that floral reduction causes extinction, or that smaller islands uniformly benefit from insurance. The later test did not resolve whether early versus late viable selfed-seed availability was responsible.

A complementary mechanism remains of interest but is not established as a survival pathway. In post-discovery source-ledger experiments, increasing a focal plant's investment sometimes benefited other mothers' viable seeds even when its own finite parental genetic return was negative. Replaying authentic evolved diploid source states confirmed a nonfocal pollen-mediated benefit, yet whole-group seed effects were not consistently positive. A static two-factor maternal-seed accounting showed that floral-investment changes simultaneously alter **recipient-specific pollen receipt and ovule allocation**; resource savings can offset reduced pollen service. These exploratory history-bootstrap intervals often spanned zero. Moreover, the original 48-plant demographic regime was nearly saturated with viable seeds, so one-generation expected census differences were negligible. These results motivate a sharper future test of whether an evolved loss of shared pollen-transfer benefits can survive resource compensation and density regulation; **we do not identify a causal chain** from evolving assurance through floral investment to lower population persistence.

Our results concern one explicitly specified model class, not a measured historical transition on real islands. Visitor arrival is imposed externally, not caused by floral-investment evolution. The original evolutionary contrast is a **finite 1,000-update outcome**, not an established long-term stationary state; a separate deterministic long-horizon diagnostic failed stationarity but did not re-test the four-setting attenuation. Island trait associations may reflect lineage sorting, establishment, local evolution and persistence, which these experimental manipulations cannot partition historically. An ecological test of the broader hypothesis would need matched natural pollination and genetic-parentage data, or genuinely independent evolutionary and demographic models with falsifying regimes rather than further outcome-selected parameter tuning.

# Conclusion

Reproductive assurance evolution was not necessary for floral-investment decline under reduced visitor replenishment, but its evolution compressed investment divergence across four prespecified mating-system settings. A separate controlled demographic experiment identified a small, capacity-dependent sensitivity to viable selfed offspring and assigned expression order, without demonstrating that naturally evolved investment affects extinction. These results distinguish evolutionary selection, observed trait divergence and finite-population persistence, rather than treating them as a single serial island-syndrome pathway.

# Primary figure assembly and captions

**Figure 1. Visitor limitation reduces the reproductive return to attraction before plant evolution.** At the same fixed plant state and assurance capacity 0.5, near and far visitor exposures are compared for outcross, viable-selfed and total contribution slopes. In the delayed setting at snapshot 400, total investment contribution changes from +0.579 to −0.700 as the outcross component falls from +1.652 to +0.085; the viable-selfed component partly offsets the decline. Points are means across 64 paired visitor histories. These are reproductive-return diagnostics before plant evolution.

**Figure 2. Reproductive assurance compresses floral-investment divergence without causing the initial decline.** Panel A shows fixed-assurance far-minus-near investment contrasts in all four reproductive settings; every interval remains below zero. Panel B shows positive evolving-minus-fixed isolation interactions in all four settings. Panel C decomposes the interactions on common four-cell replicates: 78–90% of attenuation arises from additional investment decline in the near/high-replenishment arm, with smaller far-side relief. Panel D shows the corrected rare-mutant mechanism at snapshot 400: increasing assurance from 0.25 to 0.75 weakens investment selection much more near than far, with maternal outcross and paternal pollen-export components contributing most of the difference. Panels A–C use 64 independent visitor histories with eight nested demographic repeats; Panel D is a local selection diagnostic, not a dynamic mediation estimate.

**Figure 3. Lower pollen deficit need not mean greater viable reproduction.** Whole-population investment interventions compare change in fractional viable pollen deficit with change in viable maternal offspring. In the delayed/far comparison, increasing investment from 0.25 to 0.75 at assurance 0.5 reduces fractional viable deficit by 0.0104 while reducing viable maternal offspring by 15.72 per 48 plants. These are fixed-trait reproductive assays, not evolutionary trajectories.

**Figure 4. Small demographic-capacity modulation of the reproductive-expression-order occupancy contrast.** The complete original source-locked forest plot at `figures/chapter2_k_at_B48_three_cohort_original_intervals_20261010.svg` shows three separately generated 64-history cohort estimates of `tau(K8,B48) - tau(K48,B48)`, where `tau` is the baseline versus halved-viable-selfed-seed effect on the imposed A-first minus I-first occupancy contrast after 80 updates. The **square** denotes the only prospectively preregistered supported primary, +0.0077457 [95% history-bootstrap +0.0024972,+0.0130155]; the two **circles** are post-outcome secondary/descriptive estimates, +0.0134300 and +0.0085803. No pooled uncertainty, natural evolutionary-order effect or real-island extinction rate is inferred.

**Supplementary Figure S1. Conditional finite-genetic realization.** The former Figure 4 is retained as supporting evidence that a deterministic density closure is not the exact stochastic mean of the finite ABM; its provenance and original interpretation remain in the archived 2026-10-06 Letter manuscript. It is not a fifth independent study.

# Data accessibility

The original designs, validated machine-readouts, source-code hashes and workflow provenance for the floral-investment study and the distinct capacity–persistence cohorts are retained separately in the project repository. For the latter, 521 original biological-trajectory ZIP archives from four cohorts were backed up in unpublished draft GitHub Releases with SHA-256 verification. Those private drafts and expiring Actions artifacts are **not** an externally citable research-data deposit. A DOI-backed external archive with licensing and successful independent download/verification remains outstanding under Issue #436. This unified working manuscript is not yet submitted.

## Evidence hierarchy and study-origin record

The four-setting 1,000-update intervention and its prespecified all-four passing rule are the **primary evolutionary result**. The high- versus low-replenishment gradient decomposition and fixed-plant pollen-saturation assessment are separately specified post-confirmation or earlier fixed-state supporting diagnostics. The cost-free delayed-selfing control is structurally favourable to assurance when viable selfing and unfilled ovules exist; the smallest interaction occurs with direct assurance cost (+0.1007).

The demographic experiment is a **second, nonexchangeable question within the same paper**, with its *own* registered primary and multiple negative or inconclusive antecedents: original near/far order DID practically equivalent; independent resource-window hypothesis failed; fixed-founder and B-at-K8 primary contrasts inconclusive; newly registered fixed-B48 K8-vs-K48 contrast +0.0077457 supported; original early-versus-late primary inconclusive. The three independent source cohorts are not three confirmatory model architectures. Original K/B intervention replaces one recipient pollen-dilution denominator solely for the demographic control; this is not the same exact frozen biology as the canonical four-setting campaign for all K/B comparisons.

No additional biological trajectory, bootstrap, prospective hypothesis or causal mediation has been generated to assemble this unified article. The earlier `docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md` and `docs/CHAPTER2_CAPACITY_PERSISTENCE_COMPANION_MANUSCRIPT_20261010.md` remain **source-provenance manuscripts**, not separate active submissions under the one-paper route. The exploratory PR #452 and the one-step Q3 PR #455 are excluded from the confirmed manuscript results; they remain research directions and methodological sensitivity, respectively.

# References

Ashman, T.-L., Knight, T.M., Steets, J.A., Amarasekare, P., Burd, M., Campbell, D.R., Dudash, M.R., Johnston, M.O., Mazer, S.J., Mitchell, R.J., Morgan, M.T. & Wilson, W.G. (2004). Pollen limitation of plant reproduction: ecological and evolutionary causes and consequences. *Ecology*, 85, 2408–2421. https://doi.org/10.1890/03-8024

Bodbyl Roels, S.A. & Kelly, J.K. (2011). Rapid evolution caused by pollinator loss in *Mimulus guttatus*. *Evolution*, 65, 2541–2552. https://doi.org/10.1111/j.1558-5646.2011.01326.x

Busch, J.W., Bodbyl-Roels, S., Tusuubira, S. & Kelly, J.K. (2022). Pollinator loss causes rapid adaptive evolution of selfing and dramatically reduces genome-wide genetic variability. *Evolution*, 76, 2130–2144. https://doi.org/10.1111/evo.14572

Gervasi, D.D.L. & Schiestl, F.P. (2017). Real-time divergent evolution in plants driven by pollinators. *Nature Communications*, 8, 14691. https://doi.org/10.1038/ncomms14691

Grossenbacher, D.L., Brandvain, Y., Auld, J.R., Burd, M., Cheptou, P.-O., Conner, J.K., Grant, A.G., Hovick, S.M., Pannell, J.R., Pauw, A., Petanidou, T., Randle, A.M., Rubio de Casas, R., Vamosi, J.C., Winn, A.A., Igić, B., Busch, J.W., Kalisz, S. & Goldberg, E.E. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. https://doi.org/10.1111/nph.14534

Hetherington-Rauth, M.C. & Johnson, M.T.J. (2020). Floral trait evolution of angiosperms on Pacific islands. *The American Naturalist*, 196, 87–100. https://doi.org/10.1086/709018

Hiraiwa, M.K. & Ushimaru, A. (2017). Low functional diversity promotes niche changes in natural island pollinator communities. *Proceedings of the Royal Society B*, 284, 20162218. https://doi.org/10.1098/rspb.2016.2218

Hiraiwa, M.K. & Ushimaru, A. (2024). Loss of functional diversity rather than species diversity of pollinators decreases community-wide trait matching and pollination function. *Functional Ecology*, 38, 1296–1308. https://doi.org/10.1111/1365-2435.14527

Knight, T.M., Steets, J.A., Vamosi, J.C., Mazer, S.J., Burd, M., Campbell, D.R., Dudash, M.R., Johnston, M.O., Mitchell, R.J. & Ashman, T.-L. (2005). Pollen limitation of plant reproduction: pattern and process. *Annual Review of Ecology, Evolution, and Systematics*, 36, 467–497. https://doi.org/10.1146/annurev.ecolsys.36.102403.115320

Knight, T.M., Steets, J.A. & Ashman, T.-L. (2006). A quantitative synthesis of pollen supplementation experiments highlights the contribution of resource reallocation to estimates of pollen limitation. *American Journal of Botany*, 93, 271–277. https://doi.org/10.3732/ajb.93.2.271

Sakai, S. (1995). Evolutionarily stable selfing rates of hermaphroditic plants in competing and delayed selfing modes with allocation to attractive structures. *Evolution*, 49, 557–564. https://doi.org/10.1111/j.1558-5646.1995.tb02287.x

Sicard, A., Stacey, N., Hermann, K., Dessoly, J., Neuffer, B., Bäurle, I. & Lenhard, M. (2011). Genetics, evolution, and adaptive significance of the selfing syndrome in the genus *Capsella*. *The Plant Cell*, 23, 3156–3171. https://doi.org/10.1105/tpc.111.088237

Traveset, A., Tur, C., Trøjelsgaard, K., Heleno, R., Castro-Urgal, R. & Olesen, J.M. (2016). Global patterns of mainland and insular pollination networks. *Global Ecology and Biogeography*, 25, 880–890. https://doi.org/10.1111/geb.12362

