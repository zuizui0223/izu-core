# Reproductive assumptions alter local selection and its reciprocal effects

## Design and interpretation

This exploratory sensitivity diagnostic was specified before calculation in `data/design/model3_parameter_selection_20261005.json`. It crosses delayed/prior selfing, depression 0/0.25/0.5/0.75/0.9, investment cost 0/0.25/0.5/1/2, capacity cost 0/0.25/0.5/1/2, and pollen discount 0/1. All 500 combinations retain the same five controlled communities and 45 interior resident states used in earlier diagnostics. The 112,500 cases are points in a designed parameter/state grid, not independent populations or an empirical distribution of islands. Main-experiment parameters were not altered.

The cost grid brackets the existing coefficient 0.5, including zero-cost structural controls and doubled/quadrupled values. Depression spans no viability loss to strong loss while excluding complete loss, which can make zero-pollen selfing fitness singular. These are model stress tests, not literature-calibrated plausible ranges. Other functional forms, environmental dynamics, genetic architecture and evolutionary sequences are not tested here.

## All four selection regimes occur

With a gradient deadband of 1e-7:

| Investment selection | Capacity selection | Grid cases |
|---|---|---:|
| Decrease | Increase | 36,779 |
| Increase | Increase | 35,111 |
| Decrease | Decrease | 15,586 |
| Increase | Decrease | 25,024 |

None falls in the neutral band. These counts depend on grid construction and must not be reported as the probability of a syndrome in nature. Their scientific role is to demonstrate that the model does not force both syndrome directions across all reproductive settings.

## Reciprocal reinforcement has a boundary

Increasing investment reduces the local selection gradient on capacity at all 112,500 tested cases. Increasing capacity reduces the investment gradient at 112,475 cases but **increases it at 25**. Thus the narrower prior finding that both cross derivatives are negative does not generalize to the expanded parameter domain.

The 25 positive cases all involve delayed selfing, depression 0.9, pollen discount 1 and the existing `leftdup8` community, at investment 0.7, capacity 0.3 and matching 0.2 or 0.35. They span selected investment costs 0, 0.25 or 0.5 and all five capacity costs, with the exact combinations retained in the verification receipt. They are not 25 independent ecological replications. At zero costs and matching 0.2, for example, the investment gradient is +0.8490, capacity gradient -0.4258, and capacity's cross effect on investment +0.03189. Local reciprocal effects do not by themselves establish a realized feedback loop or temporal sequence.

The positive exceptions were independently recalculated from mutant log-fitness rather than the analytical gradient function, using two outer differentiation steps. All remained positive; maximum discrepancy from the saved cross derivative was 3.33e-8. A biological attribution of this reversal to specific maternal/paternal terms has not yet been established and is not inferred solely from its association with high depression and discount.

## Numerical verification and reproducibility

All 225,000 analytical trait gradients were checked against independently computed mutant log-fitness differences, with maximum absolute discrepancy 1.256e-9 (declared tolerance 1e-6). Cross-derivative steps 1e-4 and 5e-5 had zero sign disagreements and maximum absolute discrepancy 1.402e-7. No parameter setting was removed for disagreeing with the expected syndrome.

Run from repository root:

```powershell
$env:PYTHONUTF8='1'
python -m scripts.audit_model3_parameter_selection
python -m scripts.verify_model3_parameter_selection
```

The generator checks frozen input/source hashes before calculation. Numeric arrays are in `outputs/model3_parameter_selection_20261005/fields.npz`, with axis definitions embedded. Receipts: `data/results/model3_parameter_selection_20261005.json` and `data/results/model3_parameter_selection_verified_20261005.json`.

The remaining ecological test is whether evolutionary timing and persistence change across these selection boundaries. This diagnostic does not supply that result, or resolve the stopped high-resolution deterministic/PDE comparison.
