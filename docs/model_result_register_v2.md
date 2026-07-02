# Five-candidate Izu model-result register

## Scope

This register reads five source-level candidates, including the fixed ordinal
`isolation_order` proxy, together with profile fit, prior-Monte-Carlo sensitivity,
adaptive tempered SMC, island-stage pattern scores, and the *Bombus ardens*
non-report envelope.

It reports compatible conclusions and their boundaries. It does not merge score
magnitudes across model families.

## Current logic

The source-level result is called **conditional and channel-dependent** only
when all of the following hold:

- full source-row likelihood, profile fit, and tempered SMC agree on the same
  leading candidate;
- the candidate set is explicitly declared;
- channel ablation results are shown rather than hidden.

When removing flower length switches the leading candidate from
`isolation_order` to `ardens_bridge_loss`, the register records that switch as a
discriminating channel result. It does not call either mechanism proven.

## Interpretation rules

- A leading `isolation_order` score means a fixed ordinal proxy is compatible
  with the retained summaries. It is not a geographic distance estimate,
  colonization history, or causal isolation effect.
- A non-leading bridge-loss score does not remove bridge loss from consideration.
  It means the bridge explanation is not unique under the present candidate set.
- Tempered SMC improves numerical integration diagnostics. It does not create
  new field evidence or resolve historical causality.
- Zero reviewed guide constraints block any claim about guide/spot loss.

## Build

```bash
python scripts/build_model_result_register_v2.py \
  --source-level artifacts/source_level_island_analysis.json \
  --profile artifacts/source_level_profile.json \
  --sensitivity artifacts/source_level_sensitivity.json \
  --tempered-smc artifacts/source_level_tempered_smc.json \
  --stage-pattern artifacts/pollinator_hierarchy_counterfactual.json \
  --ardens-envelope artifacts/ardens_nonreport_envelope.json \
  --output-json artifacts/model_result_register_v2.json \
  --output-csv artifacts/model_result_claims_v2.csv \
  --output-md artifacts/model_result_register_v2.md
```
