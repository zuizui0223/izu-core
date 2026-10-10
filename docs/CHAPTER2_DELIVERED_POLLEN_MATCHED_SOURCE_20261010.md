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

## Source-executed result: delivery volume explains almost all maternal seed contrast

**2026-10-10, source execution PASS.** Original [full 36-block JSON artifact 11661585364](https://github.com/zuizui0223/izu-core/actions/runs/38029045241/artifacts/11661585364), [workflow 38029045241](https://github.com/zuizui0223/izu-core/actions/runs/38029045241), source commit `cb92335b73c7ea54b6c2b3f1245128cb63ca3c19`. The original downloaded JSON is **103,497 bytes** with SHA-256 `52b55ff8ab4d7651ac86068a6cf256967d86275518f7dbb04b7909cd847ed7e3`. The exact 36-block output and null cells were independently inspected. Permanent [compact result receipt](../data/results/chapter2_visitor_delivery_matched_receipt_20261010.json).

All **36/36 matched**; 0 unmatchable. Maximum total-delivery equality error **1.52 × 10⁻¹³**. Adjusted activity ranges 0.2647–6.932, and source total pollen *export* relative to the original ranges 0.969–3.269—thus **matched delivery is explicitly NOT matched export**.

| Fixed source genotype fixture (18 blocks each) | Mean absolute viable-seed difference before delivery matching | After delivery matching | Maximum absolute matched difference | β−/Γ+ conflict classification flips after match |
|---|---:|---:|---:|---:|
| Monomorphic | 0.368866 | approximately **7.1 × 10⁻¹⁴** | **4.62 × 10⁻¹³** | **0/18** |
| Mixed diploid | 0.353998 | **0.000904** | **0.005645** | **0/18** |

Under the canonical formerly highlighted fixture (parent matching 0.2, visitor breadth 0.18, efficacy 1):

| Readout | Clonal reference | Clonal delivered-matched | Mixed reference | Mixed delivered-matched |
|---|---:|---:|---:|---:|
| Total exported pollen | 10.0931 | **15.7512** | 9.9960 | **15.1731** |
| Total delivered pollen | 0.476752 | **0.476752** | 0.456762 | **0.456762** |
| Group viable seed | 11.992566 | **11.992566** | 11.931507 | **11.928117** |
| Focal β median | −0.063174 | −0.065489 | −0.068689 | −0.075600 |
| Group Γ_seed | +0.158229 | +0.159166 | +0.140508 | +0.135943 |
| β−/Γ+ conflict? | Yes | **Yes** | Yes | **Yes** |

This **changes the priority of scientific interpretation** compared with our earlier export-only analysis: under this Model3 source kernel, the large seed reduction following visitor-optimum shifts is nearly entirely mediated *mathematically* by the amount of pollen reaching recipient plants. There is **no demonstrated large group-viable-seed effect of pollen-recipient allocation once total delivered pollen is fixed** in the two tested synthetic genotype states. The 0.000904 mixed-genotype mean absolute residual is descriptive and untested in natural populations.

This does **not** mean pollinator functional composition is irrelevant: composition strongly changes the fraction of exported pollen that reaches flowers under the source matching and transfer rules. Nor does identical total group seed imply identical paternal fitness gradients or allele dynamics. But the previously promoted phrase “strong routing contribution beyond delivery quantity” is **not supported** by this new falsifier. The correct claim is **composition-dependent delivery efficiency in one explicitly artificial Model3 reproduction operator**.

All 36 cases are post-discovery constructed source states, not independent island ecosystems; exact numeric matching of a model output is not a manipulation available unchanged in nature. No estimate of reproductive persistence, density feedback, mortality, future selection or evolutionary suicide follows.
