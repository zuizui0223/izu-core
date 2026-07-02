# Five-candidate Izu model-result register

This register compares the five declared source-level candidates with profile,
prior-Monte-Carlo sensitivity, tempered SMC, stage-pattern scores, and the
B. ardens non-report envelope. It does not pool numerical values across model
families.

## Current result

The current artifact has `isolation_order` as full-likelihood winner, profile
winner, and tempered-SMC winner. Tempered SMC gives mean order-minus-bridge
compatibility of +2.034 across three seeds, and order is higher in every
replicate.

Removing flower length changes the source-level ablation winner to
`ardens_bridge_loss`; removing outcrossing, bagging, or the empty guide channel
leaves `isolation_order` first. This is a channel-dependence result. It does not
prove an isolation mechanism or dismiss bridge loss.

## Boundary

`region_order` is a fixed ordinal proxy, not distance, colonization history, or
causal isolation. Tempered SMC stabilizes integration but does not add historical
or field observations. Zero guide constraints blocks conclusions about guide loss.

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
