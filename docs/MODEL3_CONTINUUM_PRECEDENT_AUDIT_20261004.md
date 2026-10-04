# Model 3 continuum / island-syndrome nearest-precedent audit — 2026-10-04

**Status:** exploratory positioning note for PR #396. This file narrows novelty claims; it does not modify the locked submission manuscripts.

## What is already established in the literature

### Attraction allocation is old theory

Charlesworth & Charlesworth (1987, *Evolution*, doi:10.1111/j.1558-5646.1987.tb05869.x) derived fitness expressions for partially selfing cosexual plants in which allocation to attractive structures trades off with primary reproductive functions and solved ESS allocation problems.

Therefore do **not** claim that Model 3 is the first theory to put a cost on pollinator attraction or to derive an optimum floral investment.

### Pollen limitation can favour multiple reproductive solutions

Harder et al. (2010, *Philosophical Transactions B*, PMID 20047878) explicitly modelled selection on floral traits and mating systems under pollen limitation and emphasized that pollen limitation can favour increased outcrossing, increased selfing, or context-dependent combinations.

Therefore do **not** claim that pollinator scarcity creating alternative floral/mating-system routes is new.

### Reproductive assurance under pollen limitation is classical

Busch & Delph (2012, *Annals of Botany*, PMID 21937484) review reproductive assurance as a major explanation for selfing in isolated, marginal and island populations. Porcher & Lande (2005, *Journal of Evolutionary Biology*, doi:10.1111/j.1420-9101.2005.00905.x) modelled selfing under pollen limitation and pollen discounting.

Therefore Baker-style reproductive assurance and selfing thresholds are not new.

### Floral display and mating system are already coupled empirically and theoretically

Goodwillie et al. (2010, *New Phytologist*, doi:10.1111/j.1469-8137.2009.03043.x) documented correlated evolution between mating system and floral display across angiosperms.

Rodger et al. (2019, *Annals of Botany*, PMCID PMC6589515) found that reproductive assurance weakens pollinator-mediated selection on flower size under strong pollen limitation.

Devaux and collaborators modelled joint evolution of pollen limitation, floral display/phenology and mating-system constraints; later synthesis emphasizes equilibria determined by pollinator attraction, selfing and inbreeding-depression trade-offs.

Therefore the analytic result `dB/dr < 0` is biologically useful but **not a priority claim**.

## Island-specific empirical boundary

Abe (2006, *Annals of Botany*, doi:10.1093/aob/mcl117) documented an Ogasawara pollination island syndrome including subdued floral traits.

Hetherington-Rauth & Johnson (2020, *The American Naturalist*, doi:10.1086/709018) examined 556 species in 136 phylogenetically independent Pacific island–mainland contrasts and found no global tendency toward smaller island flowers, although some archipelagos did show reductions.

Ciarle & Burns (2025, *New Zealand Journal of Botany*, doi:10.1080/0028825X.2024.2377418) likewise review heterogeneous plant island-syndrome evidence and explicitly note that pollinator paucity need not always reduce display: depending on biotic and abiotic conditions, selection can also favour showier flowers.

That heterogeneity is compatible with Model 3's state-dependent branching and blocks any universal "islands cause smaller flowers" claim.

## What remains potentially distinctive in Model 3

The defensible contribution is narrower than "first theory of floral island syndrome" but stronger mechanistically.

1. **Isolation is not entered as a floral optimum or trait coefficient.**  
   It changes a stochastic visitor-assembly process; floral selection follows from the resulting pollen-transfer operator.

2. **The same biological operator spans four levels.**  
   Finite ABM → deterministic genotype density → exact continuous-genotype sexual integral system → reduced phenotype PDE / analytic threshold.

3. **The first moment has an exact bridge.**  
   Under the frozen reduction conditions, the Price equation reproduces the exact genotype-density one-generation mean in 25/25 cells to numerical precision.

4. **The reduced continuum survives the full frozen visitor-history ensemble.**  
   It recovers the controlled response directions and the near/far intervention structure rather than merely reproducing one hand-picked equilibrium.

5. **Richness matching provides a causal-mechanism contrast.**  
   The natural near→far threshold shift disappears when annual visitor richness is response-blind matched, while visitor-history pooling preserves/strengthens the negative investment regime. This separates visitor-amount positioning from history/demographic realization.

6. **The joint selection-vector statement is stronger than either marginal result alone.**  
   Across the frozen natural near/far histories, the local vector rotates toward lower floral investment and higher reproductive assurance. A direct assurance cost shifts absolute assurance selection but cancels in the paired near/far difference, producing environment-specific critical-cost windows.

## Safe novelty statement

> Existing theory already explains why pollen limitation can favour selfing and why reproductive assurance can weaken selection for attractive floral display. Model 3 contributes a generative island mechanism: isolation acts only through stochastic visitor assembly, yet the resulting near–far shift in a joint floral-investment/reproductive-assurance selection field survives from an explicit eco-evolutionary simulation to a continuous reduction and an analytic threshold, and the shift is selectively removed by response-blind visitor-richness matching.

## Claims to avoid

- first mathematical model of the selfing syndrome;
- first theory coupling reproductive assurance and reduced floral display;
- first prediction that pollen limitation can favour selfing;
- universal smaller flowers on islands;
- universal increase in selfing on islands;
- proof of a natural island-syndrome equilibrium;
- quantitative calibration to named archipelagos;
- treating the reduced PDE as the exact sexual-genetic Model 3.


## Rare-mutant and two-trait precedent boundary

The assurance gradient must be interpreted as an **individual invasion-fitness** problem, not as the derivative of monomorphic population output when every individual changes assurance simultaneously.

- Lloyd (1979, *The American Naturalist* 113:67–79, doi:10.1086/283365) wrote exact fitness comparisons for phenotypes differing in self-fertilization, including the automatic transmission advantage and the distinction among competing, prior and delayed selfing. Delayed selfing can be individually advantageous whenever unused outcross opportunities remain under the stated independence assumptions.
- Harder et al. (2010, *Philosophical Transactions B* 365:529–543, PMID 20047878) likewise formulate pollen-limitation adaptation through the fate of a variant individual in a resident population and keep female outcross, selfing and siring success conceptually separate.
- Harder & Wilson (1998, *The American Naturalist* 152:684–695, doi:10.1086/286199) clarify that pollen discounting is a male-function cost of selfing and that its evolutionary consequences depend on pollination conditions.
- Porcher & Lande (2005, *Journal of Evolutionary Biology* 18:497–508, doi:10.1111/j.1420-9101.2005.00905.x) explicitly model pollen limitation × pollen discounting with evolving inbreeding depression/purging. Their selfing thresholds and high-selfing mixed equilibria are precedent, not Model 3 novelty.
- Lande & Schemske (1985, *Evolution* 39:24–40, doi:10.1111/j.1558-5646.1985.tb04077.x) derive alternative predominantly selfing and predominantly outcrossing states when selfing and inbreeding depression coevolve. Model 3 fixes inbreeding depression, so any branching in the present extension cannot be identified with their purging feedback.

The corrected Model 3 joint audit therefore uses

```
w_mut = 0.5 F_mut + 0.5 P_mut + S_mut
```

for a rare mutant in a fixed resident reproductive environment, where `F_mut` is maternal outcross success, `P_mut` is paternal outcross success, and `S_mut` is viable selfed seed. The selfed term carries both parental genome halves.

### Joint floral display × mating-system theory is also not empty territory

Goodwillie et al. (2010, *New Phytologist* 185:311–321, doi:10.1111/j.1469-8137.2009.03043.x) show broad correlated evolution between outcrossing and floral display and review the prediction of reduced attraction allocation in selfing species.

Devaux et al. and related pollinator-foraging models explicitly couple floral display/phenology, pollinator behaviour and selfing or geitonogamy; their synthesis emphasizes that floral display and mating-system equilibria can arise jointly from pollinator attraction and inbreeding-depression trade-offs.

Empirically, work on *Clarkia xantiana* under strong pollen limitation has detected disruptive selection through male and female fitness, with larger petals benefiting outcross siring and smaller petals associated with selfed siring. Therefore even an observed two-corner fitness landscape would not by itself be a priority claim.

## Updated safe novelty statement after rare-mutant correction

> Existing mating-system theory already contains the automatic advantage of selfing, seed and pollen discounting, pollen-limitation thresholds, joint floral/mating-system trade-offs and purging-driven alternative states. The potentially distinctive Model 3 result is narrower: the **same stochastic visitor-transfer operator** generates a near-to-far rotation of the rare-mutant selection vector for floral investment and reproductive assurance, that rotation is tested across the complete frozen visitor-history ensemble, its first-moment response is connected to the exact sexual-genetic operator by a multivariate Price identity, and the role of trait covariance and finite historical realization is then tested without changing the ecological operator.

This is the novelty boundary to use in any Evolution Letters integration.
