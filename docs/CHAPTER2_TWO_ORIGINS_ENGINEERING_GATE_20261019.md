# Two origins of island floral syndromes — executable engineering gate

**2026-10-19 | TECHNICAL-ONLY, no registered science / no publication inference.**

This separate prototype is not a change to the supported single-paper Q1–Q4 results on [PR #609](https://github.com/zuizui0223/izu-core/pull/609). It implements the **minimal source-lineage to attempted arrival to reproductive establishment to persistence to phenotypic outcome ledger**, using the *unchanged* native Model 3 finite-diploid reproduction and parentage engine. The proposed full scientific hypothesis and its empirical limits are documented in [PR #609's source-ranked two-origin design](https://github.com/zuizui0223/izu-core/blob/paper/mechanism-narrative-20261019/docs/CHAPTER2_TWO_ORIGINS_ASSEMBLY_HYPOTHESIS_20261019.md). The corrected current macroecological target is the [Ch1 manuscript](https://github.com/zuizui0223/island/blob/main/submission/chapter1_current/MANUSCRIPT.md).

## Research question, NOT answered by these fixtures

> Is the insular enrichment of reproductive function (especially self-compatibility in Ch1) more attributable to source-lineage arrival/establishment/persistence sorting than to post-establishment evolutionary change, while floral investment and morphology show a different balance of pathways?

Neither an A-policy occupancy difference nor late A fixation in the current Model 3 identifies pre-arrival lineage filtering. Ch1's self-compatibility records are not the same measure as the Model 3 autonomous-reproduction trait A. I models net floral investment, not literal colour or floral architecture. The current Ch1 species-level traits do not identify within-species island–mainland trait changes.

## What is implemented and bounded

**Executable:** `python -m scripts.chapter2_two_origins_technical_20261019 --technical-smoke --output /tmp/two_origins_smoke.json`. The command refuses a nontechnical / production mode.

- **Source candidates:** six artificial genotypes from `A_hint ∈ {0.25, 0.5, 0.75}` crossed with `I_hint ∈ {0.35, 0.65}`, each with independently seeded alleles, two starting propagules and recorded *actual* founding mean A/I. Each source genotype is stable across the two resets. The hint is not a measured self-compatibility class or an exact native phenotype.
- **Arrival lottery:** independent Bernoulli arrival with the same `p = 0.8` across lineages; no A-based dispersal rule. Attempted arrival and nonarrival are recorded separately from establishment and extinction, including all failed/empty cases.
- **Initial establishment, with an explicit neutral counterfactual:** one Model3 reproduction update using the unchanged maternal outcross, paternal pollen transfer, viable selfing and Mendelian recruitment operators. Compare (i) **native** establishment with the candidate's actual M/I/A expression against (ii) **trait-neutral establishment**, where M/I are expressed at 0.5 and A expression at 0.5 **in the initial reproduction ledger only**. In BOTH modes, offspring inherit the untouched original candidate alleles; matched sources, Bernoulli arrival draws and initial demographic RNG are retained. This removes the initial M/I/A phenotype-dependent reproductive difference in the technical reference and is *not* a null of all biological/phylogenetic filtering. All four subsequent A/I policy arms fork from the same establishment genotype **within each establishment mode**, before later clamps.
- **Persistence/evolution:** five later native reproduction/inheritance updates, zero adult carryover, no mutation or immigration. Two technical islands: zero-visitors with ovule budget 4.5 and four-visitors with budget 8; two independent arrival/demographic resets. Each lineage inhabits an **independent plot** on a labelled island; final plant assemblage is the sum of these **NONINTERACTING plots**, not a competition-aware community. The current native Model 3 has no lineage-specific resource-competition contract.
- **Two early filters × four interventions after establishment:** native evolving A/I; clamp A expression to source A0; clamp I expression to source I0 *in the reproduction ledger only*; clamp both. The underlying individual Mendelian I/A genotypes continue to be transmitted and can drift under clamps. Fixed A still allows selfing. These artificial expression clamps are **not** proof of total no-evolution, pure genetic mediation or empirical plasticity.
- **Output:** all 6×2×2×4 = **192** source lineage–island–reset–establishment-mode–post-establishment-policy rows, plus species-weighted stage means for A and I (no zero imputation when a stage is empty). Numbers from this fixture **are not scientific observations**, and its fixed grid must not be used to choose favourable parameters for later registered inference.

**One unit per record** is a candidate source lineage, not a founder replicate or independent island. Two resets with the SAME source genotype estimate conditional demographic/arrival variation only. They do not demonstrate predictability for a held-out lineage. No lineage-level predictive model is fitted. The strict proper-score helper is a future evaluator, not evidence of a predictive result.

The neutral-establishment counterfactual is **defined** rather than estimated post hoc. It permits a technical comparison of trait-dependent initial reproduction while protecting the original candidate genotype, but the fixture is too small and outcome-exposed to infer a general colonization law. A truly neutral *arrival* null is already provided by identical arrival probabilities, and an interaction-aware species community still needs a new contract.

## Model-3-exact *conditional* establishment probability (technical v2)

The native kernel used in this fixture has zero adult carryover, zero immigration and capacity 12. For **every source candidate**, even one that did not arrive, evaluate the initial expected number of successful resident recruits \(\Lambda=\sum_{m,f}\mathbb E[\text{outcross offspring}_{fm}]+\sum_m\mathbb E[\text{viable selfed offspring}_m]\) using the **unchanged** Model3 reproductive ledger. The subsequent native recruitment step draws a Poisson count with mean \(\Lambda\), so with a positive vacancy count, the one-update establishment probability conditional on arrival is exactly

\[
P(\mathrm{establish}\mid\mathrm{arrive},\mathrm{source\ genotype},\mathrm{island})=1-\exp(-\Lambda).
\]

It is not a fitted regression, new scientific result, guaranteed establishment or proof of determinism. Arrival remains a separate randomized event with a known trial probability. The output records both \(\Lambda\) and this **counterfactual probability** even for source candidates whose arrival lottery fails; it never imputes nonarrival as biological failure after establishment.

**Matched descendant random numbers (v2 correction).** Source genotype, arrival event and initial establishment random streams were already paired. The first technical version gave later policies different demographic RNG masters, which added avoidable random-stream differences to comparisons. Technical v2 initializes each later policy from the **same master RNG seed** for a given source lineage/island/reset, also shared across the two initial filter arms. This is common-random-number coupling, **not** event-by-event synchronization after branch divergence. The RNG master's hex identifier is emitted for every arm and source tests verify that all eight assignments to a lineage-island-reset share it. The technical protocol token changed from `two-origins-technical-20261019-v1` to `two-origins-technical-20261019-v2`, so the old two-reset smoke cannot be compared as though it were a replication of the same random source streams.

A [PR #610-only GitHub Actions gate](../.github/workflows/two-origins-technical.yml) now runs the single, bounded technical fixture and its tests on a pinned Python numerical environment; it explicitly rejects publication inference. No `island`/Chapter1 empirical data are reproduced or collected by this gate.

## Exact stage accounting

For either trait z in {A,I}, under a nonempty chain define:

```
source all-candidate mean                     z0
arrived-lineage source mean                  zarr
established-lineage source mean              zest
survivors' ORIGINAL source mean              zsurv0
survivors' current expressed mean            zsurvT

zsurvT - z0
 = (zarr   - z0)      arrival composition
 + (zest   - zarr)    early establishment filtering
 + (zsurv0 - zest)    later persistence filtering
 + (zsurvT - zsurv0)  within retained-lineage change
```

The stage means are equal-weighted **species/lineage** means (not abundance-weighted individuals). The survivor reference is the *candidate source genotype before the first founding reproductive update*, so all within-lineage evolution since arrival is in the last term. Establishment itself may involve Mendelian genetic change; the four terms are **descriptive composition accounting, not four identified mutually independent causal mediators**. Clamps and genotype trajectories can alter who persists. The counterfactual composition effect is thus not uniquely allocated without an explicit factorial intervention interpretation.

If an island has no arrivals, no establishments or no survivors, means for the empty stage are **undefined**, never forced to zero; separately analyse probability of an empty island. If late immigration is added later, include a separate term rather than changing the denominator without accounting.

## Testing

`pytest -q tests/test_chapter2_two_origins_technical_20261019.py`

Tests verify source-arrival/fork pairing across interventions; exact lineage-status denominators; stage-telescoping arithmetic (including synthetic independent known values); absent-arrival handling; clamp output semantics; seeded reproducibility; invalid contract fail-closed; and proper Brier/log-loss formulas. Passing tests certifies **only the technical contract** of this prospective machinery.

The source biology used by this module is not a new genomic model or scientific replication of earlier 160×160: `scripts/model3_island/types.py`, `reproduction.py`, `population.py` and `randomness.py` remain untouched.

## Next scientific admission gate (not authorized by smoke success)

1. Define a **real lineage pool** and source trait distributions independently of results; separately identify **probability of arrival**, **founder genotype sampled among propagules**, one-generation establishment and later persistence. Calibrate SC/autofertility interpretation: a continuous A is not the observed binary self-compatibility trait.
2. Include a clearly declared cross-lineage resource/competition and heterospecific pollinator-interference mechanism, **or** frame an explicit independently surviving-lineage null; do not call a noninteracting pool a native multispecies assembly process.
3. Prospective matched source pool × island/environment × demographic replicate design; strict held-out source lineages and islands. Reserve a distinct confirmation RNG namespace, source SHA, fixed observation horizon, biological minimum effect and power/budget gate before *any* new scientific outcomes are inspected.
4. Evaluate *individual lineage* arrival/establishment/persistence with calibrated held-out Brier/log-loss relative to arrival-opportunity/taxonomic/trait-neutral baselines. Analyse *archipelago composition* and within-lineage A/I changes using repeated **complete candidate-source** draws. Distinguish average stability from true individual-level predictability.
5. Compare a controlled trait-neutral arrival/establishment filter, separate A and I post-establishment expression interventions and natural inherited dynamics. Test the predicted A-sorting / I-evolution asymmetry against its null and opposite outcomes rather than hard-coding that result.
6. Independently assemble population-level island–mainland phenotype/genome observations. The corrected Ch1 species-level trait database is not a paired-population dataset, and same-species contrasts can still reflect founder-genotype filtering rather than only within-island selection.

## Exclusions

No biological publication claim, universal sorting-versus-evolution asymmetry, species-level immigration success classification, evolutionary order, positive reproductive-service spillover, permanent irreversibility, postulated natural trait values, island-wide geographic threshold, or island-versus-mainland within-species contrast can be derived from this technical sample. Keep the registered G/S readouts and Q2 `both_inconclusive` unaltered, with only one active Chapter 2 Article.
