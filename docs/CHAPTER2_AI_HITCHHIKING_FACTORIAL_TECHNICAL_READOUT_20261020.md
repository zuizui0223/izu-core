# A mutation × I payoff × I genotype reassignment — original 6-policy technical readout

**2026-10-20 | retrospective source-locked ENGINEERING result, not preregistered science, ecological replication, independent Q1 founder confirmation or proof of A–I hitchhiking.** Source head `f2c3c1f9e635fb7a84407cdc36ba683b14a793ed`, [GitHub Actions scientific gate #39365572081](https://github.com/zuizui0223/izu-core/actions/runs/39365572081), original `scientific-gate` job `118441580441`. Its focused [source tests](../tests/test_chapter2_ai_hitchhiking_factorial_technical_20261020.py) completed **success**, including exact source Q1 reproductive trace/genome parity for A-on and A-off native-I cases and identical A/M genotypes and offspring self/outcross totals between I-neutral unshuffled and I-neutral whole-I-diplotype-reshuffled cases. General workflow and broader CI are separate checks and must not be assumed green for future commits merely because this focused step succeeded.

## Exact intervention, denominator and negative controls

- **Old exposed artificial source contexts:** two original PR569 founder genomes × two original visitor histories × near/far arms × two original Q1 mating settings = **16** source contexts (four founder×visitor crosses per setting/arm). No independent new biological source samples.
- **6 policies/context** × 24 updates = **96 synthetic intervention paths**. All **4/4** paths in every setting/arm/policy reached update24 alive, so there is no differential survivor restriction **in this narrow short trial**; all reported conditional means equal the all-start means in their own four-context group.
- `Aon/Aoff` toggles only de novo A mutation; M/I continue their original mutation and separate-locus Mendelian inheritance. Initial A is 0.5 for every source allele. The `Aon_Inative` source exactly reproduces original Q1 `evolving` and `Aoff_Inative` exactly reproduces original Q1 `fixed` source genome and trace over 24 updates (fixed still allows selfing).
- `Ineutral` sets expressed I=.5 **only in the original reproduction ledger**, disabling the modeled direct I cost/affinity benefit while the real I genotype continues mutating and transmitting. `Ineutral_scramble` additionally reassigns entire I diploid genotypes among plants **at every generation** before reproduction. It preserves whole-I-diplotype marginals, full A/M genotype paths and offspring counts, but artificially breaks **both A–I and M–I associations**. This is NOT a physical recombination test or A-only causal mediation.

## Direct observed short-horizon response

Each table cell gives source-group mean `I_terminal − I_original_founder` in true inherited Model3 I units, among the four surviving context-specific source trajectories. At t24 all four survived in every arm.

| Q1 mating & visitor regime | Native I direct payoff: A-on−A-off | I-neutral payoff: A-on−A-off | I-neutral + yearly I-diplotype shuffle: A-on−A-off | Association-sensitive difference = (I-neutral A-effect)−(shuffle A-effect) |
| --- | ---: | ---: | ---: | ---: |
| Delayed control, near | **−0.059386** | **+0.050356** | +0.024860 | +0.025497 |
| Delayed control, far | **−0.069157** | **+0.121140** | +0.029402 | +0.091738 |
| Direct assurance cost, near | **−0.020372** | **+0.056884** | **−0.056763** | +0.113647 |
| Direct assurance cost, far | +0.004978 | +0.047344 | +0.044256 | +0.003088 |

All numeric cells are exact arithmetic contrasts of original gate printed group means (source path head above; displayed to 6 decimal places), not newly calculated source mutations or a new CI. They are **effects of specified model interventions on technical group mean endpoints**, not isolated indirect A→I fitness contributions. The matched 4×6 source I deltas themselves are printed in that job log, with source parity controls.

## Interpretation: not a universal directed hitchhiking result

- Removing I's direct modeled reproductive payoff **changes** A-on−A-off I differences, including their signs. Under I-neutralized source reproduction, the A mutation switch altered I group means in all four old-source contexts (positive technical contrasts +0.047 to +0.121). This is **compatible with indirect transmission**, but A-origin effects and finite family sampling remain confounded; the source event pedigree was not causally coupled to each mutation in this factorial.
- Scrambling the I genotype each generation changes these contrasts substantially (especially costly-assurance near), while A/M genotype histories and self/outcross offspring counts are **verified identical within the paired I-neutral A-policy branches**. This confirms that I genetic **placement** can affect realized I endpoints even with no direct I payoff. However I scrambling disrupts M–I as well as A–I parent associations and family persistence, so its contrast cannot uniquely be attributed to the original A mutation hitchhiking hypothesis.
- The association-sensitive difference is positive in all four *exposed*, technically constructed contexts but ranges **+0.0031 to +0.1136**. There are only 2 founders ×2 visitor histories per setting/arm; these are not independent natural taxa or prospectively sampled ecological cases and are not a robustness or statistically powered finding. Individual sources and stochastic realizations may disagree.
- The short 24-update A mean remains near 0.5 because all original founders start A=.5 and de novo mutations are sparse. This is not an A sweep, directional fixation, classic linkage block or cause of original PR569 1000-update sign variation.
- A mutation off does **not** stop I or M evolution; with I expressed neutrally, I can still change through finite Mendelian sampling, M-associated parent selection, and mutation. Source traces and I traits are not a validated stochastic ensemble mean.
- Changing the payoff rule or annually scrambling genotypes are declared **synthetic interventions**, not unaltered nature. No mutation event origin advantage, natural island sorting, 1000-update Q1 mechanism or positive ecological adaptation has been established.

## Best next discriminating synthetic negative control

**Before new external-source biological confirmation**, hold BOTH M and I expression fixed at a common reproductive value (but leave their true inherited genotypes and mutation dynamics intact), so parental fitness is driven by modeled A rather than I and M. Compare A-mutation on/off with unshuffled/shuffled I in this explicitly artificial **M+I payoff-neutral** control, require A/M and offspring-path pairing, and disclose all 4 source block signs. This can reduce the existing M–I fitness confound, but still cannot by itself identify real selfing-specific genetic hitchhiking or natural flowering response. The full independent experimental gate requires fresh founder/visitor histories, genetic source ancestry at de novo A mutation birth, fixed biological effect threshold and the longer time horizon, and is NOT executed here.

Paper PR [#609](https://github.com/zuizui0223/izu-core/pull/609) is unchanged. Keep all six-policy and follow-up outputs under research Draft PR [#610](https://github.com/zuizui0223/izu-core/pull/610).
