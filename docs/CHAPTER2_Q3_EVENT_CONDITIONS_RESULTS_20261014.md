# Q3: the event direction is constrained by threshold geometry

This outcome-informed exploratory analysis answers why the two endpoints in PR #514 need not move together. In the observed, occupied paired paths, the confirmation input states make an event gain impossible under the original restoration width. Main permits gains and forbids losses. Thus the event-direction split is not evidence against a lower conditional terminal mean. It is a consequence of the fixed starting distributions, threshold, support and shared history, with realised paths determining which permitted events occur.

This is a conditional/pathwise explanation, not an estimate of unique causal contributions from support range, variance, genotype configuration, refixation or time. The original 64-pair primary remains `unresolved`; the confirmation terminal-mean interval still crosses the operational 0.01 margin. Q1/Q2/Q4 and natural-history causes are not resolved here.

## Evidence and coverage

The [readout protocol](CHAPTER2_Q3_EVENT_CONDITIONS_PROTOCOL_20261014.md) was published at commit `aef793872e1b79b150e204e298b39b8026cb071c` before extraction. Aggregate PR #514 results were already known. The exact 410 MB raw archive is identified by SHA256 `8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e` and is available in the [PR #514 release](https://github.com/zuizui0223/izu-core/releases/tag/q3-conditional-futures-20261014). The GitHub release is not asserted to be platform-immutable.

The reader and independent sliding-window verifier reproduced all 20 fields of each of the 64 state rows and 3,904 pair rows. Both retained the three non-trigger policy-zero slots. Investment support, occupation, shared trigger expression, complete path inventory and provenance were checked. This extraction/recomputation made zero biological updates and no random draws; it does not repeat native parentage replay.

| Quantity | Main | Confirmation |
|---|---:|---:|
| Original slots | 32 | 32 |
| Triggered states / paired futures | 31 / 1,984 | 30 / 1,920 |
| Native event count | 640 | 1,280 |
| Restored event count | 1,108 | 1,208 |
| Gains (native 0, restored 1) | 468 | 0 |
| Losses (native 1, restored 0) | 0 | 72 |
| Both events | 640 | 1,208 |
| Neither event | 876 | 640 |
| Original-slot mean terminal I difference, native minus restored | 0.0209337870 | 0.0125560760 |

All sampled paired paths remain occupied through census 200. This does not prove extinction probability zero. The logical event bounds below apply to occupied paths (and, with the frozen no-arrival absorbing-extinction model, both-terminal-survivor paths), not unrestricted extinction outcomes.

## Why the directions differ

The native post-trigger investment is v. Restoration sets copies to v +/- 1/16 while preserving each individual's expressed investment v at intervention. Frozen inheritance copies existing I alleles, I mutation is disabled, and no immigrant candidates add I alleles. Thus every occupied restored mean lies between these endpoints. The reader validates the support on every saved census. The predicate remains the legacy floating calculation `B - mean_I >= 0.05`, where B is the original census-zero mean; an event requires 20 consecutive qualifying censuses.

| Input support class | Main states | Confirmation states |
|---|---:|---:|
| No supported mean can qualify | 9 | 10 |
| Centre fails, lower endpoint qualifies: gain possible | 15 | 0 |
| Centre qualifies, upper endpoint fails: loss possible | 0 | 20 |
| All supported means qualify | 7 | 0 |
| Non-trigger slot | 1 | 2 |

For main, B=0.53125. The v=0.5 states can reach qualifying low values after restoration, whereas native v=0.5 cannot qualify after the trigger. The v=0.625 states cannot reach the threshold under either arm; the v=0.375 states always qualify while occupied. Therefore main cannot lose an event under these conditions.

For confirmation, B=0.4609375. The v=0.375 native future qualifies at every census, while restoration can exceed the threshold because its upper endpoint is 0.4375. The v=0.5 and v=0.625 states cannot reach the threshold even at their restored lower endpoint. There is no gain-capable input state. This gives a zero upper bound on event gains for **any occupied future realisation** under this original intervention, not merely the observed 1,920 pairs.

Proof: if the native centre qualifies, its future eligibility sequence is all true and dominates any restored eligibility sequence pointwise. A 20-census run cannot appear only in the dominated sequence. If the centre fails and even the restored lower endpoint fails, both future sequences are all false. Their pre-trigger history is identical. Combining these two exhaustive confirmation cases forbids a gain. In main, the corresponding cases are the reverse dominance (gain-possible class) or identical eligibility (extreme classes), forbidding a loss.

## Shared history and remaining time

Eight main states and three confirmation states already have an event completed at or before the trigger. Those indicators cannot be undone: the endpoint is an *ever completed* run over years 0..200. Of main's 15 gain-possible inputs, three already had the event, leaving 12 gain-capable states. They produce the 468 gains.

If there is no pre-existing event and the shared prefix ends with k eligible censuses, even an all-eligible future needs `200-t+k >= 20`. Only confirmation state `causal_confirmation_s0.125_matched_n48_standing_MI_new_A_r6_evolving` fails this optimistic window condition: t=197, k=0, three later censuses. It is already in the support-excluded class. Therefore this specific time exclusion adds no further excluded state beyond support geometry. It does **not** establish that timing has no causal role in the other states; observed trigger times covary with entire state histories and configurations.

## Refixation describes realised witnesses, not a causal fraction

| Event joint cell | Main lower / upper / unfixed | Confirmation lower / upper / unfixed |
|---|---:|---:|
| Neither | 368 / 283 / 225 | 371 / 117 / 152 |
| Gain | 401 / 5 / 62 | 0 / 0 / 0 |
| Loss | 0 / 0 / 0 | 0 / 72 / 0 |
| Both | 296 / 147 / 197 | 632 / 424 / 152 |

All 72 confirmation losses fix at the upper endpoint before any restored event completes, and their subsequent observed fixation is absorbing. But 424 confirmation paths with an event also fix at the upper endpoint; they completed the event by that fixation census. Main has five event gains that later fix at the upper endpoint. Terminal state alone therefore cannot reconstruct a historical run endpoint.

Upper refixation is a realised witness of these 72 losses, not proof that an intervention preventing fixation would recover exactly 72 events. Selecting or comparing refixed paths conditions on a post-intervention variable. Identifying a persistence-maintenance policy would require a separately specified intervention and its full effects on frequencies, variance and reproduction.

## A lower expected mean does not order event probabilities

As a purely algebraic illustration, let v=0.375, B=0.4609375 and h=1/16, with no already-completed event and enough future time. Suppose a hypothetical restored policy settles immediately after the shared trigger at 0.3125 with probability 0.75 or 0.4375 with probability 0.25. Its expected terminal investment is 0.34375, below native 0.375, but its event probability is 0.75, below native 1. These illustrative probabilities are not estimates from the model. An expectation ordering does not imply pointwise ordering of paths or their 20-census-run probabilities.

## What is now answered and what still needs intervention

The opposite event directions have a verified input-geometric explanation under the frozen original policy, and every observed discordance respects it. Exact gain/loss counts depend on realised trajectories; the 72 confirmation losses have verified upper-refixation witnesses. This resolves the apparent contradiction between the two endpoints within these recorded states and conditions.

It does not identify the separate causal effects of range and variance/configuration. The original two arms changed both together. For example, response functions `d*w/h` and `d*V/h^2` agree at native (w,V)=(0,0) and original restoration (h,h^2), yet assign the response to different coordinates. No extra repetition of those same two assignments distinguishes them. Nor can an observed refixation association identify a fixation-prevention effect without an intervention definition.

The next minimal comparison is the [three-policy triangle](CHAPTER2_Q3_DISTRIBUTION_TRIANGLE_20261014.md): one contrast holds the exact support set fixed; another holds allele variance fixed. Its construction is feasible at all 61 trigger states. These new policy effects are still unknown. The active goal is not complete; the next gate is a separately fixed execution contract with endpoints, allocation/seeds, precision, costs and explicit approval before new biological futures.

## Reproduction and evidence files

From a checkout containing PR #515, with the downloaded archive at `work/Q3_CONDITIONAL_FUTURES_20261014.zip`:

```text
python -m pytest -q tests/test_q3_event_conditions_20261014.py tests/test_verify_q3_event_conditions_20261014.py tests/test_q3_distribution_triangle_20261014.py
python scripts/q3_event_conditions_20261014.py --archive work/Q3_CONDITIONAL_FUTURES_20261014.zip --preflight data/designs/restoration_futures_preflight_20261014.json --protocol docs/CHAPTER2_Q3_EVENT_CONDITIONS_PROTOCOL_20261014.md --out work/q3-event-conditions-fresh
python scripts/verify_q3_event_conditions_20261014.py --archive work/Q3_CONDITIONAL_FUTURES_20261014.zip --preflight data/designs/restoration_futures_preflight_20261014.json --protocol docs/CHAPTER2_Q3_EVENT_CONDITIONS_PROTOCOL_20261014.md --output work/q3-event-conditions-fresh --reader scripts/q3_event_conditions_20261014.py
```

The recorded extraction is under `data/results/q3_event_conditions_20261014/`: `STATES.csv`, `PAIRS.csv`, `SUMMARY.json`, `PROVENANCE.json`, and `INDEPENDENT_VERIFICATION.json`. The last receipt binds the independently recomputed outputs and verifier. Fresh extraction refuses to overwrite a directory. Source functions governing support are archived `frozen_source/scripts/model3_island/population.py` (`inherit`) and production `scripts/run_q3_futures_20261014.py` (empty arrivals; `mutation_traits=(False,False,True)`). Reviews are under `docs/reviews/Q3_EVENT_CONDITIONS_*`.
