# Stored genetic-variation clocks and fixation values

## Scope and source

This is a post-outcome read-only analysis of the completed 160 × 160 cohort, not another simulation or a new confirmatory experiment. [Actions run 39226906489](https://github.com/zuizui0223/izu-core/actions/runs/39226906489) completed the reader at source commit `386c035d`. All 97 original source assets were hash-checked. The output covers 25,600 founder–visitor crossings, two assurance policies, two budgets and three loci. Duplicate fork states are excluded from the 6,451,200 distinct saved state count.

Original protocol: [definitions and inference](protocols/CHAPTER2_VARIATION_CLOCK_READBACK_20261019.md). Machine-readable [results](audits/CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json) and [donor/seed transfer](audits/CHAPTER2_VARIATION_CLOCK_SEED_TRANSFER_20261019.json).

## Verification

[Independent review](audits/CHAPTER2_VARIATION_CLOCK_INDEPENDENT_REVIEW_20261019.json) verified all 32 output receipts, all 25,600 crossing summaries and occupancy curves, all 12 contrasts and family intervals, and all 64 seed cohorts. Twelve raw trajectories from three crossings were independently checked against source arrays; this sampled raw check is not a second exhaustive raw reanalysis.

The original Actions artifact is retained in the [draft release](https://github.com/zuizui0223/izu-core/releases/tag/untagged-918e4fde8af4206d79f4). This is retention, not an immutable DOI deposit. The workflow now supports manual dispatch only, matching repository trigger policy; the original completed PR-triggered run remains the provenance of these results.

## Main result

Assurance evolution does not uniformly exhaust the variation of other traits. Under B8, where every population survives, evolving assurance shortens the time with segregating I alleles by 2.628 updates and increases I fixation before census 80 by 3.551 percentage points. Under B4.5, it instead increases occupied-polymorphic duration for I and M, alongside a large survival difference. The latter is a combined persistence-and-variation outcome, not an isolated genetic mediation effect.

## When variation disappears

Each row starts with 25,600 populations. Fixation means one distinct allele value while occupied; extinction is a competing event, never counted as fixation. Median times below are conditional on fixation being observed before extinction and are not unconditional clocks. Duration counts occupied polymorphic censuses 0–79.

| Budget | Trait | Assurance history | Fixation before extinction | Median fixation census among events | Mean occupied-polymorphic duration | Extinct by 80 |
|---|---|---|---:|---:|---:|---:|
| B8 | M | fixed | 12,756 | 61 | 69.796 | 0 |
| B8 | M | evolving | 13,282 | 60 | 69.003 | 0 |
| B8 | I | fixed | 18,968 | 56 | 61.298 | 0 |
| B8 | I | evolving | 19,877 | 53 | 58.670 | 0 |
| B8 | A | fixed | 15,664 | 55 | 64.457 | 0 |
| B8 | A | evolving | 25,582 | 36 | 34.804 | 0 |
| B4p5 | M | fixed | 24,476 | 47 | 47.694 | 24,215 |
| B4p5 | M | evolving | 14,156 | 58 | 67.896 | 482 |
| B4p5 | I | fixed | 24,862 | 45 | 45.019 | 24,215 |
| B4p5 | I | evolving | 20,403 | 52 | 57.703 | 482 |
| B4p5 | A | fixed | 24,761 | 45 | 45.660 | 24,215 |
| B4p5 | A | evolving | 25,584 | 36 | 34.578 | 482 |

**Fixed A is fixed expression, not a genetically monomorphic locus.** Its expression is overridden to 0.5, but latent A alleles still segregate and transmit. The A-fixed rows describe those latent alleles. Initial allele richness differs between M and I/A, so their raw times cannot establish an intrinsic ranking of evolutionary predictability.

## Paired effects of allowing assurance evolution

Effects are evolving minus fixed within founder–visitor crossings. The intervals below use the predeclared post-outcome two-axis variance estimator, t159 and Bonferroni adjustment across 12 readouts. They are exploratory model-conditional uncertainty summaries; the 25,600 crossings are not independent replicates.

| Budget | Trait | Fixation incidence difference (percentage points; family 95% interval) | Occupied-polymorphic duration difference (updates; family 95% interval) |
|---|---|---:|---:|
| B8 | M | +2.055 [-0.184, +4.293] | -0.793 [-1.408, -0.177] |
| B8 | I | +3.551 [+1.606, +5.495] | -2.628 [-3.447, -1.809] |
| B8 | A | +38.742 [+37.188, +40.296] | -29.653 [-30.467, -28.839] |
| B4p5 | M | -40.312 [-42.106, -38.519] | +20.202 [+19.637, +20.767] |
| B4p5 | I | -17.418 [-18.794, -16.041] | +12.684 [+11.984, +13.383] |
| B4p5 | A | +3.215 [+2.657, +3.773] | -11.082 [-11.864, -10.299] |

B8 M-fixation incidence includes zero in its adjusted interval. B4.5 has 24,215 extinctions under fixed assurance and 482 under evolving assurance; its durations cannot separate survival benefits from changes in within-population fixation. Both effect directions must remain in the paper.

## Which value is fixed

Counts include fixation events followed by later extinction. M is continuous; its event-conditional distribution is retained in the JSON rather than reduced to a few allele bins.

| Budget | Trait | History | Fixed allele values: event counts |
|---|---|---|---|
| B8 | I | fixed | 0.375: 9,257; 0.5: 6,893; 0.625: 2,818 |
| B8 | I | evolving | 0.375: 11,393; 0.5: 6,437; 0.625: 2,047 |
| B8 | A | fixed | 0.25: 5,332; 0.5: 5,187; 0.75: 5,145 |
| B8 | A | evolving | 0.5: 275; 0.75: 25,307 |
| B4p5 | I | fixed | 0.375: 8,560; 0.5: 9,050; 0.625: 7,252 |
| B4p5 | I | evolving | 0.375: 11,464; 0.5: 6,638; 0.625: 2,301 |
| B4p5 | A | fixed | 0.25: 8,355; 0.5: 8,162; 0.75: 8,244 |
| B4p5 | A | evolving | 0.5: 361; 0.75: 25,223 |

In B8 evolving-assurance histories, 25,307 populations fixed A at 0.75 and 275 at 0.5; 18 remained polymorphic at census 80. I did not invariably fix low: 6,437 fixed at 0.5 and 2,047 at 0.625, compared with 11,393 at 0.375. A lack of subsequent I increase therefore does not by itself mean a population first reduced I and then failed to recover.

## Before versus during seed transfer

The 64 seed cohorts are nested within 32 donors (16 founder–visitor cells × two policies), not 64 independent historical populations. Counts of donor polymorphism below count cohort-source rows, with two rows per donor.

| History | Donor-polymorphic cohort sources (M/I/A) | Polymorphic seed cohorts (M/I/A) | New monomorphism during transfer (M/I/A) | Entry I at or above realized original-founder mean |
|---|---|---|---|---|
| fixed | 14/4/6 | 12/4/5 | 2/0/1 | 24/32 |
| evolving | 18/6/0 | 17/4/0 | 1/2/0 | 22/32 |

Most missing I polymorphism therefore predates the 12-seed transfer, although transfer eliminated it in two evolving-history cohorts. All evolving-history A cohorts were already monomorphic in their donors. Twenty-four fixed-history and 22 evolving-history seed cohorts entered at or above their own original-founder mean I. These observations distinguish target attainability, segregating variation and actual trait change.

## Claim boundary and relation to pollen limitation

The supported synthesis is conditional: assurance evolves while changing both persistence and the duration of standing variation; its effect on other loci depends on the demographic regime. These data do not prove irreversible evolution, genetic mediation, natural island filtering or a universal assurance-first clock.

This readback does not identify whether initial pollen limitation modifies the incremental A response to an additional decline in visitor activity. That separate frozen 384-path factorial is tracked in [PR #607](https://github.com/zuizui0223/izu-core/pull/607). Its results must be recovered or, after excluding duplicate execution, generated and audited before the manuscript adopts that claim. No unobserved factorial result is supplied here.
