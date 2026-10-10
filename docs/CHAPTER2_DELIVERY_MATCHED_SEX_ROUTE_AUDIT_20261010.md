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
