# Q3→Q4 no-visitor falsifier: pollinator availability changes the survival contrast

**2026-10-11 | Source-native, post-discovery, single synthetic Model 3 family.** This is a falsifier of a simplified narrative, not independent confirmation of extinction caused by genetic evolution.

## Research question

The restored scientific structure is **閾値 → 順序 → 実現 → 帰結**. Under inherited investment variation, does genotype-dependent investment always lower population survival? Is the negative Q3→Q4 contrast caused by a general reproductive allocation cost, or is it contingent on whether conspecific pollen transfer is available?

The experiment holds the original K8/B48, eight founding `0.20/0.50` heterozygotes (initial expressed investment 0.35), four mating rules, no mutation, no immigration, zero adult survival and the original source Poisson recruitment fixed. Only the **visitor context** is changed:

- `visitors4`: previously exposed four synthetic visitor functional types, fixed through the 80-year experiment.
- `visitors0`: empty visitor state. The original Model 3 reproductive ledger must then give **exactly zero pollen transfer, zero maternal outcross, and no pollen-mediated nonfocal benefit**. Selfing remains as defined by the original setting.

For each context compare the 165-state exact inherited-genotype Markov process under (i) native genotype-dependent investment expression, (ii) expression set to 0.35 while alleles keep segregating. The numerical parameters are historical synthetic cases **budget 6 or 8**, chosen from earlier exploration; not environmental measurements or new independently reserved visitor histories.

## Source-matched results at budget 6

| Reproductive rule | ΔP80 with 4 visitors | ΔP80 with 0 visitors |
|---|---:|---:|
| Delayed selfing | −0.00397082 | **+0.00325650** |
| Prior selfing | −0.00122373 | **+0.00325650** |
| Pollen discount | −0.00022277 | **+0.00325650** |
| Assurance cost | −0.00053182 | **+0.00033296** |

Here `ΔP80 = P(occupied80 | native genotype expression) − P(occupied80 | fixed expression)`; values are absolute probabilities, not percentages or sampling confidence intervals.

In this specific budget6 example, allowing inherited investment to affect expression has a **negative** occupancy contrast with artificial visitor-mediated outcross reproduction, but a **positive** contrast without visitors. The three no-discount, cost-free-assurance settings become mathematically identical with no visitors, because their differences in selfing timing and pollen discount no longer alter the original no-outcross seed ledger. The direct assurance-cost rule still changes resource expenditure.

**This is a source-level ecological sign reversal, not evidence that a naturally evolving plant causes pollinator disappearance or that pollinator arrival changes with flower investment.** Visitors are externally prescribed and static; there is no feedback from flower investment to insect population demography.

## Crucial null at budget 8: visitor absence is NOT sufficient to predict the sign

| Reproductive rule | ΔP80 with 0 visitors, budget 8 |
|---|---:|
| Delayed selfing | −0.01256875 |
| Prior selfing | −0.01256875 |
| Pollen discount | −0.01256875 |
| Assurance cost | **+0.01228423** |

Even though zero visitors guarantees zero outcross and zero nonfocal pollen externality, the long-run consequence of inherited investment expression still depends on ovule budget and mating-system cost. Therefore, neither 'zero visitors rescues population survival' nor 'all inherited investment variation reduces survival' is defensible as a general ecological claim.

## Interpretation under the four-question hierarchy

- **Q1 — Threshold:** Different visitor contexts and allocation budgets change reproductive fitness payoffs. Zero visitor pollen contribution is a stringent original-model negative control for claims requiring pollinator-mediated benefits.
- **Q2 — Order:** No genomic mutation-access or A-first/I-first order is manipulated. Reproductive selfing timing is a mating rule, not inherited evolutionary order.
- **Q3 — Realization:** The exact parent-pair and Mendelian `0.20/0.50` genotype classes transmit even in the expression-clamped control. This is not an evolutionary freeze, and the fixed initial phenotype masks standing genetic variance.
- **Q4 — Consequence:** Model 3's 80-update occupancy response can change sign between visitor contexts because seed intensity and inherited genotype composition feed back through the Poisson cap over generations. It is not reducible to a one-year pollen-transfer sign or a universal 'tragedy of commons'.

Source calculations integrate the original `reproduce_kb`, unchanged parent-sex outcross matrix, viable selfing, original (R=\min(\operatorname{Poisson}(\mu), K)) census cap and the 165-state multinomial Mendelian genotype distribution. The numeric alleles are the original fixed `0.20/0.50` source, but gamete identity is coded by **genotype class**, not equality to a hardcoded allele number (guarding against the issue corrected in PR #466).

## Reproducibility and evidence limit

- Runner: `scripts/audit_chapter2_q3q4_no_visitor_20261011.py`.
- Tests: `tests/test_chapter2_q3q4_no_visitor_20261011.py` — zero pollen/outcross, three-source equivalence without visitors, K8 first-generation genotype identity, row stochasticity, complete 4×2×2 scope and budget8 counterexamples.
- Parent model foundation: merged PR #464 original source genomic/seed-operator factorial. PR #465 (time), PR #466 (width) remain distinct source models, not external ecological replication.
- **No new simulated visitor histories, external species, observations or prospective hypothesis tests.** The supported interpretation is a mechanism-generating demonstration *within the synthetic Model 3*. No reclassification of confirmed #411/#442, no manuscript replacement and no evolutionary-suicide headline.
