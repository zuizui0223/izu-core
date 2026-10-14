# Post-isolation allele-state transplant: island adaptation, payoff and persistence (2026-10-08)

**Scientific state:** exploratory four-visitor-history discovery followed by one **prospectively frozen, new 16-history, targeted test that FAILED its global sign-and-bootstrap gate**. Do not reclassify the failure using favourable secondary contrasts. This work is on Draft PR #413 and does not amend the prospectively confirmed four-setting assurance feedback from merged PR #411.

## Why this is the next island-ecological mechanism

The original problem is not simply whether a plant evolves greater selfing capacity before smaller floral investment. A history of low visitor replenishment changes outcross return and viable selfing opportunity, then changes the inherited population state. Later, even under **the same present visitor process**, that state may alter both immediate female/paternal reproduction and finite-population persistence.

The prior mutation-access timing work showed the intended phenotypic order in most histories, but **failed independent16 confirmation of a predicted mating-system-specific survival sign contrast**. A balanced mutation-supply-duration follow-up had pooled four-setting mean zero. Hence timing is a weak standalone explanation. We instead manipulate **which posthistory alleles are present at the start of a common future demographic test**.

## Intervention and identification boundary

Each reproductive setting starts with identical founders. Near and far visitor replenishment produce two 400-update inherited populations. After identically seeded eight-plant bottlenecks, on each of the **near or far recipient genetic backgrounds**, we cross two donor factors:

- **Investment donor:** native near-history versus evolved far-history pair of diploid investment alleles
- **Assurance donor:** native near-history versus evolved far-history pair of diploid assurance alleles

Donor individuals are aligned to recipient individuals by stable **within-locus phenotype rank**. The recipient matching/access locus remains unchanged. Both alleles, origin markers and mutation flags are transferred together. Thus the manipulation **retains the donor's actual standing locus variation** rather than clamping all eight recipients to a single mean. A native/native treatment is bitwise equal to the unmodified recipient.

The common future visitor histories, population ceiling (8), reproductive budgets (3 and 4), and 80-update postshock random streams are held matched across all four factorial donor combinations. There is **no plant immigration**.

This is an intervention on **locus-level inherited distributions**, not an isolated intervention on trait mean or a clean mediation fraction. It may also change inter-locus covariance, which allele identities are carried, and epistasis/trait matching. The small-population stress budgets came from previously exposed pilot work; none represents measured island demography.

## The exploratory four-history result

Four independent visitor histories, one demographic repeat, 128 genetic states and 512 postshock trajectories. On the recipient **near-history background**:

| Reproductive setting | Assurance donor effect on immediate viable maternal output | Assurance donor effect on 80-update occupancy |
|---|---:|---:|
| Delayed control | +0.127 | +0.063 |
| Prior selfing | +0.076 | −0.063 |
| Pollen discount | +0.152 | +0.219 |
| Direct assurance cost | +0.058 | 0.000 |

This suggested a contrast between pollen-discount and prior-selfing mating systems, but was too small to determine generality. After reading these outcomes, we froze a new 16-history cohort and **one** specific sign test before using its outcomes.

## New 16-history independent frozen test (2,048 postshock trajectories)

- New visitor seeds: 35100801–35100816; one nested demographic repeat per history
- 64 paired historical near/far populations, 128 recipient backgrounds, 512 factorial allele states, 2,048 poststress trajectories
- 9,999 history-bootstrap replicates, seed 3510082026
- Frozen primary: on **near-history recipient backgrounds**, pollen-discount minus prior-selfing **assurance-donor marginal effect on occupancy**, averaging both investment donor levels and all four stress/visitor conditions. Require mean and bootstrap 95% lower endpoint positive.

**Outcome: primary FAILED.** Difference **+0.140625**, history bootstrap 95% **[−0.078125,+0.359375]**. The interval includes zero; a positive point estimate does not meet the frozen rule.

### Secondary, setting-complete estimates

Each cell gives the **effect of replacing near-history assurance alleles with far-history assurance alleles**, averaged across near/far investment donor levels and the full four-condition postshock grid.

| Setting | Near-recipient occupancy effect [95% history bootstrap] | Far-recipient occupancy effect [95% history bootstrap] |
|---|---:|---:|
| Delayed control | +0.297 [+0.133,+0.461] | +0.281 [+0.094,+0.469] |
| Prior selfing | +0.180 [+0.070,+0.297] | +0.234 [+0.086,+0.383] |
| Pollen discount | +0.320 [+0.156,+0.492] | +0.297 [+0.141,+0.445] |
| Direct assurance cost | +0.047 [0.000,+0.094] | +0.039 [−0.008,+0.086] |

These **secondary** results point to a stronger effect in the three settings without direct assurance allocation cost, but they were not the single preregistered success criterion and were obtained using a highly specific synthetic stress grid.

The average far-history-minus-near-history trait difference among **native bottleneck populations** was:

| Setting | Investment I | Assurance A |
|---|---:|---:|
| Delayed control | −0.228 | +0.132 |
| Prior selfing | −0.088 | +0.115 |
| Pollen discount | −0.112 | +0.171 |
| Direct assurance cost | −0.235 | +0.128 |

The intervention therefore transfers, on average, higher-assurance and lower-investment inherited alleles from the low-replenishment history; the sign is not unanimous across the 16 histories. Its immediate viable maternal benefit was positive in all four settings (from +0.040 to +0.251 across recipient backgrounds), while occupancy depended strongly on the mating-system cost structure.

## What is now resolved — and what is not

1. **Confirmed independently in the prior #411 campaign:** floral investment declines under low visitor replenishment without evolving assurance; evolving assurance compresses high–low floral-investment divergence mainly through stronger high-replenishment decline.
2. **Current targeted 16-history transplant:** an inherited assurance-allele distribution can modify immediate reproductive output and later occupancy in a specified finite demographic regime. The exploratory secondary effects support this mechanism; **the prespecified between-mating-system difference was not confirmed**.
3. **Not identified:** the precise mediation of all evolving-genetic covariance, population genetic potential, the effect of *observed temporal trait-change order*, real island extinction risk or causal effect of island-colonization filters.

The island ecology hypothesis is therefore sharper than a generic selfing-syndrome narrative: **the same present pollinator community can interact differently with historically evolved, multi-trait inherited population states.** But a clean future test must separately identify which allele changes carry the effect and how the outcome depends on demographic stress without choosing the stress threshold from observed results.

## Reproducibility / claim firewall

- Designs: `data/design/chapter2_island_genetic_state_transplant_pilot_20261008.json` and `...independent16_20261008.json`
- Results: `data/results/chapter2_island_genetic_state_transplant_pilot_20261008.json` and `...independent16_20261008.json`
- Replayers: `scripts/run_chapter2_island_genetic_state_transplant.py`, `...independent16.py`, and `scripts/summarize_chapter2_island_genetic_state_transplant_independent16.py`
- Raw exploratory ZIP SHA-256 `6b4416515cf8eb3048ecf4ee1ae87e51ebaa76d5759275471adba2df15397c04`
- Raw independent16 ZIP SHA-256 `0213d9ca1a39cd49891bf71706230942b1095d1f62b9bd1cfe1549c00c8fb442`
- Independent16 raw single-file SHA-256 `44a00313654d347bb29c0500e5f562472adec9b6cd74441c57c8d6cef1ac3fd6`
- Both ZIPs include the archived original 2026-10-06 biological source snapshot, SHA-256 `71a1b1d9c4d683b874c989fa7768a14e72c5353063d8213cbe42f42cd37473d4`. ZIPs are locally archived, **not DOI deposited**.
- An isolated manual-only GitHub Actions full 16-history replay is written, but is **not reported as having completed**. The new tests are included in the existing PR scientific gate.

Keep PR #413 Draft and all failed gates visible. Do **not** move the allele-transplant finding into the Ecology Letters primary abstract before causal and source-independent challenges.
