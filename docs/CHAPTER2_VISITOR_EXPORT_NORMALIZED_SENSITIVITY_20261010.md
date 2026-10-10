# Matched total-pollen-export visitor composition sensitivity

**2026-10-10 · PR #452 · exploratory, designed after the source model's previous positive composition finding.** This is a strict within-ledger falsifier, not new independent source visitor-history replication and not a real island fitness result.

## Why this experiment?

The preceding [16-row factorial](CHAPTER2_VISITOR_RICHNESS_COMPOSITION_FACTORIAL_20261010.md) showed that equal visitor-ID counts of four can give β− / Γ_seed+ versus β− / Γ_seed− depending on the arrangement of visitors' matching optima. However, changing optima at equal count may also change **total pollen export**. A composition-specific conflict change could be a disguised change in the amount of pollen exported, not a functional mating-allocation effect.

The follow-up holds the original Model3 diploid parental state, N=K=8, pollen background B=48, four visitor IDs, equal functional breadth, equal effectiveness and the full source reproductive formula fixed. It tests:

1. Reference four optima at the source activity (0.4).
2. The same four equally spaced optima all shifted +0.2, at source activity (0.4).
3. The shifted four optima with **only the source activity scalar adjusted** until their total expected pollen export exactly matches the reference (absolute error ≤ 1e-8).

If the β/Γ contrast is lost after pollen-export matching, differences in pollen export provide a parsimonious source explanation; if it persists, the original source kernel's matching, recipient allocation and resulting mating distributions contribute beyond **total** export.

This is still not a natural causal mediation percentage. Matching export does **not** hold actual visitation, realized pollen receipt, mate distribution or maternal reproductive assurance fixed. The shifted model's forced encounter activity can change saturation and the distribution of pollen.

## Frozen sensitivity grid

- Plant matching mean: **0.2, 0.5, 0.8**.
- Parental genotypes: **monomorphic** and one deliberately fixed **mixed-diploid** state.
- Every visitor's matching breadth: **0.12, 0.18, 0.30** (all identical within arm).
- Every visitor's transfer effectiveness: **0.5, 1.0** (all identical within arm).
- Four source optima: **0.15, 0.35, 0.55, 0.75**; shifted: **0.35, 0.55, 0.75, 0.95**.
- Activity law: fixed; visit types remain exactly four.
- **36 paired blocks × 3 arms = 108 complete source rows.**

We archive each full β/Γ readout and F (maternal outcross viable seed), S (viable self seed), total exported pollen, total delivered pollen, adjusted activity and within-fixture contrasts. All no-flip cells must remain. There is no sampling-based p-value or environmental independent replication.

**Source parity control:** the 0.2-matching / 0.18-breadth / effectiveness-1 raw pair is asserted equal, for both diploid fixture states, to the exact [previous 16-row source artifact](https://github.com/zuizui0223/izu-core/actions/runs/38027262398/artifacts/11660547248). If the native source reproduction kernel changes, the run must fail rather than silently claim transferability.

The design is frozen in `data/design/chapter2_visitor_export_normalized_sensitivity_20261010.json`, executed by `scripts/audit_chapter2_visitor_export_normalized_sensitivity.py`, and enforced by `tests/test_chapter2_visitor_export_normalized_sensitivity.py`.

## Reproduce

```bash
pytest -q tests/test_chapter2_visitor_export_normalized_sensitivity.py
python -m scripts.audit_chapter2_visitor_export_normalized_sensitivity \
  --out /tmp/chapter2-export-normalized.json
```

The diagnostic refuses missing cells, mismatched pollen export, invalid derivatives, or mismatch with previous exact Model3 source rows. The archive must retain every row and the raw SHA-256 before numerical outcome claims are made.

**Publication boundary:** A source-internal 36-block sensitivity study cannot demonstrate natural island impacts or long-term evolution-to-extinction; it can only establish which components of the *existing model* are logically required for the instantaneous floral-investment conflict. The natural transport test still requires independently measured plant matching, visitor functional effectiveness, single-visit deposition, and reproductive outcomes at the same site/block.

## Executed source outcome (2026-10-10; exploratory)

**Run succeeded.** Source code commit `32ab1346abb21ff57883283b4903343a3b2b59e4`; [GitHub Actions run 38027964437](https://github.com/zuizui0223/izu-core/actions/runs/38027964437); [full 108-row JSON artifact 11660358587](https://github.com/zuizui0223/izu-core/actions/runs/38027964437/artifacts/11660358587). Original uncompressed JSON SHA-256: `924a29fd710aa00a5982a16477c17cdc58407d39e34358dd6f72fe84692d655d`; bytes: 106,261. This original ZIP was downloaded independently and the JSON digest checked. Compact result and caution contract: `data/results/chapter2_visitor_export_normalized_sensitivity_receipt_20261010.json`.

All 108 rows and 36 three-arm contrasts are present. The maximum absolute normalized-export difference is **3.584 × 10⁻¹²** (tolerance 10⁻⁸). Matched activities ranged **0.2693 to 2.0026**. The original 16-row Model3 benchmark is exactly recovered in both synthetic diploid states (matching 0.2, breadth 0.18, effectiveness 1.0).

For this **representative prior source fixture**:

| Measurement | Monomorphic reference → shifted raw → shifted export-matched | Mixed-diploid reference → shifted raw → shifted export-matched |
|---|---|---|
| Encounter activity | 0.400 → 0.400 → 1.109 | 0.400 → 0.400 → 1.071 |
| Total pollen export | 10.093 → 3.716 → **10.093** | 9.996 → 3.818 → **9.996** |
| Delivered pollen | 0.477 → 0.112 → **0.305** | 0.457 → 0.115 → **0.301** |
| Group viable seed | 11.993 → 10.883 → **11.474** | 11.932 → 10.889 → **11.457** |
| β median | −0.063 → −0.273 → **−0.156** | −0.069 → −0.272 → **−0.159** |
| Γ_seed | +0.158 → −0.212 → **−0.00195** | +0.141 → −0.210 → **−0.01008** |

After equalizing total pollen export, viable seed still decreases by **−0.51874** and **−0.47462**, respectively, compared to the reference. **However both equalized Γ_seed values are within the frozen ±0.02 classification deadband and therefore inconclusive: they are NOT robust group-negative gradients.** In these original fixture contexts, the majority β-negative / Γ-positive disagreement condition is no longer satisfied, but that is a classification condition, not proof of an opposite evolutionary equilibrium.

Across all 36 intentionally chosen, NOT independent natural-system blocks: **8/36** conflict-status flips with the raw optimum shift, **7/36** after equalizing export; **20/36** equalized blocks had negative seed differences and **16/36** positive. There is no universal direction over arbitrary plant match, breadth and efficacy, and the 36 cells must not be treated as a binomial biological sample or an effect-size meta-analysis.

**Scientific result:** Equal total pollen *export* is insufficient to equalize pollen *delivery*, viable seed output or the β/Γ landscape in the original source reproductive operator. The difference can be produced through its matching, pollen-allocation and recipient pathways. **Not identified:** an independent ecological-pollinator mechanism, a natural-species-richness effect, a clean fraction of mediation by visitor composition, a long-term evolutionary investment shift, or a species-persistence response.

**Run status boundary:** The audited sensitivity runner and artifact upload succeeded at source commit `32ab1346`; the full Python CI matrix and latest-commit scientific gate are tracked separately. Do not infer their completion from this row-level success alone.
