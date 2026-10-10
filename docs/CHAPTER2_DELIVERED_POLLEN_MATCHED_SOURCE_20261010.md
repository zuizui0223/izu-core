# Matched *delivered* pollen, not just exported pollen (source falsifier)

**Status (2026-10-10): exploratory post-discovery source-model diagnostic, design fixed before its own numerical run.** This extends [the SHA-verified 108-row export-normalized analysis](CHAPTER2_VISITOR_EXPORT_NORMALIZED_SENSITIVITY_20261010.md). The previous 36 matched source fixtures showed that holding total *exported* pollen equal is not enough to hold delivered pollen equal; the prior raw JSON provides a descriptive delivery-vs-seed difference correlation near 0.9999 within each of the two fixed genotype fixtures. These are fixed source design rows, not independent biological samples.

## New falsifiable mechanism target

The unchanged Model3 `reproduce_kb` source ledger is

- 8 diploid plants with fixed matching and assurance alleles within each block, 4 visitors
- four reference optima (0.15,0.35,0.55,0.75) versus shifted optima (+0.2 each)
- identical type counts, per-type breadth and efficacy, fixed mode encounter law
- **only the shifted arm activity** is adjusted until summed pollen *delivered to recipients* equals that of the reference (absolute tolerance 1e-8)
- native prior-selfing option is *not* invoked; this uses the source delayed-selfing setting and pollen-background B=48.

There are 2 synthetic diploid state templates × 3 parental matching means × 3 visitor breadths × 2 effectiveness settings = 36 registered contrasts, with all reference/raw/delivery-matched source outcomes preserved. **Numerically unmatchable states remain explicit blocks**; matching failure is never imputed as no biological effect.

## Critical mathematical negative control

Under exactly equal plant genotypes, the source ledger has the same ovule budget `O`, autonomously viable selfed fraction `a(1-depression)`, and (by within-plant exchangeability) equal recipient pollen receipt at each of 8 maternal plants. For delayed selfing,

```
Total viable seed =
  sum_i [ a_i (1-delta) O_i +
          (1-a_i (1-delta)) O_i
          * (1-exp(-recipient_receipt_i / (2*pollen_scale))) ]
```

Consequently, for identical mother genotypes and homogeneous incoming pollen allocation, **equal total delivered pollen mathematically forces equal total viable seed output**. If this invariant fails for a matched source block, stop and diagnose a biological-operator or implementation error. For synthetic mixed-diploid mothers, summing receipts loses their individual allocation information, so a nonzero matched seed contrast is possible.

## How this constrains ecological claims

If all original composition/seed contrasts vanish at matched delivery, the preceding `total export` sensitivity was principally a pollen-delivery quantity effect *within this source kernel*, and a purported extra effect of visitor partner identity on collective female seed output is not independently established by that simulation. Focal male (paternal) genetic success could still respond to **where pollen goes**, even if maternal group seeds become identical. If mixed genotype cases retain a difference, its source explanation remains recipient-specific receipt, ovule budget and assurance combinations—**not observed natural mate quality, novel ecological evolutionary mechanisms or long-term extinction**.

Execute:

```bash
python -m scripts.audit_chapter2_visitor_delivery_matched --out /tmp/delivery-matched-source.json
pytest -q tests/test_chapter2_visitor_delivery_matched.py
```

Source design: `data/design/chapter2_visitor_delivery_matched_20261010.json`. Implemented source runner: `scripts/audit_chapter2_visitor_delivery_matched.py`. Tests: `tests/test_chapter2_visitor_delivery_matched.py`. Values require a source-head run, full 36-block JSON archive and checksum verification before they can be promoted even as descriptive source results. Retain this PR as Draft.
