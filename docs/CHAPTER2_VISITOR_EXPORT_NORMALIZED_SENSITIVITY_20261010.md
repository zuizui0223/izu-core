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
