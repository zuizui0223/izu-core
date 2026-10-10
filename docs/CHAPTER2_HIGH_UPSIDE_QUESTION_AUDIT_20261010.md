# Chapter 2 high-upside research question audit — 2026-10-10

**Status: editorial/hypothesis audit, not a new biological result, preregistered test or endorsement of a journal's acceptance.** One eventual article, not separate floral-evolution and demographic manuscripts. Baseline journal ambition: Ecology Letters; higher-impact editorial consideration is CONDITIONAL on demonstrated new causal/ecological generality, not manuscript length or the number of repository experiments.

## 2026-10-10 executed Stage-1 original-genome review (PR #457, still exploratory)

We subsequently **re-downloaded and SHA-verified original 2026-10-06 evolutionary genotype checkpoints**, corresponding fixed/evolving source histories and their frozen reproductive source, for **64 paired visitor histories but only ONE of eight nested demographic repeats**. The near/far historical visitors were reconstructed exactly from their original RNG streams. This is stronger than the previously constructed fixed eight-plant fixtures, but it is **post-outcome replay of the original model**, not an independent natural experiment.

- Near t400, the evolved-assurance plant investment means were **0.0165–0.0440 lower** than the matched fixed-assurance means. Artificially restoring investment **within the SAME evolved genotype population** to the corresponding fixed-arm mean increased expected pollen transfer on average (E minus restored **−0.689 to −1.801** across settings), but only **33–37/64** individual visitor-history source states had a negative signed contrast.
- Unilaterally increasing one *native evolved adult* investment produced positive nonfocal viable maternal seed effects in **62–63/64 near history states**, under all four original mating-system settings; without visitors, there was no transfer/externality. This confirms a **conditional one-generation conspecific reproductive externality in actual evolving genomes**.
- Critically, **individual finite parental genetic contribution `W_i=.5F_i+.5P_i+S_i`** rather than own maternal seed alone must be used for an individual genetic-payoff sign. A stricter `W_i↓ / whole-group viable maternal seeds↑` conflict was present in only **12–23/64 near histories with at least one conflicting focal plant**, and **196–438/3072 correlated focal interventions per setting**. It was not a ubiquitous population-level sign disagreement.
- **Total viable maternal seeds were NOT consistently reduced** by source evolved lower investment: in the matched within-genome I restoration comparison, evolving minus restored viable seeds were **−0.243 delayed, +2.472 prior, +1.761 pollen-discount and +0.883 assurance-cost**. Thus delivered pollen loss can coexist with short-term viable seed compensation.
- The original K48 demographic response was almost **completely capacity saturated**: all near source expected viable seed means exceeded K; exact Poisson capped next-census mean differences after investment clamp were **less than 0.00025 plants** in all four settings. This is one-generation demography, not a long-horizon survival result.

**Decision:** Stage 1 supports pollen transfer and nonfocal benefit *components* but **fails to establish the full private-insurance → reduced collective reproductive fitness → extinction story**. In fact, seed compensation and demographic saturation block a generic harmful-persistence inference. **Keep Candidate B (confirmed evolutionary compression) as the one-paper Ecology Letters headline** until a genuinely independent, nonsaturated source-genetic-to-demography test is preregistered, executed and passes. Stage-1 raw source archive is retained with SHA and CI guards in [PR #457](https://github.com/zuizui0223/izu-core/pull/457); do not treat that exploratory Draft as a confirmed survival study.

## 2026-10-10 mechanism update: exact ovule-allocation versus pollen-receipt offset

Further original-genome source replay (PR #457; **64 previously exposed histories, 1 of 8 nested demographic repeats, near t400**) shows why the strong high-upside private-insurance → shared-pollen-loss → harmful-group-output inference is not yet supported. A within-evolving-genome **static investment clamp** was separated via a two-factor exact symmetric Shapley accounting identity into source maternal ovule-budget recovery and recipient-specific pollen receipt.

- Mean **ovule-resource contribution** to E versus E-investment-clamped viable maternal seed: **+1.772/+1.934/+2.968/+2.572** across delayed / prior / pollen-discount / assurance-cost settings.
- Mean **recipient-specific pollen receipt contribution**: **−2.015/+0.539/−1.208/−1.690** in the same order. Notably, *prior selfing* has an **average positive seed contribution from the changed distribution of pollen receipt (+0.539)** even though total delivered pollen decreases (−1.386). Total pollen volume therefore does not determine maternal seed output when plants are heterogeneous in ovule number, assurance and receipt.
- Mean **net group viable maternal seed change**: **−0.243/+2.472/+1.761/+0.883**, but all four pollen and resource component **post-hoc 64-history bootstrap95 intervals include zero**, and three of four net seed intervals also include zero. The narrowly positive unadjusted pollen-discount net interval [+0.042,+3.401] is **not a preregistered or multiplicity-corrected confirmation**.
- At native K48 all expected source near viable maternal seed totals exceed the demographic ceiling in all original histories, leaving near-zero **one-year capped expected recruitment** effects. No 80- or 1,000-update survival inference follows.

**Decision strengthened:** Do not promote universal decline in total population seed output or "evolutionary tragedy" as a Nature-level headline. The model actually provides both channels — resource compensation, pollen receipt redistribution and density buffering — so the next general mechanism question must ask **under which conditions a loss of indirect reproductive service survives compensation and density regulation to affect inherited population persistence**, rather than assume that it does. Design a prospectively registered *nonsaturated* same-genome intervention with externally justified demographic envelope and null cases; old source histories cannot be counted as new independent validation.

Source output SHA-256 `6fdd8ed45af9f7b9c65b513cb20fa1f3ba224519695ec37940421a7a6d60ae5e`, post-hoc history bootstrap SHA-256 `7c261e35e0dd5c496b488945a0e1edc3f9f57df3cf21a7afa7c4a053609f1d35`. Exact replay runner, descriptive receipt and original four-shard provenance in [PR #457](https://github.com/zuizui0223/izu-core/pull/457). The EL one-paper confirmed four-setting result is unaffected.

## 2026-10-10 completed six-budget one-step demographic falsifier (PR #457)

The original authenticated 256 evolved-diploid source states were evaluated under an explicitly bounded **six-level ovule budget multiplier** grid [0.025,0.05,0.125,0.25,0.5,1] with original fixed K48/B48 and unchanged visitors. In the source model's exact one-year N'=min(Poisson(bμ),K48) update, reducing the budget produces genuinely interior expected census sizes around b=.05 or b=.125, but **not a common negative group demographic effect**. At b=.125, mean E-vs-investment-clamped next-N contrasts are **−0.0304** delayed, **+0.3090** prior, **+0.2201** pollen-discount and **+0.1103** assurance-cost, and original mean E one-year occupancy stays ≥0.999995 in each setting. At b=.05 mean occupancy is still ≥0.99599. A 64-history bootstrap (one of eight original demographic repeats, exploratory and unadjusted across 24 setting-budget cells) does not authorize confirmatory promotion. The complete 1,536 source-derived one-year cells and exact Poisson formula are preserved in PR #457; no longitudinal trajectories or new independent histories were run.

**Interpretation:** Loosening the original density cap makes expected abundance responsive, but does **not** automatically connect a negative pollen-delivery source contrast to decreased collective viable seed, growth or persistence. Do **not** choose a now-observed 'favourable' low-budget cell and run more stochastic repeats as if the environmental hypothesis were frozen independently. Candidate A (evolutionary insurance undermines shared floral services with a population consequence) remains **unproven / currently NO-GO for an extinction headline**. The EL single-paper fallback B is not weakened.

## Select the question by what can be falsified

### Candidate A — high-upside, currently UNPROVEN

> **Can individually favoured reproductive insurance erode a shared pollen-transfer service, ultimately reducing the collective reproductive return or persistence of small plant populations?**

This is a mechanism of **private reproductive insurance versus shared effective pollen-transfer services**, *not* a claim that selfing directly causes pollinator extinction. In source Model 3, pollinator arrival/abundance is exogenous. At fixed floral investment and no pollen discount, changing assurance has **zero direct** effect on other mothers' outcross fertilization; with pollen discount, direct negative effects are possible. A mediated route would require that evolution of assurance **actually changes investment**, which **actually changes pollen receipt in neighbours**, which **actually changes demographic performance after density and genealogy are accounted for**. The original four-setting experiment establishes the first contrast, but NOT this entire mediation chain.

Grounded evidence:
- **Prospectively confirmed inherited evolution:** 64 new visitor histories × 8 demographic repeats × four reproductive settings × 1,000 updates. Keeping assurance fixed, far-minus-near investment is −0.302…−0.441; evolving assurance shrinks divergence +0.101…+0.220. Terminal occupancy = 1.0 in ALL main arms; that experiment has **no extinction contrast**.
- **Post-discovery pollen externality in source ledgers:** 14/384 investment states are finite focal β-negative / group viable-seed Γ-positive, and nonfocal expected viable seed gains are positive in the 128 visitor-present static source states. This does NOT establish evolutionary underinvestment or density-mediated persistence.
- **Essential falsifier:** Matching TOTAL DELIVERED pollen in 36 artificial source contexts eliminates virtually all collective seed differences (monomorphic exactly zero, mixed mean absolute 0.000904); composition affects receipt amount, while genetically mixed parental shares may still change. A large additional recipient-routing service at constant delivery is **not supported** by this test.
- **Separate demographic result:** imposed A-first/I-first expression schedules have a single preregistered positive K8−K48 moderation of selfed-seed viability sensitivity at fixed B48: +0.0077457 absolute occupancy probability (64 visitor history clusters; 95% [+0.0024972,+0.0130155]); timing of effects is inconclusive. These manipulations do NOT establish that naturally evolved assurance lowered group pollen services or changed persistence.
- **Feasibility NO-GO so far:** the native original investment commons persistence pilot saturates occupancy (floor or ceiling) near the key N6–9 conflict regime; the individual selection gradient changes sign at larger N. New confirmatory persistence runs would require a fresh, independently justified, nonsaturated demographic regime and a source-intervention falsifier, not more seeds in the same doomed regime.

**Novelty:** The combination of insurance-mediated evolutionary investment change with nonfocal pollen-transfer consequences and future demographic fitness could be important, but floral magnet/conspecific facilitation is known (Torices, Gómez & Pannell, Nature Communications 2018, DOI 10.1038/s41467-018-04378-3) and selfing-associated evolutionary suicide/Allee effects predate this work (Cheptou 2004, DOI 10.1111/j.0014-3820.2004.tb01615.x; see the review in Annals of Botany 2019). An effect only in one synthetic kernel would not by itself establish Nature Ecology & Evolution-level generality.

**Decision gate for promotion to ONE higher-ambition headline:**
1. Show a paired source-verified **evolving-assurance → inherited-investment → receipt/externality** counterfactual with *actual evolving* genomes and the same visitor history, not arm-mean mediation or imposed floral states. Predefine effect, matched partners and stage-specific readouts F/P/S; record direction and nulls.
2. Establish one independently predeclared **population-level** contrast of future occupancy/growth conditional on original genomic sources with matched K/B and a nonsaturated baseline; the contrast must **causally depend on the documented pollen-service/investment path**, not solely seed viability or schedule labels. Keep mortality, migration, demographic units and selection bias explicit.
3. Show stability or a clear boundary under at least two independently modified model environments / mating-system trade-offs, including cases where the effect SHOULD fail. Near pollen-saturation baseline is currently NOT achieved: source near F/O ~0.2197, far ~0.0103, and the bounded 16× input feasibility screen failed 90% admission. Do not describe that comparison as well-pollinated mainland versus island.
4. For a broadly explanatory island claim, add independent natural longitudinal pollen-deposition / parentage / inherited trait data, or genuinely external model families and species contexts. Chapter 1's contemporary broad trait associations cannot be substituted for historical process observations.

**Fail or null:** If reduced investment does not decrease effective nonfocal pollen service in actual evolving histories, or if such loss does not reduce viable offspring/occupancy after valid density controls, **reject A as the article's causal headline**. Retain the already confirmed investment-compression story and publish nulls transparently.

### Candidate B — supported / publishable baseline

> **Can mating-system evolution *erase the visible between-environment difference* in floral investment without being necessary for the original adaptive reduction?**

Four-setting prospective results directly support a **model-specific evolutionary compression / partial masking** of a fixed-assurance treatment contrast. The 78–90% additional near-side decline is **post-confirmation algebraic localization**, not a population-viability mediation percentage. The stronger near environment is far from saturated (fixed-state F/O ~22%); the observation is not proof that a fully pollinated mainland would respond similarly. The direct-cost assurance treatment has the smallest +0.1007 interaction and near-side −0.0789 decline. Cost-free delayed assurance is structurally favoured whenever unfertilized ovules remain.

**Prior art:** Allocation to attractive floral structures and delayed/competing selfing were modelled by Sakai (Evolution 1995, DOI 10.1111/j.1558-5646.1995.tb02287.x); phenotypic masking by genetic compensation/countergradient variation was articulated by Grether (American Naturalist 2005, DOI 10.1086/432023). What is potentially distinctive here is the **specific prospective no-necessity plus environment-interaction intervention in an explicit biparental pollen ledger**, not first discovery of masking as a biological principle.

**Remaining falsifiers to strengthen generality:** an independent, outcome-independent low→saturated pollen-exposure comparison that truly reaches the prespecified outcross coverage criterion; matched count vs functional visitor composition; full evolutionary follow-up with source-genetic retention. No outcome-driven rescue of the saturation failure.

**Route:** One Ecology Letters-centred original article if candidate A fails its substantive gate. Separate experimental-demographic occupancy belongs in a bounded figure/panel or SI, not as if it were the measured demographic consequence of B.

### Candidate C — possible broadly comparative problem, but not identified

> **Why are island reproductive functions recurrent while present-day floral phenotypes and evolutionary histories are heterogeneous?**

The current corrected Chapter 1 (source of truth: `zuizui0223/island/config/chapter1_submission_current.json`) supports self-compatibility enrichment with isolation in four geographic regions, region-contingent other traits, positive pollen limitation–isolation association in GloPL, and post-hoc functional compatibility. This is a **community-assembly cross-sectional association**, with many unresolved exact island-origin labels; it does not identify within-lineage evolutionary transitions. Model 3 provides conditional mechanism *possibilities*, but the historical Ch1 regional phenotype coefficients are **not quantitatively reproduced** by four previously audited synthetic emulator designs. A Ch1 + Ch2 juxtaposition therefore cannot become a proved cross-scale general law by integrating prose.

**Promotion gate:** state-matched historical natural island transitions or independent validated mechanistic cross-system predictions, discriminating colonization/establishment filtering, evolution after arrival, and post-establishment persistence. Failure to identify them keeps this as dissertation framing, not a stand-alone Nature-level central result.

## Ranking for the single-paper strategy

| Question | Current evidentiary maturity | Upside if falsifiers pass | Editorial risk |
|---|---|---|---|
| **A. Private assurance vs shared pollen-service feedback** | Strong source-level pieces, causal chain **missing** | Highest potential for broad eco-evolutionary mechanism beyond EL | Highest; known prior components, original survival pilot NO-GO |
| **B. Evolutionary compression/masking** | 4/4 prospectively confirmed in one model family | Clear Ecology Letters-style conceptual result; higher rank requires genuine externality/generalization | Moderate; countergradient and selfing–floral allocation established prior art |
| **C. Cross-scale island convergence vs contingency** | Ch1 macro associations + Model3 mechanisms, **not jointly fitted** | High if cross-scale evolutionary history becomes identified | Very high; natural temporal/genetic evidence missing |

**Single-main-goal decision:** Start with **A as a *research hypothesis* and one tightly scoped diagnostic gate**, while protecting B as the only established paper headline. Do not convert B's Ecology Letters route to Journal of Ecology just because an 80-update K study was appended. Do not turn a weak K interaction into a central conclusion of a high-impact article. A journal such as Nature Ecology & Evolution is an *aspiration conditional on new convincing results*, not a verified current destination; its scope spans individual/population/community and evolutionary processes, but the currently supported dataset is one biological model family.

## Journal formats are secondary to the claim

The current one-paper work draft contains **6,164 main-text words including Methods**, with a **235-word abstract**. The official *Ecology Letters* Letter caps are **5,000 main words** and **150 abstract words**. The current *Nature Ecology & Evolution* Article format allows **up to 3,500 main-text words excluding Methods**, **200 abstract words** and six display items. This particular version has about **4,253 words excluding Methods** (Introduction + Results + Discussion + Conclusion), so **neither target is format-ready**. Nature Ecology & Evolution's broad ecology/population/evolution scope fits the *question*, but a journal's scope is not evidence that this one-model study has the novelty or external validation required. Source: official Wiley Ecology Letters author guide and Springer Nature Ecology & Evolution content types, checked 2026-10-10.

We will not inflate the paper to integrate unsupported survival stories, nor cut the independent K nulls merely to improve narrative. The first scientific gate is whether Candidate A's missing **causal chain** can actually be identified. **If not, use Candidate B as the one-paper Ecology Letters claim and move unrelated demographic engineering detail to Supporting Information, clearly preserving provenance.**

## No-go rules

- Never claim that selfing reduces pollinator abundance: visitor arrival/loss is exogenous in source Model 3.
- Never claim that the A-first/I-first phenotype schedules are the spontaneous inherited mutation order.
- Never claim that the +0.007746 K moderation demonstrates evolving assurance → lost common pollen delivery → extinction.
- Never call source β−/Γ_seed+ an evolutionary suicide test; Γ_seed is collective viable seed, not growth, long-term occupancy or allele fitness.
- Never call 384 designed parameter cells, 1,533 correlated path-years, three within-model cohorts or 64 artificial visitor histories independent ecological systems.
- Never claim a globally new floral public-good principle or a universally new compensatory-evolution concept.
- If the high-ambition hypothesis fails, retain the pre-existing negative results and unaltered four-setting confirmatory results.

## Scientific sources / source ledgers

- Merged main: `docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md`, `data/results/chapter2_assurance_generality_20261006.json`, `docs/CHAPTER2_HIGH_REPLENISHMENT_POLLEN_LIMITATION_FEASIBILITY_20261010.md`.
- Deliberately exploratory unmerged #452: `docs/CHAPTER2_PR452_ONE_PAGE_SCIENTIFIC_DECISION_20261010.md`, `docs/CHAPTER2_DELIVERED_POLLEN_MATCHED_SOURCE_20261010.md`, `docs/CHAPTER2_INVESTMENT_COMMONS_PERSISTENCE_FEASIBILITY_20261010.md`.
- Merged capacity manuscript as evidence archive: `docs/CHAPTER2_CAPACITY_PERSISTENCE_COMPANION_MANUSCRIPT_20261010.md`.
- Independent external prior literature: Sakai 1995 Evolution; Torices et al. 2018 Nature Communications; Cheptou 2004 Evolution; Grether 2005 American Naturalist; Acoca-Pidolle et al. 2024 New Phytologist.
