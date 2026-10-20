# Secondary colonisation — source-matched archive audit (2026-10-20)

**State:** complete read-only reanalysis of the **already executed** 240 Model3 futures. No new ecological histories, biological transitions, p-values, independent sample count, or confirmatory result were generated.

## Source verification

- Original Actions run: https://github.com/zuizui0223/izu-core/actions/runs/39366132489
- SHA-256 of the original EXPLORATORY.json: **44664beef561ff30a0bddd0a9bd06950302b60c90477aa2ccb0698bb9542c223**
- Independent founder-axis seeds: 2; independent visitor-axis seeds: 2; **four crossed background blocks**, not 240 independent islands
- All 20 donor states were alive and produced an eight-seed cohort; sampled viable seed potential ranged from **134 to 200** per donor. The cap was reached in every case.
- **All 48** matched founder × visitor × destination × distance × future-replicate contexts had exactly the same *number of initially settled seeds* across the five genetic-source histories. Thus the differing within-context ancestry endpoints are **not explained by different cohort sizes or seed-settlement draws** in this particular frozen pilot.
- However, the arrival RNG **was not matched across different recipient destinations**. Therefore a contrast between vacant and already-occupied mainland-like destinations cannot be attributed to competition or genotype-dependent fitness alone.

## Paired comparison: mainland-like recipient with existing conspecifics, distance 1.5

| Source history | Source-selected-locus alleles present at year 20 | Paired discordance |
|---|---:|---|
| Ancestral t0 | 2/8 | Not a matched A intervention |
| Island A fixed, t10 | 2/8 | Evolving-only 3; fixed-only 1 |
| Island A evolving, t10 | 4/8 | Both 1; neither 3 |
| Island A fixed, t25 | 2/8 | Evolving-only 3; fixed-only 1 |
| Island A evolving, t25 | 4/8 | Both 1; neither 3 |

The paired difference **4/8 vs 2/8** is not the result of all eight streams consistently favouring evolving A: at both t10 and t25, **three** pairs favour the evolving-history source while **one** favours the fixed-history source. There are only **four** crossed-source backgrounds, each used by **two nested futures**. This is descriptive heterogeneity, not a significant effect, A-specific genetic mediation, or evidence of naturally occurring mainland recolonisation.

In this recipient/distance cell, **six of eight** paths had at least one settled migrant seed for *each* source history, and the **total resident population remained occupied in all eight**. In contrast, source alleles at the three selected M/I/A loci remained in only 2/8 or 4/8 paths. **Total habitat occupancy is not migrant establishment.** Those source alleles may also survive by introgression without a self-sustaining separately identifiable migrant population.

## Direction is recipient- and distance-dependent

For t25 historical sources:

| Recipient/distance | Fixed-A source | Evolving-A source |
|---|---:|---:|
| Island-like vacant, distance 1.5 | 5/8 | 6/8 |
| Mainland-like vacant, distance 1.5 | 7/8 | 8/8 |
| Mainland-like occupied, distance 1.5 | 2/8 | 4/8 |
| Mainland-like occupied, distance 0 | 7/8 | 7/8 |

The source-history contrast is therefore not a universal advantage for the evolving-A treatment. Source M/I/A allele distributions, their reproduction, and subsequent stochastic parentage also differ between histories. All descendant treatments allow A to evolve, while the original fixed-A intervention still permits selfing.

The original raw archive includes conditional reproductive-return diagnostics and I/A endpoints. Their comparison is conditioned on source-locus carrier persistence, uses artificial reference competitors, and is **not by itself adaptive fitness improvement**.

## Scientific interpretation and next gate

What is supported **inside this artificial model**: same-sized, arrival-matched migrant cohorts with different source histories can have different later persistence of tracked source-selected alleles; a recipient community can persist after these alleles disappear. The present model does **not** show a real island-to-mainland migration event, a species-level establishment rate, restored ancestral flowers, or the causal effect of A alone.

Two follow-on checks are deliberately separate:

1. **Already implemented in this PR:** a source-locked *technical* pedigree replay tracing genealogical descendants through the native maternal/paternal parentage ledger, alongside the frozen selected-locus marker. It must verify every original census before reporting new descendant counts. Its full archived 240-path replay has **not yet been admitted**, so this document reports **no pedigree results**.
2. **Later prospective biological experiment:** match the same landed seed cohorts across both vacant and resident-occupied recipient contexts, and distinguish natural propagule export from artificially equalized export. Freeze the protocol before enlarging the four original crossed-source blocks and test A expression/genotype-module interventions separately.

Reproduce the current read-only audit with:

    python -m scripts.audit_secondary_colonization_archive_20261020 \
      --original PATH_TO_ORIGINAL_EXPLORATORY_JSON \
      --output NEW_PATH_TO_AUDIT_JSON

The script checks the complete 240-key allocation, exact original SHA-256, 20 capped seed cohorts, 48 cross-source settlement matches, 30 descriptive groups, and 12 paired-history contingency tables. The original archive remains unchanged.
