# Model 3 selection correction and closeout — 2026-10-04

Base: d83ceb569e198d90d2f0fbe4b430b49608e12e78 (Evolution Letters preparation).
Repair branch: codex/model3-selection-repair-20261004. Main and Oikos frozen surfaces are unchanged.

## Why a correction was necessary

The old monomorphic threshold differentiated population-wide investment, changing resident pollen supply and recipient competition simultaneously. That is not a mutant invasion gradient. For access .2, investment .5, assurance .5 and the central four visitors, it gave +0.002988756; fixed-resident invasion gives -0.152264826 and the independent low-frequency density calculation gives -0.152264825.

The old expression is retained solely as a labelled whole-population sensitivity. No archived simulation result was overwritten.

## Corrected mechanism

The derivative holds the resident environment fixed and uses mutant parental-genome contribution W = .5 F + .5 P + S. Mutant ovule cost affects its maternal and selfed seed; paternal output is determined by mutant export and resident mothers. The corrected analytic derivative matches finite differences for delayed/prior selfing, pollen discount and assurance cost, including empty communities and heterogeneous visitors.

The controlled gradient is a local selection statement, not a prediction that every finite endpoint reaches the same phenotype.

## Full frozen bridge rerun

Same 128 histories, 5 access states, 3 investment states, 3 interventions, and all 200 annual visitor communities. No retuned thresholds, changed seeds or altered ecological processes.

At access .5, mean far-minus-near investment selection gradients:

| Intervention | i=.3 | i=.5 | i=.7 |
|---|---:|---:|---:|
| Natural assembly | -.528074 | -.537250 | -.538250 |
| Richness matched | +.010550 | +.012642 | +.014214 |
| Visitor pooled | -.598511 | -.614043 | -.603867 |

In all 15 access-investment states, all 128 natural and pooled histories shift negatively. Matching breaks universal negative direction and leaves small mean contrasts. Matching thins the near assemblage; it is not restoration of the far assemblage, and also affects identity persistence.

Source: [corrected gradients](../data/results/model3_corrected_invasion_bridge_20261004.json), including all per-history contrasts and source hashes.

## What remains unchanged

- Reproduction, inheritance, ABM and density numerical operators were not changed.
- Exact multivariate Price rerun: 48 cells, maximum error 7.77e-16 (earlier runtime 7.22e-16).
- Full-G response rerun: 46/48 strict component-sign gates; two near-zero components still fail.
- Every raw finite case was admitted and recomputed: 4 settings x 3 starts x 128 histories x 4 repeats x 2 arms = 12,288 arm cases. Endpoint classes, occupancy and branching conclusions are unchanged.
- No alternative-endpoint branching supported by the frozen criterion.
- Prior selfing does not exceed the structural-control endpoint maximum; the clearest descriptive amplification remains assurance cost. Endpoint maxima are not causal paired tests or estimates of natural prevalence.
- No new field calibration or long-term equilibrium claim.

## Admission guard repairs

Price failure or missing response evidence is rejected. The raw settings, initial states, history IDs, demographic repeats, numerical domains, occupancy, means, classifications and summaries are checked. Branching flags are recomputed rather than trusted. Historical input files must match the reviewed immutable-workflow hash manifest.

The original promotion requirement said response support but supplied no tolerated failure proportion for the 48 local response checks. This repair conservatively withholds automatic promotion when that gate is incomplete: current 46/48 is not silently converted into 48/48. This administrative result does not negate exact Price, joint selection, or observed finite endpoints. Do not relabel a new tolerated fraction as preregistered.

The summary's central-state evidence is implicit only when all 45 states pass. Admission of partial-state summaries requires richer state-level evidence rather than assuming the central state passed.

Sources: [re-adjudication](../data/results/model3_corrected_adjudication_20261004.json), [legacy input identities](../data/results/model3_repair_input_provenance_20261004.json).

## Trajectory capture

An optional --trajectory-dir now saves compact population, trait mean/variance, allelic diversity, heterozygosity, reproduction and density diagnostics with SHA-256 receipts. The same immutable RNG streams are used. A prespecified first-history central-start assurance-cost near/far pair was replayed through all 200 periods: both endpoints exactly match the original artifact at 1e-12, and stored arrays match in-memory arrays.

[Replay receipt](../data/results/model3_repair_capture_20261004/receipt.json).

This is a storage/reproduction check, not evidence that 200 periods are adequate. The full 12,288 biological trajectories were not rerun because their operator and frozen results are unchanged; all their endpoint records were revalidated. No conclusion about global time-scale sufficiency or two attractors is added.

## Scientific conclusion

Isolation shifts the local reproductive selection field toward reduced floral investment under the declared model. This shift survives correction from a population derivative to individual invasion selection. Joint assurance-selection and finite outcomes are separate evidence layers; common direction does not guarantee uniform realized endpoints or historical repeatability. The theory does not reproduce literal floral colour, geographical rates, or natural syndrome frequencies.

## Verification

Regression tests include the sign-reversal counterexample, independent density low-frequency comparison, malformed/incomplete/incorrect-source result rejection, and failed Price admission. Relevant existing continuum/PDE, inheritance and manuscript boundary tests were also executed. This is focused repair verification, not a claim that all repository CI was rerun locally.

A fresh independent review found no blocking numerical/admission defect; its provenance and document-consistency suggestions were incorporated. Full joint-vector recheck completed: all four settings retain 45/45 passing states, minimum joint-history fraction 127/128, negative correlational selection in all checked cells. The frozen gamma step settings and sign-stability checks were verified from the fresh output. See model3_repair_joint_vector_recheck_20261004.json.

Final focused gate: 48 tests passed in Python 3.10; broader continuum/PDE and 128-history bridge tests also passed earlier in this repair. Full repository CI was not run. Independent review found no blocking defect. Automatic approval denied removal of local pytest scratch directories; those untracked directories remain and are not part of the commit.
