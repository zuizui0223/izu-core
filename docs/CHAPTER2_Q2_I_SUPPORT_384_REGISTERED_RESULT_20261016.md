# Q2 — 384 registered diploid histories: I-allele carrier assignment and realized response order (2026-10-16)

**Registered scientific verdict: `both_inconclusive`.** This is the *completed new* prospective native Model 3 evolutionary intervention, not a technical 12-update smoke test. Both co-primary Bonferroni-corrected intervals include zero. The estimated effects are positive but **do not meet the preregistered confirmation rule**. No missing histories were excluded and no post-outcome seeds, settings, cutoffs or experiment arms were added.

**Machine-readable evidence:** [full readout with six classifications](audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json); original [Actions execution #38918737325](https://github.com/zuizui0223/izu-core/actions/runs/38918737325), original [independent 384-case readout](https://github.com/zuizui0223/izu-core/actions/runs/38918737325/artifacts/12054486425), 32 separately retained original source-shard artifacts on the same Actions run. **This is 1 registered biological cohort, not 33 independent replications.**

## Experiment and identifiable intervention

The pre-outcome frozen [protocol](protocols/chapter2_q2_i_support_order_20261016.json) set 8 independent artificial founder-genotype draws × 8 exogenous visitor histories × 2 visitor-replenishment arms (`far` and `near`) × 3 I-locus genotype-distribution policies: **384 paths, 200 updates each**, 201 censuses. The plant census capacity was 48. Initial expressed M/I/A for every individual, paternal/maternal/autonomous-selfing ledger, ID and external visitor history were identical across policies *within each matched founder×visitor×environment*; the original scientific gate admitted all 128 possible t0 cells. Thus this is a controlled Model 3 policy assignment, **not a causal reconstruction of geographic mainland–island separation**.

| Initial I-locus policy | I allele half-width around 0.5 | Heterozygous carriers / 48 | Standing I alleles | Can reach founder-relative I decline 0.05 without new I alleles? |
| --- | ---: | ---: | --- | --- |
| `dense_reachable` | 0.078125 | 24 | 0.421875, 0.5, 0.578125 | Possible, not guaranteed |
| `sparse_reachable` | 0.078125 | 12 | 0.421875, 0.5, 0.578125 | Possible, not guaranteed |
| `dense_unreachable` | 0.046875 | 24 | 0.453125, 0.5, 0.546875 | **Structurally impossible** for decline ≥0.05 |

All founder I phenotypes are initially 0.5; the three policies do **not** freeze actual I thereafter. Both I mutation and seed immigration are disabled, while native M and A mutations and finite Mendelian transmission remain possible. With no new I alleles, the inherited allele set cannot expand. In `dense_unreachable`, all descendants' I must remain ≥0.453125, above the prespecified 0.45 target: the control's absence of I events is an **engineered logical negative control**. Carrier assignment changes frequencies, genotype composition and standing variance jointly even when the support set is identical; it is **not** an isolated genetic-variance mediation design.

A-first, I-first, near-simultaneous, A-only, I-only and neither were defined from founder-relative A increase ≥0.05 and I decline ≥0.05, each persisting for 20 occupied censuses, with starts within five updates called near-simultaneous. All starting paths remain in the denominator, including non-events and extinction if any occurred. `far` is the sole registered primary environment; `near` is secondary. Both are artificial pollen-limited regimes.

## Predeclared co-primary contrasts (far)

Let `D=P(A-first)-P(I-first)` count six-class **all-start** probabilities. The primary paired differences compare `dense_reachable - sparse_reachable` for both `D` and `P(I-event)`. Each contrast is averaged over an 8×8 founder-by-visitor grid. Inference resamples the **eight founder labels and eight visitor labels separately**, 9,999 draws, and uses two-sided Bonferroni-adjusted 97.5% percentile intervals for the two co-primary hypotheses. The registered **joint success requires *both* intervals exclude zero**.

| Primary contrast | Matched effect estimate | Familywise-adjusted interval | Predeclared verdict |
| --- | ---: | --- | --- |
| `ΔD` — A-first minus I-first score | **+0.109375** | **[−0.125000, +0.343750]** | **Inconclusive** |
| `ΔP(I-event)` — I decline incidence | **+0.187500** (18.75 pp) | **[−0.062500, +0.421875]** | **Inconclusive** |

**Overall: `both_inconclusive`**, not zero-effect equivalence, proven benefit, or failure of the underlying genetic inheritance theorem. The directions are positive as descriptive estimates; neither passed its registered adjusted interval gate. These 64 matched founder×visitor cells are **not 64 independent island systems**.

## All six realized order classes — no missing denominators

Each row contains 64 complete 200-update original histories. Every arm has **64/64 terminal occupancy**; occupancy here is a ceiling, *not* evidence of Q4 rescue.

| Environment | I policy | A-first | I-first | Within ±5 | A only | I only | Neither | I event / 64 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| far (primary) | dense reachable | 14 | 1 | 5 | 44 | 0 | 0 | **20** |
| far | sparse reachable | 6 | 0 | 2 | 56 | 0 | 0 | **8** |
| far | dense unreachable | 0 | 0 | 0 | 64 | 0 | 0 | **0** |
| near (secondary) | dense reachable | 5 | 0 | 2 | 53 | 0 | 4 | **7** |
| near | sparse reachable | 3 | 0 | 0 | 57 | 0 | 4 | **3** |
| near | dense unreachable | 0 | 0 | 0 | 60 | 0 | 4 | **0** |

The raw far I-event rates were 20/64 (**31.25%**) for dense and 8/64 (**12.5%**) for sparse. For matched far histories, **17/64 gained** an I event under dense versus sparse, **5/64 lost** an event, **3/64 had an event in both**, and **39/64 in neither**. Thus `(17−5)/64=+0.1875`, and even this artificial carrier-number intervention was **not monotonic for every individual future**. This paired re-tabulation is descriptive, not a newly registered third hypothesis or source of new sampling power.

The A-first-minus-I-first score difference is `[(14−1)−(6−0)]/64=+0.109375`; do not equate it with the difference in A-first counts `8/64`. In the eight founder labels, the descriptive order-score differences were `[+0.125, 0, 0, +0.500, 0, +0.125, −0.125, +0.250]`; one founder had the opposite sign. No post hoc founder exclusions or additional seeds are permitted.

## Source integrity and independent readback

- **Actual execution:** one explicit author-approved `workflow_dispatch` on `main` commit `f760f936b164df3dd3dceb9d9942d6b9805304eb`, [Actions run #38918737325](https://github.com/zuizui0223/izu-core/actions/runs/38918737325), marked **completed / success**. All 32 original-shard ZIP artifacts plus one independent full-readout artifact were uploaded (**33 Actions artifacts**).
- **Pinning:** frozen design SHA256 `f4edc17fcda3b76e3274d10538c152faa46d67c7c56486f9c679aebe3e70d709`, original biological/Q2 producer source-manifest SHA256 `69e6c2b789ff610214a46cbffd79e34c46ab0ee335ab20bc4e147443dd032030`, author activation SHA256 `714081dbb822ef8936a7fa9a6e63ec20f8284e95a58429010344cb05ddcb2e2a`. The source baseline separately SHA-pins 25 historical Model 3 files and rejects changed biology.
- **GitHub's execution-time independent consumer** required all 384 typed diploid source cases, rederived six categories with a separate scalar annual event loop, checked full typed genotype/parentage lineages and executed an optional **complete same-RNG native source-model replay**, which passed. This is an independent *reader and producer replay*, **not a new independent ecological model or second biological trial**.
- **Additional separate raw re-readback:** all **32 source-shard Actions ZIPs** were retrieved and their inner original source archives opened; all 384 original NPZ files and individual JSON receipt hashes were checked. Another read-only annual pedigree and I-homolog inheritance audit examined **76,800 inter-census transitions, 3,686,377 original offspring parentage records and 7,372,754 individual offspring I homologs**; I support never expanded and I mutation flags remained false. All 384 six-class outcomes, six-cell counts and the independent 9,999-draw two-axis bootstrap **exactly reproduced** GitHub's original readout. This reads the **same 384 original biological paths**, not new independent simulations.
- Original independent readout Actions ZIP: artifact `12054486425`, archive SHA256 `4ac98db1e04e8f9768f9d6a20717f40976ee96f9fcbebf51615be8f5bc28dbac`. The original GitHub Actions artifacts have time-limited retention (90 days), and **an independent durable DOI-backed external raw-data deposit remains unverified and must not be claimed**.

## What changed scientifically, and what did not

The exact support theorem holds under locus-specific no-I-mutation/no-immigration, and the structural control corroborates the registered negative bound. This prospective, phenotype-matched intervention additionally offers **positive descriptive changes** in I-event incidence and order, but the two registered co-primary cross-founder/visitor intervals **both overlap zero**. Therefore the stronger general claim that simply adding initial I-allele carriers reliably changes the A-first/I-first distribution **is not established** in this study.

Earlier Q2's A-half-width shift used two original founder backgrounds and bundled support, variance and threshold reachability; it is **not an independent confirmation** of this carrier-number experiment. Earlier Q3's 703 access-exclusion histories and the distinct 3/32 and 2/32 density–ABM ordering discrepancy remain **separate source cohorts**, with **no identified common mediation chain**. Nor does this 64/64-occupied experimental regime identify any Q4 survival benefit.

**Manuscript placement:** A short bounded registered Q2 negative/inconclusive-result paragraph and source link, without replacing the prior Q1 non-necessity result, original figures or S1–S33. The central ecological message is refined: *genetic access can exclude a specified trajectory, while the size and direction of a carrier-frequency effect on realized ordering remain contingent and not yet prospectively resolved*. Avoid claiming that initial genotype alone “determines” evolutionary order.

**Replication and data-handoff priority:** Preserve the 32 original archival ZIPs outside time-limited GitHub Actions before they expire, independently of the manuscript's existing DOI blocker. No new biological cases, post-outcome sample expansion, or p-value hunting are justified by `both_inconclusive`.
