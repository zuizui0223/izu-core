# After pollen delivery matching, does paternal return still move?

**Exploratory source Model3 F/P/S audit, 2026-10-10 (PR #452).** This is not a new pollinator community sampled in nature, nor a selection-over-generations test. Its data are fixed *before this diagnostic*, but its choice of question follows observation of the previous Model3 36-block delivery-matched outcomes; it is thus post-discovery.

## Scientific decision

The earlier [matched-delivery experiment](CHAPTER2_DELIVERED_POLLEN_MATCHED_SOURCE_20261010.md) demonstrated that total expected group seed output is nearly equal after matching total pollen delivered, for synthetic monomorphic and mixed-diploid plant states. However, this does not demonstrate that **fathers contribute equally** or that a focal plant has the same incentive to invest. Total maternal seeds is a sum across mothers. The male donor marginal genetic contribution `P_i` is a *different perspective on the same outcross seeds*.

We therefore compare original reference functional visitor optima with shifted optima at an activity scalar tuned to match total delivered pollen, holding each of the 36 original Model3 genotype/N/K/B/visitor-breadth/effectiveness states constant. *No founder genotype, population history or canonical reproduction operator is modified.*

For each of the eight fathers/mothers `i` in each source state, the original source genetic contribution is

```text
W_i = 0.5 F_i + 0.5 P_i + S_i
beta_i = d log(W_i) / d investment_i
       = beta_F,i + beta_P,i + beta_S,i
```

Each term is computed by ±0.005 finite differences, using the **same activity scalar for the + and − perturbations**. The signed component differences sum to the full focal log-gradient to a numerical tolerance of 1e-10, using the source `log_mean(W+,W−)` identity. The donor count-share vector `P_i/sum(P)` and its L1 distance between arms measure the degree of redistribution of expected paternal success.

| Case | Expected controls | Interpretation if altered |
|---|---|---|
| Eight clones | Donor shares equal (L1 ≈0); group maternal seed difference ≈0 once delivery is matched | β components can still differ when derivatives of recipient affinity change; do not equate endpoint seed equality with identity of derivatives |
| Eight mixed diploids | Total delivery equal, but donor shares may redistribute; β_F/P/S can respond differently | A mechanistic *within-source* route redistribution, not observed natural parentage or evolutionary selection |
| Every original state | `sum P = sum F`, total seed = F+S, β components exactly add | Stop the model test on any accounting failure |

The 36 contexts are **not statistical sampling units** from ecological systems; retaining 36×2×8=576 source focal log-gradients does not increase the number of natural populations studied (zero).

## Status and execution

Frozen contract: `data/design/chapter2_delivery_matched_fps_decomposition_20261010.json`. Reproducible source evaluator: `scripts/audit_chapter2_delivery_matched_fps_decomposition.py`. Regression suite: `tests/test_chapter2_delivery_matched_fps_decomposition.py`.

```bash
python -m scripts.audit_chapter2_delivery_matched_fps_decomposition --out /tmp/chapter2-delivery-fps.json
pytest -q tests/test_chapter2_delivery_matched_fps_decomposition.py
```

**Adoption rule:** No numerical component or parentage claims until the complete source-head JSON is executed, SHA-verified, and checked on the original 36-block scaffold. Even if a sex-route contrast exists, it does not show historical island floral adaptation, pollen limitations in the wild, heritable trait evolution, genetic load, population extinction or evolutionary suicide. Keep PR #452 Draft.

## Executed source audit (2026-10-10)

**Source runner PASS.** GitHub [run 38032275754](https://github.com/zuizui0223/izu-core/actions/runs/38032275754), original [full F/P/S artifact 11662276812](https://github.com/zuizui0223/izu-core/actions/runs/38032275754/artifacts/11662276812), uncompressed JSON 362,001 bytes, SHA-256 `5dbc7a1f219fe2f6e627fbc65c59de9c0071086ce92fd56bc705f281f2fdc14c`, independently downloaded/extracted/hashed. Full 36 blocks, 72 distinct source-arm evaluations, 576 finite parental investment derivative records. Source commit `16a7d615b29d1fa82ff4fcee9f180ffdbd4d57a8`; SHA-locked compact [result receipt](../data/results/chapter2_delivery_matched_fps_source_receipt_20261010.json). This run is *post-discovery and model-internal*, not independent biological confirmation.

| Original fixed source genotype fixture | Monomorphic (18 blocks) | Mixed diploid (18 blocks) |
|---|---:|---:|
| Mean absolute **group seed** contrast at identical pollen delivery | ~7.1e−14 | 0.000904 |
| Paternal contribution **share L1** difference (mean) | **0.000** | **0.1122** |
| Paternal share L1 maximum | 0 | **0.5511** |
| Mean absolute focal β difference, computed across adults | 0.000958 | **0.01731** |
| Mean absolute β_F difference | 0.000130 | **0.008801** |
| Mean absolute β_P difference | 0.001038 | **0.008878** |
| Mean absolute β_S difference | 0.0000455 | 0.000361 |
| Focals with absolute β difference greater than 0.02 | 0/144 | **35/144** |
| Blocks with both positive and negative individual β changes | 0/18 | **16/18** |

These deliberately constructed plant states show **conditional divergence between collective output and distribution of individual expected genetic returns**. In mixed diploid model populations, **all 18/18** visitor-optimum shifts changed relative paternal shares even after total delivered pollen was matched. For cloned mothers/fathers, equal delivery led to equal group viable seeds and uniform paternal shares, as required by symmetry.

This is **not a claim of paternal-only selection**: maternal β_F and paternal β_P changed by similar average absolute magnitudes in the mixed-genotype fixture. The raw signed effects can cancel in the median, even when individual absolute gradients are substantially different. It would be scientifically misleading to infer `selection unchanged` merely because the **median** focal β shifted by only ~0.003 in the mixed-diploid 36-cell source benchmark.

**Crucial distinction:** even with group seed output essentially held constant by fixing total receipt, source individuals may redistribute how much expected outcross reproductive success they gain from maternal and paternal channels, because the pollen operator depends on their trait matching. Focal β changes are derivatives around each fixed baseline genotype, not measured genetic change or independent proof of selection over generations. Therefore, no claim of future allele trajectories, local adaptation, extinction, island-wide generality or universal pollen-routing benefit is admissible.

The earlier pollen-delivery matching conclusion remains intact: **group seed-output differences are almost wholly explained by total pollen delivery in these fixtures**. The present result adds a *different level* of analysis—the distribution of reproductive contributions among individuals—not a correction reviving the earlier rejected claim of a large extra group-seed benefit at fixed total delivery.

**Remaining decisive outside-model test:** measure individual-linked pollen deposition, parentage/paternity and maternal viable-seed outcome under equal observation effort on the same plants/blocks; evaluate whether the source mathematical allocation differences appear in real populations. Model3 results alone do not determine natural effect sizes.
