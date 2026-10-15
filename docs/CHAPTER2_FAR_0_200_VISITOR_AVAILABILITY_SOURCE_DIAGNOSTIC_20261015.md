# Far t0–200 investment divergence versus years without visitors (2026-10-15)

**Result: exploratory retrospective source-only evidence.** All 512 exact original far first-repeat genetic paths from the already completed source replay were reopened as authenticated original-artifact ZIPs, with source SHA-256, case receipts, t200 genotype-parity flags and annual genetic accounting checked. No new evolution, visitor history, independent founder, field island, or randomised pollinator removal was generated. The inferential unit is **64 original visitor histories shared across four mating rules**, not 256 independent island systems.

Sources: [exact original 0–200 original-genotype replay](CHAPTER2_FAR_ORIGINAL_0_200_MECHANISM_RESULTS_20261015.md), [authentic workflow 38712511100](https://github.com/zuizui0223/izu-core/actions/runs/38712511100), source artifact IDs 11960493773, 11961232718, 11960428880, 11961412529. [Archived artifact identities](deposit/chapter2_far_asymmetry_source_artifact_inventory_20261015.json). Reproduction/Price terms are the original source equations (not a new approximate fitness definition).

## Primary post-hoc historical diagnostic

Across the 64 original far visitor histories, the 0–200 interval has on average **127.02 years with no visitor types** (min 17, max 179; 200 years total). The *same* visitor sequence is used in fixed- versus evolving-A treatments within each mating setting.

| Reproduction rule | Spearman `zero visitor years` vs far I E−F level at t200 | Descriptive 95% history bootstrap |
| --- | ---: | ---: |
| Delayed/no A cost | +0.074 | [−0.150, +0.299] |
| Prior selfing | +0.041 | [−0.225, +0.290] |
| Pollen discount | −0.138 | [−0.391, +0.126] |
| Direct A cost | −0.091 | [−0.349, +0.172] |

**Interpretation:** The simple historical account “more visitor-free years → systematically greater positive early evolving-minus-fixed investment difference” does **not receive consistent support**. All four exploratory rank-correlation intervals include zero and their signs differ. This does not establish no effect: exposure timing, visitor composition, genetic state, correlation in the model and finite sampling could matter. In particular the original 64 visitor histories were already examined during development, and the bootstrap intervals are **descriptive post-outcome intervals**, not a new prospective family-wise test.

## Exact partition of realized t0–200 I change by historical visitor availability

For every paired source history, partition **annual realized** `ΔI_evolving − ΔI_fixed` into years with zero visitor types and years with at least one. This telescopes **exactly** to the already archived t200 E−F I difference. These are arithmetic allocations across time, not causal effects of switching visitors on/off.

| Rule | E−F total I by t200 | Cumulative component on visitor-absent years | On visitor-present years |
| --- | ---: | ---: | ---: |
| Delayed/no cost | +0.05536 | +0.04828 [0.01494, 0.08045] | +0.00708 [−0.02832, 0.04219] |
| Prior selfing | +0.05993 | +0.03909 [0.01100, 0.06806] | +0.02084 [−0.01136, 0.05407] |
| Pollen discount | +0.03035 | +0.02463 [−0.00647, 0.05409] | +0.00572 [−0.02801, 0.03991] |
| Direct A cost | +0.02722 | −0.00021 [−0.03067, 0.03047] | +0.02743 [−0.00779, 0.06269] |

The first three settings have more of their **aggregate** positive t200 difference allocated to zero-visitor years, but direct assurance cost does not. There are more zero-visitor than visitor-present years. The within-history **per-year average** absence-minus-presence E−F differences have descriptive 95% bootstrap intervals spanning zero in *all four* settings (mean +0.000171, +0.000036, +0.000205, −0.000354). This does **not** identify an absence-specific selection mechanism.

Original source annual Price and realized residual terms telescope separately within each exposure stratum. In the complete source audit, only the prior-selfing whole-period *parental Price* mean E−F interval excluded zero descriptively; other settings could include substantial realized transmission residual. The direct assurance-cost rule is an explicit counterexample to treating “visitor absent” as a universal explanation for the early positive far E−F.

## What this rules out, and what it leaves

- **Disfavours a simple dose-response:** visitor-absence duration alone does not predict original t200 investment preservation across the 64 history units.
- **Does not prove cessation of selection:** when no pollen is delivered, the source fixed-state investment gradient is `−2*c_I*I` and remains negative for I>0. Absence changes the dependence on A, not all investment selection.
- **Does not estimate direct effects of visitor loss:** this is observational partitioning of **already realized synthetic model histories**, not `do(visitor=0)`.
- **Does not apportion selection versus drift:** Price weighting and realized residual both depend on evolving genetic states and segregation/mutation; no unique mechanism fraction follows.
- **Does not transfer to natural islands:** both original near and far environments are artificial visitor-replenishment regimes; model-local results cannot identify a historical cause for the Izu islands.

**Next scientific decision:** do **not** add a broad exploratory search for a stronger correlation. If the far sign is to be promoted as a causal novelty, first conduct a **separately prospectively frozen and independent visitor/founder cohort** crossing A-fixed versus A-evolving during t0–200, and preserve both positive and negative early signs. Until then, keep the active Letter centred on Q2/Q3 genetic response and finite inherited realization, with Q1 as theoretical context and Q4 as a separate demographic consequence.

### Reproduction

```bash
python -m scripts.audit_chapter2_far_early_visitor_states_20261015 \
  --shards original_shard0.zip original_shard1.zip original_shard2.zip original_shard3.zip \
  --out /new/output/source_visitor_partition.json
pytest -q tests/test_chapter2_far_early_visitor_states_20261015.py
```

The CLI rejects archive SHA changes, duplicate or missing source histories, broken case receipts, unequal paired visitor paths and non-telescoping Price/residual identities. Outputs are **new paths only**, without changing frozen source results.
