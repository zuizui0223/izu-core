# Prospective assurance and life-history robustness campaign

Status: specified before any new robustness outcomes; old campaign runs unchanged. Q1 is inspiration only. This adds tests, not replacement outcomes or a new claim of comprehensive island evolution.

## Question and declared interventions

Does the baseline inherited response/persistence depend on unusually effective delayed selfing or on coupling annual pollen and ovule effort to survival?

Use the exact forward-ported individual lifecycle in `model3_robustness.py`. Default settings must exactly replay the archived implementation. Added parameters enter viable parental contributions before inheritance. Pure observation fields record total available ovules, raw selfed offspring, inbreeding loss and resource-matched supplementation deficits before density regulation. These fields do not feed back or consume randomness.

1. Assurance factorial: selfing0.1/0.5 x depression0/0.5/0.9 x annual/perennial survival0/0.75 x mainland/full-island environment x initialaccess0.3/0.7 x selected/neutral. 96cells,256independent seed blocks percell =24,576runs. Each seed is104729+7919*i, i=0,...,255, shared with corresponding baseline conditions for controlled comparisons. Baseline-matching cells are intentionally replayed to recover new supplementation diagnostics, not to replace or select the old outcomes. No-selfing depression invariance is an exact tested identity; no redundant depression sweep at selfing0.

2. Effort separation: at survival0.75,selfing0.5,depression0.5, vary (ovule effort,pollen effort) among(annual,lifetime),(lifetime,annual),(annual,annual), crossed with the same2environments x2starts x2controls. 24cells x256 =6,144runs. The(lifetime,lifetime) reference comes from the assurance factorial. At survival0 both effort modes are algebraically identical, so no redundant annual-arm reruns.

All trajectories400reproductive seasons; retain common-calendar10/50/100 and replacement-time perennial40/200/400. Total30,720runs. These are local standing-variation and stationary-environment scenarios, not geological reconstructions. Resident visitor process, finite founder supports, cost0.5, saturation scale1, density cap48 and all remaining settings stay at baseline. Do not infer generality over these unvaried settings. The independent settings audit remains applicable.

## Predictions and unresolved outcomes

P1: depression is irrelevant without selfing. At zero compatible pollen, expected viable offspring equal O*a*(1-delta); stronger depression can cross below replacement. This is an accounting prediction, not a new discovery. Finite-population persistence and inherited investment trajectories are additional outcomes.

P2: ovule-only, pollen-only and joint effort scaling need not give the same perennial outcome because fertilization saturates. A difference invalidates a longevity-only interpretation of the joint baseline treatment; it does not identify one allocation as empirically correct.

P3: direction or magnitude of inherited investment/access changes may persist, vanish or reverse across assurance settings. There is no declared universal sign to recover. Distinct founder supports prevent a shared optimum even here; report distance reduction, not common-attractor convergence.

## Estimands and reporting

Every contrast is blocked by seed, environment, start and life history as applicable. Report unconditional extinction probabilities with Wilson95%intervals, unconditional survival-plus-direction frequencies, and trait contrasts conditional on BOTH compared populations surviving, with the paired denominator and each marginal extinction frequency. Define direction using the already-declared +/-0.02 trait-change band. Extinct traits stay undefined. Report distributions and Monte Carlo standard errors;256replicates imply worst-case approximate95%halfwidth6.1percentage points for a single binomial proportion, not a guarantee for rare events or all contrasts.

Compute resource-matched deficits from actual yearly ovule and offspring ledgers: Lout=1-Yout/O, Lviable=1-(Yout+Yself_viable)/O; zero O is undefined. Summarize reproductive counts before density regulation and established recruits after density regulation separately. Do not call the ideal supplemented ceiling a field treatment, dynamic genetic load, purging, or a counterfactual evolved trajectory.

All scalar settings, seeds, scripts and this document are hashed before execution. Whole-run validation checks source hashes, every case, conservation/support invariants, exact replay samples, and the new deficit identities. Preserve sign disagreement and low-survivor/unresolved cases. No favorable result changes cost, source pool, horizon or sample count. Wider fitness-cost/source-geometry tests and the properly initialized finite-grid distribution comparator are separate outstanding gates.
