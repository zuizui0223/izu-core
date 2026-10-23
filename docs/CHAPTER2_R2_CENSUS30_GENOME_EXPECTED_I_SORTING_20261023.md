# R2: recover original full census-30 genotypes before inferring I selection versus stochastic realization

**2026-10-23 — source-exact technical replay and static expected-parentage diagnostic, NOT new future evolution or independent confirmation.** This note is a **stacked follow-up** to the original 384-pair and A/M-fixed source audits (#630–#632). Existing R1–R5 evidence ranks, the independently founded R2 overall INCONCLUSIVE result and the registered R4 G/S remain unchanged.

## Remaining scientific identifiability problem

A fixed A locus and a fixed M locus do not prevent I from diverging in the original Model 3. In the 22 strong-history A/M-fixed, I-polymorphic paired cases, decline leads to I fixation in 22/22 futures versus 13/22 maintained controls. Those counts do **not** tell us how much I sorting is due to genotype-weighted reproductive expectation versus random draws and Mendelian segregation. The original archived 384 source ZIP retains census30 **allele support and a complete genome fingerprint**, but not all 48 plants' per-locus genotypes at every intervening update.

The original frozen 384 producer is itself deterministic given its initial seed, demographic stream and immutable native Model 3 code. Therefore **the full census30 diploid genomes can be reconstructed exactly**, rather than replaced by synthetic genotypes guessed from allele frequencies. This is a technical source replay of the same biological data, not new independently sampled founder or visitor histories.

## Source-lock and admission before calculation

The immutable roster records **all 24** (22 strong + 2 weak prior pollen limitation) native census30 source cells in which A and M are already monomorphic but I is still polymorphic. Its records include frozen initial A, visitor baseline, original founder and nested demographic-repeat seeds, original census30 full state SHA256, and original terminal full state SHA256 of *both* future arms, all transcribed from the source ZIP that independently passed original ZIP SHA/manifest verification in #630.

The new script:
1. Loads the original 2026-10-19 frozen protocol and **verifies all original native source operator Git blob SHAs** through the unchanged pilot's admission function.
2. Replays only **30 original historical Model 3 generations** for each of the **24 source cells**, with original source founders, visitor panels, demographic RNG and original native `advance`.
3. Fails if **any exact census30 complete-genome fingerprint** differs from the authenticated original source ZIP roster; also checks original 24/11-source, A/M monomorphism and I segregating status.
4. From each recovered source genotype, invokes only the **original deterministic one-generation `reproduce` ledger** under maintained activity (0.40) or imposed decline (0.04) with exactly the same source state. It performs **no additional population step or offspring draw after census30**.

No individual source genotype is independently inferred from aggregate allele frequencies, and no original biological source/model file is edited.

## Exact expected one-generation I offspring mean

For plant i with expressed I_i, the source ledger's pollen-related `outcross[f,m]` is the weight of a viable outcross offspring whose **father** is f and **mother** is m; `self_viable[i]` supplies a selfed offspring of parent i.

If every newborn inherits one Mendelian I allele from each parent and no mutation occurs, its **expected expressed I** at the next census, conditional on positive resident recruitment, is

    E[I_child | current state and source expected parentage]
      = { Σ_{f,m} outcross[f,m] * (I_f + I_m)/2
          + Σ_i self_viable[i] * I_i }
        / { Σ_{f,m} outcross[f,m] + Σ_i self_viable[i] }.

Its *immediate reproductive sorting differential* is

    S_I = E[I_child | current state] − mean_i(I_i).

The fixed-state treatment contrast is `S_I(decline) − S_I(control)`. The source reader calculates this twice with independent, algebraically equivalent donor/recipient and ordered-parent matrix formulas and fails closed on disagreement. This is **a genotype-weighted conditional expectation under the full native father+mother+self return**, not the naïve derivative of total group seeds or maternal-only fecundity.

At census30, the original source-paired external pollen treatment differs, but resident **A, M, I, genotypes and full ancestry are all byte-identical**. Thus the contrast in S_I is a genuine native Model 3 **one-generation expectation difference** for each originally archived source state.

## Limits: not yet a 50-generation selection-versus-drift decomposition

A future stochastic 50-update trajectory has path-dependent mating environments, allele frequencies and reproduction. One initial conditional expected shift is **not** its long-run selection coefficient, selection/drift fraction, realized fixation probability or genetic causal mediation. A complete 50-generation pathwise decomposition would require reproducing the actual full sequence of genotypes and computing expected offspring I for **each visited state**, plus a residual for sampling/segregation. That can be attempted now that source genome reconstruction is possible, but such a pathwise identity would still not uniquely isolate a causal "drift share" without a well-defined counterfactual.

The audited original 24 cells derive from only **11 founder seeds**, selected after exploratory R2 outcomes. Results must remain post-outcome conditional source diagnostics, not new randomized founder experiments, new environmental calibration, or conclusions about naturally isolated islands. A full independent stochastic replicate campaign still needs separately specified source axes, a prespecified meaningful effect threshold, replication unit and author-approved execution gate in the existing unapproved prospective proposal.

## Reproduce and verifiable output

- Original producer: `scripts/chapter2_pollen_baseline_factorial_20261019.py`
- Exact source-checkpoint roster: `data/design/chapter2_r2_original_384_strict_AM_prefixes_20261023.csv`
- New expected-genetic-sorting reader: `scripts/audit_chapter2_r2_shock_genome_expected_I_20261023.py`
- Dedicated tests: `tests/test_chapter2_r2_shock_genome_expected_I_20261023.py`
- The PR scientific author-review CI runs the source-exact replay and archives `R2_CENSUS30_EXPECTED_I_SORTING.json` with source and immutable protocol IDs.

Commands:

    python -m pytest -q tests/test_chapter2_r2_shock_genome_expected_I_20261023.py
    python -m scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 > /tmp/R2_CENSUS30_EXPECTED_I_SORTING.json

**Execution scope:** 24 × 30 deterministic *original-source replays*, **zero** newly generated future populations, **zero** new prospective statistical tests, and no fabricated individual genomes.
