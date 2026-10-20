# N5 higher-impact theory proposal — scientific corrections before any new simulation

**Scientific review, 2026-10-19, PR #609.** This is a **read-only, source-grounded** derivation and a proposal for future independently registered studies. **NO new biological simulations**, no changes to source G/S registration, no claimed new confidence intervals, no added sample and no assertion of natural-island causation or a universal transition.

## Short verdict / 最も重要な判断

N5 is the strongest possible bridge from the registered Q3 high-I support result to Q4 persistence. But the proposed universal statement **“assurance ALWAYS harms floral genetic material, and protects evolvability only by avoiding extinction” is NOT shown by the present data**. In the harsh B4.5 arm, the fraction retaining founder-target I support **among survivors** is *higher* under the evolving-A policy (9,245 / 25,118 = **36.8063%**) than under fixed A (140 / 1,385 = **10.1083%**). At B8, the corresponding fractions are 37.5% versus 45.8281%, respectively. Survivor conditioning is post-treatment selection: the B4.5 comparison is NOT the causal direct effect on inherited allele maintenance. However, treating the genetic mechanism as uniformly deleterious is not justified, either.

Likewise, 25,600 crossed founder×visitor cells are **160 independent founder sources and 160 independent visitor-history sources**, not 25,600 sampled independent island systems. Claim rankings, source checks and original B8 G (+8.328125 pp; 97.5% adjusted interval [+6.69391,+9.96234]) and B4.5-vs-B8 S (+92.707031 pp; [+92.04959,+93.36447]) remain frozen.

## Exact first-competing-event audit already available (no simulation)

Source: [registered confirm160 source readout](audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json). Under **no I mutation or immigration**, a living population can exit the state of being genetically capable of reaching the original high-I allele target through either **G**: first loss of target-compatible allelic support while alive, or **E**: extinction before G. When G occurs first, eventual later extinction does NOT erase the first-G classification. End-of-horizon continued access is **X**. Each of these mutually exclusive first-event outcomes is counted from the **same original all-start denominator**, hence

`P_X(T) = 1 − CIF_G(T) − CIF_E(T)`,

where CIFs are **cumulative incidence of the first competing event**, not cause-specific hazard estimates.

| Resource | Policy | G first | E first | Still alive + I target accessible at census 80 |
| --- | --- | ---: | ---: | ---: |
| B8 | Fixed A | 13,868 | 0 | 11,732 |
| B8 | Evolving A | 16,000 | 0 | 9,600 |
| B4.5 | Fixed A | 12,896 | 12,564 | 140 |
| B4.5 | Evolving A | 16,018 | 337 | 9,245 |

Every row sums to 25,600. Between evolving and fixed policies:

| Resource | `ΔCIF_G` pp | `ΔCIF_E` pp | `ΔP_X=-ΔCIF_G-ΔCIF_E` pp |
| --- | ---: | ---: | ---: |
| B8 | +8.328125 | 0 | **−8.328125** |
| B4.5 | +12.1953125 | −47.76171875 | **+35.56640625** |

**Key observation:** In B4.5 a larger fraction experiences *genetic closure first* in evolving A, but a much smaller fraction experiences *extinction before closure*. The net fraction remaining alive and target-accessible increases. **The +12.20 pp first-G difference does not prove that the instantaneous genetic-loss hazard rises**: competing extinction changes the population at risk. This comparison is descriptive post-outcome analysis of previously registered data, not an additional registered confirmatory result.

The alternative exact product `P_X=P(alive)×P(I accessible | alive)` is valid. Its symmetric Kitagawa decomposition gives B4.5 +21.74655607 pp as a survival-prevalence term and +13.81985018 pp as a survivor-conditional-composition term. These are **arithmetic**, not mediation. The second term is not zero, and treating it as a direct genetic-maintenance effect would be biased by selection on survival.

## A minimal mechanistic model and its limits

Define the three states: **X** alive with required I support; **Y** alive but genetically closed to the founder I target; **D** extinct. No X return is possible without supplying a missing I allele. The allowed transitions are X→Y (first G), X→D (first E), Y→D (eventual extinction). D is absorbing; the model allows Y→D but no D→X.

For each policy `a` and resource `b`, let `h_G(a,b,t)` and `h_E(a,b,t)` be **conditional first-event probabilities among still-X populations during update t**, with `0≤h_G+h_E≤1`. Then exactly in discrete time under this event definition:

`P_X(a,b,T) = ∏_{t<T} [1 − h_G(a,b,t) − h_E(a,b,t)]`.

This is an *existing competing-risks accounting structure*, **not a new biological law**. A constant-rate continuous-time submodel has `P_X=exp{−T[λ_G(a,b)+λ_E(a,b)]}`, and evolving assurance increases the joint-accessible proportion if

`λ_G(E,b)+λ_E(E,b) < λ_G(F,b)+λ_E(F,b)`.

For the more general actual discrete system, compare the products instead. A **new biological theory** would need independently justified, source-compatible expressions for how resource/pollen service, finite reproduction, assurance expression, effective size, inbreeding and inherited I alleles drive `h_G` and `h_E`. Simply writing a product, or postulating a genetically adverse `Δλ_G>0`, is insufficient.

For the original **binary policy** comparison (not continuous A), the exact algebraic sign condition can alternatively be written, for positive terms, as

`log[P_alive(E)/P_alive(F)] + log[P(I-access|alive,E)/P(I-access|alive,F)] > 0`.

An elasticity derivative requires a *new explicitly continuous assurance parameter* and its defined counterfactual. Its elasticities cannot be estimated merely by calling fixed-A and evolving-A policy arms two nearby trait levels.

At current B4.5, the observed survivor-conditional access proportion is *higher* in evolving A. Therefore the proposed universal premise “evolvable A always decreases survivor-genetic access” is **not an observation** and must not be used as a confirmed theorem hypothesis.

## Proposed three research streams, in order

**1. Mechanistic source-consistent theory (no new biology first).** Derive a parsimonious model of resource-dependent reproductive/occupancy hazard and standing-I allelic-support loss. Present X/G/E as competing events. State explicitly which monotonicity/cost assumptions guarantee one transition or permit none/multiple transitions. Showing two opposite observed signs at B4.5 and B8 does **not** establish a unique smooth budget threshold. At most, if the *underlying expected* policy-contrast function is continuous and truly opposite in sign at those endpoints, an intermediate crossing exists; no uniqueness follows. Model3's original integer/ovule/seed operators and discretization must be checked before assuming budget continuity.

**2. Independent prospectively registered resource-gradient falsification.** Freeze NEW founder × visitor seed namespaces, budget grid, ≥2 biologically justified mating/cost regimes, source versions and statistical plan before producing new outcomes. Primary: all-start `P_X(B,T)` policy difference, not survivors-only access. Keep `CIF_G`, `CIF_E`, `P_alive` as predeclared separable diagnostics. Pre-register whether a unique root is predicted and allow the predictions “no crossing” and “more than one crossing” to fail the simple theory. Specify scientific SESOI, two-axis resampling, interaction/within-cell sensitivity and budget costs. **Do not launch** from this note; authorization and the repository's power gate must be respected. A held-out generative model is stronger generality evidence than merely finer tuning of the already exposed Model3 grid.

**3. Causal rescue and actual response (defined interventions, not magical survival).** Arbitrarily forbidding extinction over dozens of reproductive updates changes cohort size, parents, genetic drift and selection. It cannot by itself prove that A affects future opportunity “only through survival”. Distinguish:
- A prospective **controlled demographic support** policy with precise genotype/fecundity side effects, whose effect is a *new intervention effect*, not automatically a natural indirect effect of A;
- a separately defined **I-allele reintroduction** with source-matched census and A-expression at the fork (test whether support limits a sustained high-I response);
- a restored-functional-pollinator versus matched non-restoration comparison, with positive actual pollen/maternal/paternal return confirmation, ancestral target attainment (not merely positive mean change), occupancy in the all-start denominator, and special treatment for donors already meeting the I target;
- eligibility and source-cohort nesting decided **before** exposing outcomes, with mutation/immigration-enabled rescue as explicitly distinct sensitivity.

A large effect after demographic protection is not proof of unconfounded mediation, just as a survivor-only comparison is not a direct genetic effect.

## Journal decision, independent of outcome shopping

**Existing data:** One bounded, honest model-based **Evolution** paper is feasible after permanent archiving, final visual/Methods/reference/author checks.

**Stronger general theory:** A source-derived competing-risk model predicting independent results and at least one independent generative context could make **The American Naturalist** a compelling first target.

**Nature Ecology & Evolution stretch:** Broad conceptual originality and out-of-model/empirical generality plus an informative actual restored-service/allele-rescue intervention would strengthen the case. Even if all registered predictions are supported, no journal acceptance or priority is assured. Conversely, a registered falsification must **revise or reject the proposed law**, not automatically relabel the same predicted mechanism for a different journal.

**Do not conflate:** source result vs analytic assumption, statistical precision vs biological SESOI, first-event incidence vs cause-specific hazard, selected survivor composition vs genetic causal effect, target-compatible allele vs realized floral recovery, or two exposed synthetic budgets vs a universal single critical boundary.

**Editorial recommendation:** Preserve the original four Q1–Q4 questions, lead with the registered B8 G and resource-dependent S effects, display the **source-locked first-competing-event table as an explanatory secondary result**, and retain N5's `P(alive and genetically I-target accessible)` sign pattern as explicitly **exploratory** until an independent registration tests the theory. Keep the still-unverified actual-return hypothesis outside completed Results.

## Literature context

- [Competing-risk cumulative incidence](https://academic.oup.com/eurheartj/article/35/42/2936/784255) and [cause-specific CIF dependence](https://pmc.ncbi.nlm.nih.gov/articles/PMC3328633/): event incidence is not cause-specific hazard.
- [Outcome truncation by death and survivor-average effects](https://pmc.ncbi.nlm.nih.gov/articles/PMC4131726/): randomization does not make raw survivor-only treatment contrasts causal.
- [Four-population Viola resurrection study](https://doi.org/10.1111/nph.19422): field selfing-syndrome evolution is established but does not measure our founder-target high-I genetic-access endpoint or restoration time window.
- [Cheptou 2019, published online 2018](https://doi.org/10.1093/aob/mcy144): existing rescue/extinction theory; avoid claiming the first selfing-rescue trade-off.
