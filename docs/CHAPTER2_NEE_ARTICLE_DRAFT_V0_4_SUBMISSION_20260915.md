# Nonlinear response limits transport of determinant rankings across ecological regimes

## Abstract

Ecologists increasingly quantify how the relative importance of environmental and biotic drivers changes with context. A harder problem is whether a determinant ranking estimated in one context can be transported to another after ecological structure has been compressed into a scalar summary. We derive an exact sufficiency boundary: in a bilinear state–community response, variance-equivalent effective independence gives community and state-by-community contributions the same second-moment multiplier, so their rank cannot reverse. Higher-order response geometry breaks this invariance. Two structurally distinct nonlinear ecological models cross the resulting boundary, and a prospectively frozen feedback intervention produces 52 community-to-interaction reversals in 108 comparisons versus none without feedback. We then place 42 island interaction systems from six studies on separately measured partner-breadth and temporal-synchrony axes; the source-balanced plane spans both dimensions under prespecified coverage criteria. Yet a frozen audit of 25 island studies finds no complete outcome-independent determinant–response contract. Context-dependent importance is therefore only the starting point: transporting a ranking requires evidence that the receiving regime preserves the response information on which that ranking depends.

Ecological studies often summarize “what matters most” using effect sizes, variance components or predictive importance. Recent statistical work makes such importance explicitly conditional on ecological context, and empirical analyses show that the relative contribution of major drivers can vary across environments and functional groups (Schulz et al., 2025; Guilbault et al., 2025). Context dependence itself is therefore not the unresolved point. The unresolved point is **transportability**: when does a ranking estimated in one ecological regime remain valid in another?

This question becomes especially sharp after compression. Ecology routinely replaces structured systems by scalar equivalents. Hill numbers express diversity as an effective number of equally common types (Jost, 2006), while synchrony and portfolio metrics summarize covariance structure (Loreau & de Mazancourt, 2008; de Mazancourt et al., 2013). Such reductions are useful because they state what property is preserved. But a scalar that preserves one property need not preserve a nonlinear ecological response to the structure that was discarded.

Consider `k` equal-variance community components with common pairwise correlation `rho`. Their pooled mean has the same variance as the mean of

`k_eff = k / [1 + (k-1)rho]`

independent components. This equivalence is exact for the second moment. If a determinant ranking depends only on that preserved information, it should transport along a fixed-`k_eff` contour. If it does not, the receiving system differs in response-relevant information that the compression omitted.

We use this logic to turn transportability into a testable ecological object. First, we derive an exact response class in which the ranking must be invariant. Second, we identify the higher-order mixed response geometry that breaks that invariance. Third, we ask whether two nonlinear ecological models cross the boundary and prospectively test a phase-shaping mechanism. Finally, we ask whether natural island interaction systems occupy distinct values of the context dimensions that the theory says should remain separate, and whether existing island studies contain the matched measurements needed to test cross-regime transport directly.

Island systems are useful here not because we assume a universal island syndrome. Insularity can alter partner breadth, composition, turnover, stochasticity and reproductive context simultaneously, while comparative studies often seek general driver rankings across islands. We therefore use island interaction systems as an external regime map, not as direct validation of the synthetic mechanism.

Our claim is consequently narrower than “importance is context dependent” and stronger than a simulation counterexample. We identify an exact sufficiency boundary for determinant-rank transport, demonstrate how nonlinear ecology violates it, show that the required context axes are independently occupied in nature, and identify the measurement contract still missing for direct natural tests.

## Results

### A second-moment compression has an exact rank-transport boundary

Let centered `X` denote focal state and `Zbar_k` the mean of `k` exchangeable centered community variables with variance `sigma^2` and common correlation `rho`. For the bilinear response

`Y = aX + b Zbar_k + c X Zbar_k`,

write

`tau_k = Var(Zbar_k) = sigma^2[rho + (1-rho)/k] = sigma^2/k_eff`.

With `X` independent of `Zbar_k`, the exact functional decomposition is

`S = a^2 Var(X)`,  
`C = b^2 tau_k`,  
`I = c^2 Var(X) tau_k`.

Hence `I/C = c^2 Var(X)/b^2`. Aggregation or synchrony can make the state component `S` overtake both realization-linked components, but they cannot reverse the ordering of `C` and `I`. Fixed second-moment equivalence is therefore sufficient for this part of the determinant ranking under the bilinear response class.

The first omitted information is higher order. For a smooth response to centered pooled variation `Z`,

`E[f(mu+Z)] = f(mu) + f''(mu)kappa_2/2 + f'''(mu)kappa_3/6 + f''''(mu)(kappa_4+3kappa_2^2)/24 + ...`.

Variance equivalence fixes `kappa_2`, but not `kappa_3`, `kappa_4` or higher cumulants. Under a common-factor construction, systems with identical `k_eff` therefore retain different higher-order distributions.

A scalar expansion alone does not determine rank because interaction variation is generated by mixed state–community geometry. For the exact centered quadratic response

`Y = aX + bZ + cXZ + (d/2)(Z^2-tau) + (e/2)X(Z^2-tau)`,

community and interaction components are

`C = b^2 tau + bd mu_3 + (d^2/4)Var(Z^2)`

and

`I = Var(X)[c^2 tau + ce mu_3 + (e^2/4)Var(Z^2)]`.

For symmetric `Z`, the sign of the change in `I/C` with fourth-order variation is `sign(e^2 b^2 - c^2 d^2)`. Second-moment sufficiency therefore survives this order only under a restrictive alignment of pure and mixed curvature. This is the analytical boundary: a compressed coordinate can transport the ranking only when the response operator discards, or is insensitive to, the information that the compression discards.

### Two nonlinear ecological systems cross the transport boundary

We next tested whether this failure occurs in ecological models with different internal structures. In a plant–pollinator response model, plant state interacts with stochastic partner identity, trait matching, breadth, arrival, loss and effectiveness. Across the same six master seeds under collision-free hierarchical random streams, the `k=1` baseline contained a median **45.5 mixed-sign realizations [43–59]/96**; median normalized `(S,C,I)` was `(0.031, 0.743, 0.228)`, with six-seed ranges `S=0.020–0.041`, `C=0.698–0.787` and `I=0.186–0.268`. The medians changed to `(0.247, 0.232, 0.508)` at `k=4` and `(0.535, 0.141, 0.320)` at `k=16`. Starting-state share exceeded community share in 4/6 seeds at `k=4` and 6/6 at both `k=8` and `k=16`; `I/C` rose from 0.31 to 2.28, so community and interaction contributions still reversed order. The historical offset-stream values are retained only as provenance; the corrected six-seed receipt is used for inference.

A structurally separate adaptive consumer–resource model crossed the same boundary. Across 54 settings and six frozen seeds, 255/324 setting-by-seed trajectories contained an interaction-dominated intermediate scale, 111/324 crossed the `C/I` boundary and 68/324 followed a community-dominated → interaction-dominated → state-dominated winner sequence. Eighteen of 54 settings reversed `C/I` in at least four of six seeds.

These results do not establish a natural threshold at a particular synthetic `k`. They show that determinant rank can fail to transport even when a simpler second-order description suggests equivalence.

### A post-freeze structural challenge separates robust and operator-dependent rank transitions

After the primary plant–pollinator result was frozen, we challenged the two most direct implementation-specific explanations without changing biological parameters, master seeds, replicate count or the `k` sequence. First, refining the starting-state grid from 21 to 41 and 81 points preserved the same median winner sequence at the audited scales: community realization at `k=1`, non-additivity at `k=4` and starting state at `k=16`. The intermediate interaction-dominated regime is therefore not a consequence of the frozen 0.05 grid spacing.

Second, we removed both discontinuities in the plant update rule. Instead of a hard service threshold and movement toward one best partner, the smooth rule moved plant state continuously by `alpha(1-service)` toward the encounter-weighted centroid of current partner traits. The prespecified criterion required `C>I` at `k=1` followed by `I>C` at a later audited scale in at least four of six seeds. All six seeds passed, although the first crossover varied from `k=2` to `k=16`. The stronger high-`k` starting-state takeover was not preserved: under smooth feedback the median `k=16` decomposition remained community/interaction dominated, while a fixed-state negative control became interaction dominated after `k=1`.

Raw variance components clarify the mechanism. Under the frozen 21-point rule, median per-cell community SS contracted with log2 slope **-1.51** across `k`, whereas non-additive SS contracted more slowly at **-0.84** and starting-state SS was approximately retained (**+0.11**). Refining the grid changed these slopes negligibly; smooth and fixed rules also retained faster contraction of `C` than `I`. Thus intermediate interaction dominance reflects **differential contraction**, not absolute amplification of interaction variance. The robust core is the `C/I` ordering reversal; the later `I/S` ordering is a property of the frozen response operator rather than a universal consequence of aggregation.

### A failed prediction isolates the wrong level of nonlinearity

**Additional response-rule boundary (2026-09-25).** A prospectively specified 2 × 2 × 2 factorial separated the service threshold, response target and service-dependent damping using the same six seeds, 96 histories, 21 starting states and five aggregation scales; fixed state was retained as a descriptive control. At k=16, removing only the threshold retained S dominance (median 63.0%), whereas changing only the target from the best partner to the encounter-weighted centroid reduced S to 4.2% (primary 53.5%). Best-to-centroid changes reduced S share in all 24 conditional comparisons at k=16 (four settings × six seeds, not 24 independent seeds). These within-model interventions implicate target choice within the tested envelope, not a general loss-of-memory explanation: fixed state retains initial traits exactly yet is I dominated. Furthermore, continuous centroid movement without service-dependent damping remained C dominated by component medians at all audited k. Thus the C/I reversal described above survives the specific smooth-rule challenge, but is not universal over the expanded response-rule family. Full cells, all contrasts and separate terminal-state diagnostics are retained in `data/results/update_factorial_20260925/`; no parameters were retuned to restore a preferred ranking.

We first froze a scalar explanation based on fourth-order curvature of the Holling-II response before opening the consumer–resource setting map. The curvature index increased strongly with handling parameter `h`, predicting more `C/I` reversals at larger `h`.

The prediction failed in the opposite direction. Summed reversal counts were 41 at `h=1`, 38 at `h=2` and 32 at `h=4`. Among 18 matched high- versus low-`h` blocks, zero increased, 16 tied and two decreased. Scalar nonlinearity alone was therefore not the phase-setting condition.

The failure is informative because the exact theory points to mixed state–community geometry. A response can be strongly nonlinear in one scalar while lacking the mixed derivatives needed to reorganize determinant order.

### A fresh intervention identifies a phase-shaping feedback

Guided by the analytical result and the failed scalar prediction, we froze a directional feedback test before running six previously unused seeds. Across 18 factorial blocks, a feedback knockout (`alpha=0`) was compared with active state adjustment (`alpha=0.15`), giving 108 paired block-by-seed comparisons.

The knockout produced **0/108** `C/I` reversals. Active feedback produced **52/108**. Every discordant pair was in the predicted direction. The intervention did not merely increase interaction variance: without feedback, all 108 cases were already `I>C` at `k=1`; active feedback instead created a community-dominated low-aggregation regime in 52 cases, all of which crossed to `I>C` by `k=4`.

Feedback therefore changed phase topology. It created a determinant-order boundary that aggregation could traverse, providing a prospective mechanism-level test of the transport failure.

### Natural island systems occupy separate breadth and synchrony regimes

The theory does not license literal substitution of natural diversity for synthetic `k`. It instead implies a measurement requirement: partner breadth and temporal synchrony should remain separate coordinates when nonlinear response is plausible.

Before candidate extraction we froze a public-data admission protocol. Eligible systems required quantitative machine-readable biotic interactions, stable local-system and partner identity, at least six aligned source-native time bins, at least three nonconstant partner series, known or normalizable effort and a reconstructible time-by-partner matrix. Breadth was pooled effort-standardized Hill `D1`; synchrony was Loreau–de Mazancourt `phi`. Multiple sites from one study did not count as independent studies, and cross-system summaries were source balanced.

The final plane contains **42 systems from six studies and five island or archipelago groups**, from Hawaii (Aslan et al., 2019), Mallorca (Lázaro et al., 2022), Tenerife (Lara-Romero et al., 2019), Cabrera (Serra-Marin et al., 2025), Martinique (Cyrille, 2025) and Great Britain STEP (Holzschuh et al., 2016), with the England data harmonized in EuPPollNet (Lanuza et al., 2025). Source-balanced breadth had `D1` q90/q10 = **4.521** and synchrony had `phi` q90-q10 = **0.352**. The absolute source-balanced Spearman correlation between `log D1` and `phi` was **0.325**, and **26.2%** of systems occupied the joint interquartile interior.

We specified minimum coverage criteria before candidate extraction to prevent a narrow or effectively one-dimensional sample from being promoted to a broad regime claim. The observed plane exceeded each criterion. Removing all 19 Mallorca systems, the largest study, left `D1` q90/q10 = **5.494**, `phi` span = **0.352**, interior occupancy = **26.1%** and `|rho_s| = 0.454`.

England STEP expanded the high-synchrony edge. Its island-study classification was inherited from EuPPollNet before this analysis. Before coordinates were opened, we froze four source-native rounds in each of 2012 and 2013, equal 30-minute and 300-m2 site-round effort, and admitted only three sites with complete 4+4 outcome-independent schedules. Their `phi` values were 0.450, 0.635 and 0.414. An independent implementation reproduced every committed `D1` and `phi` exactly; a positive-bin-only diagnostic retained high `phi` values of 0.411, 0.618 and 0.364.

A stricter leave-one-study-out diagnostic shows where replication remains thin under the original source-native schedules. Removing England reduces source-balanced `phi` span to **0.162**; removing Martinique lowers interior occupancy to **18.75%**. Because time-bin depth ranged widely among sources, we then froze a separate sampling-depth sensitivity before execution and rarefied every admitted system to six distinct source-native bins 1,000 times. The full-data correlations confirmed finite-depth sensitivity (`rho_s(phi, time bins)=-0.273`; `rho_s(rho_eq, time bins)=-0.372`). Nevertheless, the primary phi-only dispersion criterion still passed in **90.8%** of 999 valid rarefactions. England's three sites retained high six-bin median `phi` values of **0.446, 0.680 and 0.475**. More importantly, after excluding England the synchrony-span criterion passed in **93.3%** of equal-depth rarefactions and all four dispersion criteria passed in **89.1%**. Thus the original full-data England leverage is partly sampling-schedule contingent rather than evidence that high synchrony is uniquely supplied by England. We retain the full-data coordinates as primary because six-bin rarefaction itself inflates `phi` in several longer series; the equal-depth analysis is a sensitivity test, not a replacement estimator. The stronger joint-coordinate perturbation, which also recomputed `D1` from the six selected bins, passed in **61.1%** of valid rarefactions. The primary source search stopped once the prespecified coverage and largest-source sensitivity criteria were satisfied. After the original all-source leave-one-study-out diagnostic identified England and Martinique as individually load-bearing, we prospectively opened a separate four-candidate robustness challenge using the unchanged admission and coordinate contract. All four candidates closed before coordinate extraction; no additional `D1` or `phi` values were opened and no source was added.

### Existing island literature cannot yet test rank transport directly

A separate audit, frozen before the natural-regime search, contains 25 research entries across 21 exact geographic-overlap labels. Direct comparable plant responses were available in **21/25** entries and direct partner arrival or replacement in **2/25**, but **0/25** supplied the complete outcome-independent source-state → transition → realized-community → plant-response contract.

The natural-regime reconstruction closes only the context side of that measurement problem. It shows that breadth and synchrony can be estimated from suitable repeated-interaction data, but it does not add matched plant-response outcomes and therefore does not change the 0/25 result.

Together, the natural analyses define the empirical ceiling. Island systems occupy distinct breadth–synchrony regimes, but current studies do not provide the matched response structure required to test whether a determinant ranking estimated in one regime transports to another.

## Discussion

Context-dependent relative importance is already an established ecological problem. Conditional variance-partitioning methods explicitly allow driver contributions to vary with context, and recent macro-moth analyses show that the relative importance of climate and habitat changes across bioclimatic and functional settings (Schulz et al., 2025; Guilbault et al., 2025). Our result addresses the next inferential step: **what has to be preserved for a ranking to be transportable across contexts?**

The bilinear null gives one exact answer. When a compressed coordinate preserves every distributional feature to which the response ranking is sensitive, transport follows. The nonlinear extension gives the failure mode: equal second moments can leave higher cumulants and identity support unconstrained, and mixed state–community curvature can translate those omitted features into a different ordering of variance components. The point is not that effective numbers are defective. They are equivalence coordinates. The error is to promote an equivalence coordinate to a sufficient nonlinear ecological state without establishing response sufficiency.

The failed Holling prediction further sharpens this boundary. Scalar curvature alone did not predict rank transitions, whereas a prospectively frozen state–community feedback intervention did. This directs mechanism tests toward pathways that couple focal state to realized community context rather than toward one-dimensional nonlinearity scores.

The post-freeze plant challenge adds an important distinction. Feedback is not required for non-additive state × community variance or even for a finite `C/I` crossover in the plant model; matching geometry alone can retain non-additivity as additive realization variance is averaged away. What the frozen threshold-best operator contributes is stronger preservation of between-state variance, allowing `S` eventually to overtake `I`. We therefore do not treat the complete community → interaction → state sequence as the general law. The more portable result is that aggregation can contract additive realization variance and non-additive variance at different rates, so the identity of the dominant component can change even while all realization-linked variance is declining.

The natural regime plane supplies an external ecological constraint. Six studies occupy a broad breadth–synchrony space under a result-blind admission protocol, and the prespecified coverage criteria survive removal of the largest source. Under the original unequal sampling schedules, England supplies much of the sampled high-synchrony edge and Martinique materially supports interior occupancy. Equal-depth rarefaction shows that the apparent England leverage is not stable to temporal sampling depth: England itself remains highly synchronous, but England-excluded synchrony dispersion usually clears the frozen numerical floor once all systems are evaluated at six bins. The strongest natural inference is therefore that the response-relevant context space is real and broadly occupied, while source leverage in the observed plane partly reflects the sampling schedule and should not be read as an ecological uniqueness claim.

This framing changes how comparative disagreements should be interpreted. Conflicting determinant rankings across studies need not be treated only as residual heterogeneity; they can be evidence that a ranking was transported beyond the regime in which its sufficiency assumptions held. In island-syndrome research, different studies may sample distinct breadth–synchrony regimes, but our data do not test that explanation for any particular floral or reproductive syndrome. It remains a prospective prediction.

The 0/25 audit shows what a decisive natural test requires. A study must measure the relevant context coordinates before opening outcomes, follow the transition into a realized community, and then quantify the response on the same unit. The current literature is rich in outcomes but sparse in complete transition-linked contracts. The next advance therefore does not require a larger retrospective collection of examples; it requires prospectively matched regime and response measurements.

The logic extends beyond islands. Whenever ecology compresses structured context and then compares the relative importance of drivers, transportability should be demonstrated rather than assumed. A practical sequence is: define the property preserved by the compression; derive what information it omits; determine whether the response operator is sensitive to that omitted information; measure the relevant context axes in donor and receiving systems; and collect matched outcomes when cross-regime transport is the target.

Several boundaries remain. The natural systems do not validate the synthetic `C/I` crossover, and natural Hill `D1` is not synthetic `k`. The numerical coverage criteria are analysis-design safeguards, not biological thresholds. The consumer–resource generalization was motivated after the original plant–pollinator pattern, although the feedback intervention itself was prospectively frozen on unused seeds. The natural plane retains source-specific leverage. These boundaries restrict the claim to what the evidence supports: an exact transportability condition, demonstrated nonlinear violations, and an empirically occupied regime space in which direct transport remains unidentified.

Determinant rankings are therefore conditional ecological objects. The question is not only whether importance changes with context, but whether the information preserved across contexts is sufficient for the ranking to survive transport.

## Methods

### Response decomposition and analytical null

For response matrices `Y_ir`, indexed by focal state `i` and stochastic community realization `r`, total variation was partitioned exactly as `SS_tot = SS_S + SS_C + SS_I`. Normalized shares `S`, `C` and `I` represent additive focal-state variation, additive community-realization variation and the non-additive state-by-community remainder. The decomposition is descriptive rather than a causal identification scheme.

The bilinear null, common-factor cumulant expansion and exact quadratic mixed-response model were fixed in the higher-order sufficiency design. The bilinear null identifies an invariant `I/C`; the higher-order calculations identify information omitted by variance equivalence and the mixed-curvature condition under which that information changes component rank.

### Nonlinear model classes and prospective intervention

The plant–pollinator model evaluated 21 focal starting states across stochastic community realizations and pooled independent trajectories over `k={1,2,4,8,16}`. A post-freeze implementation audit found that the historical arithmetic seed offsets reused integer streams across mainland/island replicate pairs. We corrected stream construction without changing the six master seeds, replicate count, trait grid, biological parameters or `k` sequence, using `numpy.random.SeedSequence` in the hierarchy master seed → replicate → scenario → copy. Copy streams retain prefix stability across `k`, preserving the intended common-random-number comparison while keeping mainland and island streams disjoint. Paper-facing Monte Carlo magnitudes use the corrected six-seed median and range; the historical offset-stream values remain archived only as provenance. The adaptive consumer–resource model crossed resource number, matching width, handling, adaptation and aggregation levels over six frozen seeds. The failed handling-curvature prediction was frozen before its setting-level outcome map was opened.

The mixed-feedback test was frozen before execution on six previously unused seeds. Across 18 factorial blocks, `alpha=0` and `alpha=0.15` were compared using 256 realizations at each audited aggregation level. The primary outcome was defined in advance as `C>I` at `k=1` followed by `I>C` at any later audited `k`.

The later plant–pollinator structural challenge was explicitly post-freeze and was not used to retune the primary model. Before execution we fixed two diagnostics. The grid audit repeated the corrected six-seed, 96-realization, `k={1,2,4,8,16}` design on 21-, 41- and 81-point equally spaced state grids. The update-rule audit kept the 21-point grid and compared the frozen threshold-best rule with (i) a smooth rule that moves state at every nonempty step by `alpha(1-service)` toward the encounter-weighted partner centroid and (ii) a fixed-state negative control. The smooth-rule decision was set before execution at at least four of six seeds showing `C>I` at `k=1` and `I>C` at one or more later scales. In addition to normalized shares, the audit stored raw SS, per-cell SS and log2 scaling slopes for each component to distinguish absolute amplification from differential contraction.

### Natural-regime admission and provenance

The natural-data gate was frozen on 13 September 2026 before candidate extraction. Data had to be public before the freeze and provide quantitative biotic interactions, stable local-system and partner identity, at least six aligned source-native time bins, at least three nonconstant partner series, known/equal/normalizable sampling effort and a reconstructible time-by-partner matrix. Unavailable data were not treated as biological negatives. Candidate searching followed a result-blind source order and stopped when the prespecified coverage and largest-source sensitivity criteria were satisfied. After the primary route was fixed, a separate post-promotion robustness challenge prospectively froze four previously unresolved candidates and reused the same admission contract to test whether England-removal coverage could be restored. None passed to coordinate extraction, the candidate universe was not expanded, and the challenge closed with the original source-complementarity limitation unchanged.

Systems from one study were retained as systems but not counted as independent studies. Mallorca and Cabrera are separate studies but one Balearic group. Great Britain retained the island-study classification assigned by EuPPollNet before our analysis. Source admission records, hashes and adapter decisions were committed before coordinate opening.

### Natural breadth and synchrony

Natural `D1` was not treated as an estimator, calibration or proxy for synthetic `k` or `k_eff`. In the theory, `k` is the nominal number of exchangeable synthetic community components and `k_eff` is a variance-equivalent effective independence determined jointly by `k` and correlation. In the natural analysis, `D1` is the effective diversity of the pooled effort-standardized partner interaction-share distribution. Its role is only to provide an outcome-independent coordinate for realized partner breadth. We estimated no numerical mapping between `D1` and `k` or `k_eff`, and used no natural threshold corresponding to synthetic `k≈4`. The theory-to-data connection is therefore structural: the nonlinear transport argument requires breadth and synchrony to remain separately measured context dimensions; it does not place natural breadth on the synthetic aggregation scale.

Within each system, interaction values were standardized by the source-native effort scalar fixed at admission. Pooled partner shares `p_j` defined breadth as

`D1 = exp[-sum_j p_j log(p_j)]`.

Synchrony was

`phi = Var_t(sum_j x_tj) / [sum_j SD_t(x_tj)]^2`

using nonconstant partner series. Uncertainty was estimated with 1,000 bootstrap resamples of source-native time bins.

For cross-system summaries, each source study received equal total weight. Before candidate extraction we specified minimum requirements for system/study/group counts, breadth dispersion, synchrony dispersion, two-dimensionality, joint-interior occupancy and persistence of the numerical dispersion criteria after removal of the largest source. These were analysis-design safeguards, not ecological thresholds.

After a post-freeze code review identified a negative association between synchrony and the number of source-native time bins, we froze a separate six-bin sensitivity before running it. For each of 1,000 deterministic rarefaction iterations, six distinct bins were sampled without replacement within every admitted system and synchrony was recomputed after re-evaluating nonconstant partner eligibility. The primary sensitivity retained full-data pooled `D1` and perturbed only `phi`; a secondary analysis recomputed both coordinates from the same six bins. Iterations were invalid only if any system fell below three nonconstant partner series. This analysis tests sampling-depth dependence of the admitted plane and does not redefine the primary estimand or source-admission rules.

### Literature identifiability audit

The formal island audit retained the original denominator of 25 research entries. Each entry was scored for directly observed comparable plant response, direct partner arrival or replacement and the full outcome-independent measurement contract. Missing axes were not inferred from outcomes or narrative interpretation. Later source expansion and natural-regime reconstruction did not alter this denominator.

### Reproducibility and claim control

Admission records, source hashes, adapters, analysis plans, regime coordinates, search closure and post-analysis sensitivity diagnostics are versioned in the repository. England STEP was admitted and its adapter frozen before coordinates were opened; an independent implementation later reconstructed its `D1` and `phi` values exactly. The all-source leave-one-study-out analysis was performed only after the primary coverage decision and is reported as a transparency diagnostic, not a retroactive selection rule. A separate four-candidate robustness challenge was prospectively frozen only after that diagnostic and opened no candidate coordinates; its failure is retained as a robustness record rather than a route redefinition.

### AI-assisted development and writing

OpenAI ChatGPT was used as an assistive tool during project development for code drafting and review, workflow and source-provenance organization, and language editing. Large-language-model output was not treated as empirical evidence or as an authority for source qualification. All LLM-assisted code and text were subject to human review and to the versioned tests and provenance checks described above; responsibility for study design, analysis choices, interpretation and the final manuscript remains with the authors. No large language model is listed as an author.

## Data availability

Natural-regime analyses use the public source datasets cited below. Source locks, checksums and access provenance are recorded in the repository. Source data retain their original licences and repository records.

## Code availability

Analysis code, frozen design objects, failed and successful prediction receipts, natural-regime coordinates and provenance diagnostics are maintained in `izu-core`. A permanent archived release and DOI will replace the repository-only statement before publication.

## References

Aslan, C. E., Shiels, A. B., Haines, W. & Liang, C. T. Non-native insects dominate daytime pollination in a high-elevation Hawaiian dryland ecosystem. *Am. J. Bot.* **106**, 313–324 (2019). https://doi.org/10.1002/ajb2.1233

Cyrille, N. Floral offer and seasonality shape plant-pollinator networks in tropical gardens [dataset and analysis code]. dataUBFC (2025). https://doi.org/10.25666/DATAUBFC-2025-03-28

de Mazancourt, C. et al. Predicting ecosystem stability from community composition and biodiversity. *Ecol. Lett.* **16**, 617–625 (2013). https://doi.org/10.1111/ele.12088

Guilbault, E. et al. Strong context dependence in the relative importance of climate and habitat on nation-wide macro-moth community changes. *J. Anim. Ecol.* **94**, 1948–1961 (2025). https://doi.org/10.1111/1365-2656.70107

Holzschuh, A. et al. Mass-flowering crops dilute pollinator abundance in agricultural landscapes across Europe. *Ecol. Lett.* **19**, 1228–1236 (2016). https://doi.org/10.1111/ele.12657

Jost, L. Entropy and diversity. *Oikos* **113**, 363–375 (2006). https://doi.org/10.1111/j.2006.0030-1299.14714.x

Lanuza, J. B. et al. EuPPollNet: A European database of plant-pollinator networks. *Glob. Ecol. Biogeogr.* **34**, e70000 (2025). https://doi.org/10.1111/geb.70000

Lara-Romero, C., Seguí, J., Pérez-Delgado, A., Nogales, M. & Traveset, A. Beta diversity and specialization in plant–pollinator networks along an elevational gradient. *J. Biogeogr.* **46**, 1598–1610 (2019). https://doi.org/10.1111/jbi.13615

Lázaro, A., Gómez-Martínez, C., González-Estévez, M. A. & Hidalgo, M. Portfolio effect and asynchrony as drivers of stability in plant–pollinator communities along a gradient of landscape heterogeneity. *Ecography* **2022**, e06112 (2022). https://doi.org/10.1111/ecog.06112

Loreau, M. & de Mazancourt, C. Species synchrony and its drivers: neutral and nonneutral community dynamics in fluctuating environments. *Am. Nat.* **172**, E48–E66 (2008). https://doi.org/10.1086/589746

Schulz, T., Saastamoinen, M. & Vanhatalo, J. Model-based variance partitioning for statistical ecology. *Ecol. Monogr.* **95**, e1646 (2025). https://doi.org/10.1002/ecm.1646

Serra-Marin, P. E. et al. Comparative assessment of automated and manual monitoring in comprehensive plant–pollinator communities. *Methods Ecol. Evol.* **16**, 2960–2978 (2025). https://doi.org/10.1111/2041-210X.70165

## Figure legends

**Figure 1 | Exact sufficiency boundary for rank transport.** A variance-equivalent coordinate fixes the second moment while higher cumulants remain free; the quadratic mixed-response result identifies the curvature condition under which omitted information changes `C/I`.

**Figure 2 | Nonlinear determinant-order transitions and prospective mechanism test.** Plant–pollinator and consumer–resource rank trajectories; failed scalar-curvature prediction; fresh feedback knockout versus active-feedback reversal counts. A post-freeze structural challenge separately shows grid-stable C/I rank inversion, faster contraction of community than non-additive SS, and update-rule sensitivity of the later starting-state takeover.

**Figure 3 | Natural breadth–synchrony regime plane.** Forty-two systems coded by source and island group with source-balanced summaries. The largest-source sensitivity is prespecified; later source-deletion diagnostics show England leverage under the original schedules, while the equal-depth six-bin sensitivity shows that this leverage is partly sampling-depth contingent.

**Figure 4 | Measurement ceiling for rank transport.** The full determinant–response chain, 21/25 direct response coverage, 2/25 direct arrival/replacement and 0/25 complete contracts, linked to a prospective cross-regime design.
