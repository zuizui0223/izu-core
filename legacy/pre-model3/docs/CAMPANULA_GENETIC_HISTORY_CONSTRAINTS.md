# Campanula population-genetic history constraints

## Why this is a constraint document, not another fitted axis

The current *Campanula* calibration contains smooth island-order erosion in flower size/outcrossing and a sharp Oshima-to-Toshima transition in autonomous reproductive capacity. Static geography and pre-1986 volcanic recency do not reproduce that multichannel profile.

Population history is nevertheless a serious alternative explanation for the continuous island-order components. Two primary population-genetic studies provide source-native constraints, but their abstracts do **not** expose a common island-level numeric history variable that can be safely inserted into the AICc comparison.

`data/design/campanula_genetic_history_constraints.csv` therefore records the reported constraints without inventing a latent score.

## Inoue & Kawahara 1990: allozymes

Primary source: *American Journal of Botany* 77:1440–1448, DOI `10.1002/j.1537-2197.1990.tb12554.x` / `10.2307/2444754`.

The source abstract reports:

- 17 populations were studied, 10 from the Izu Islands and seven from mainland Honshu;
- total genetic variation was nearly the same in island and mainland sets, but among-population differentiation was greater in the islands;
- total genetic diversity in each island population decreased with distance from the mainland;
- genetic and geological evidence suggested relatively ancient founding on northern islands followed by progressive dispersal to southern islands.

### Consequence

A winning `island_order_cline` is therefore **not mechanistically diagnostic of pollinator change**. A north-to-south colonisation sequence is a source-supported alternative that is structurally aligned with the same ordered scaffold.

Without the original population table, it is not legitimate to manufacture a numeric `colonisation_history` score from the abstract.

## Oiki et al. 2001: RAPD

Primary source: *Annals of Botany* 87:661–667, DOI `10.1006/anbo.2001.1389`.

The primary abstract reports:

- RAPD variation was examined in nine *Campanula microdonta* populations;
- Shannon H values did not correlate with distance from the Japanese mainland;
- cluster analysis suggested that colonisation of each island probably occurred once, except Miyake Island, where immigration occurred at least twice.

### Consequence

The RAPD result cannot simply be averaged with the allozyme result into one history gradient. The marker systems give different distance-diversity relationships, and Miyake is explicitly described as a colonisation-history exception.

The abstract does not list the complete sampled-locality table or provide an island-level numeric colonisation score. Therefore the Miyake statement remains a qualitative history constraint until the source table is recovered.

## Current interpretation rule

The present evidence supports the following separation:

1. **Continuous flower-size/outcrossing erosion:** descriptive response shape established, mechanism unresolved. Pollinator turnover, colonisation history, demographic structure and other ordered processes remain confounded.
2. **Autonomous reproductive capacity:** Oshima-to-Toshima step remains a distinct response shape that is not reproduced by the tested climate-PC1, mainland-distance, area/connectivity, or volcanic-recency axes. This is stronger mechanistic leverage, but still not proof of historical Bombus causation.
3. **Cross-lineage replication:** remains necessary to distinguish a pollinator-specific breakpoint from lineage-specific colonisation history.

## Next recovery gate

Before fitting population-genetic history as a numeric competitor, recover from the original genetic papers:

- exact island/population labels;
- population-specific diversity values and sample sizes;
- genetic distances or similarities used for clustering;
- uncertainty where available;
- an explicit mapping to the focal trait populations.

Until then, `island_order` must remain labelled as a descriptive scaffold rather than a causal pollinator or colonisation variable.
