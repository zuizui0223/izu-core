# Appendix S20. Finite-community system-size audit

## S20.1 Rationale

The Chapter 2 model contains two different mathematical layers. Pollinator communities follow a finite stochastic Markov process in which individual partners are lost and new partners arrive. Conditional on one realized pollinator trajectory, plant-state motion is deterministic; the 21 starting positions sample that conditional flow rather than interacting as plant agents. A deterministic mean-field reduction would therefore average over the community-realization component that is itself one focal quantity in the response decomposition.

This does not imply that a PDE description is impossible. An exact distributional master-equation representation exists in principle, and diffusion or linear-noise approximations may be useful in large systems. The present audit instead asks a narrower model-internal question: how much of the observed branching is attributable to finite-community sampling over the declared model class?

## S20.2 Prespecified system-size scaling

The design was frozen before execution in `data/design/chapter2_finite_community_system_size_freeze_20260908.json`. We used the zero-trait-adjustment submodel to isolate community-composition sampling from adaptive plant-state motion. For each scenario and realization, k independent copies of the unchanged finite-community Markov process were generated and their extant partners pooled before service was evaluated. We used k = 1, 2, 4, 8 and 16, the same six prespecified seeds as the relational-robustness audit, 96 matched community realizations per seed and the unchanged 21-point trait grid.

Pooling changes neither per-copy partner arrival/loss probabilities nor pollinator trait, breadth, generalist or replacement distributions. Because service remains based on mean extant-partner match, increasing k does not increase service merely by increasing abundance. It reduces finite-community compositional sampling and empty-community probability while preserving the expected scenario-level partner mixture.

## S20.3 Results

| pooled copies k | island-like final-count CV range | island-like empty-final fraction | mixed realizations / 96 | community-realization SS fraction | state × community non-additivity fraction |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.575–0.691 | 7.3–13.5% | 64–75 | 51.4–67.3% | 32.5–48.2% |
| 2 | 0.404–0.489 | 0–2.1% | 71–78 | 32.5–52.1% | 46.4–64.1% |
| 4 | 0.285–0.355 | 0% | 67–74 | 26.5–34.2% | 61.3–67.7% |
| 8 | 0.219–0.239 | 0% | 57–75 | 23.9–35.9% | 56.7–67.4% |
| 16 | 0.134–0.172 | 0% | 44–60 | 20.3–34.5% | 50.6–65.4% |

Finite-community count variation and empty-community events declined sharply with k, and the additive community-realization share was substantially smaller at k=16 than at k=1. Mixed individual response geometry nevertheless remained common at k=16, and the relative state × community non-additive component remained large. Within this audited range, finite-community sampling therefore contributes materially to realization variance but is not sufficient to explain response branching.

## S20.4 Claim boundary

This is not an exact mean-field, master-equation, Fokker–Planck or linear-noise calculation. k=16 remains finite, and the audit does not identify a population-size threshold at which an analytical approximation becomes valid. The result is a model-internal system-size diagnostic and not a natural pollinator abundance estimate. A formal finite-N-to-mean-field approximation study is left outside Chapter 2.
