# Reading the prospective evolutionary campaigns

This is a reporting guide, not a change to either frozen simulator or design.
No terminal campaign outcomes were used to choose these comparisons.

## Required order

1. Admit only terminal, source-verified, complete artifacts and exact replay checks.
2. Report persistence before interpreting floral change. At each checkpoint,
   every replicate contributes to exactly one of extinction, alive/decreasing,
   alive/small-change, or alive/increasing. The direction band is the frozen
   +/-0.02. Denominators are all replicates, not survivors only. Marginal Wilson
   intervals are Monte Carlo uncertainty, not simultaneous inference across cells.
3. Selected-minus-neutral trait differences use only seeds alive in both arms;
   report that denominator and each arm's extinction count. These contrasts do
   not isolate selection from all subsequent demographic feedback.
4. In the assurance supplement, compare depression 0.5 and 0.9 against zero at
   the same selfing, environment, life history, start and control. In the effort
   supplement, compare each annual-effort intervention to the lifetime/lifetime
   reference in the assurance campaign (selfing 0.5, depression 0.5). Use matched
   seed blocks and fail if any required reference is absent.
5. Read pollen deficit before selfing alongside viable-seed deficit after
   selfing and depression. Cumulative deficits are ratios of summed offspring
   and ovules, not means of annual ratios. An extinct population with zero
   ovules has an undefined annual deficit. Cumulative ledgers stop accumulating
   at extinction; low cumulative output is not automatically low efficiency.
6. Report actual recruits separately from expected offspring before density
   regulation. Inbreeding loss here is expected viable-offspring loss from a
   fixed depression parameter, not purging, inherited load or measured deaths.

## Time and ecological claim boundaries

Compare calendar years 10/50/100 directly between life histories. Annual
10/50/100 versus perennial 40/200/400 is a comparison using the declared adult
replacement-time proxy, not empirically calibrated generations. A checkpoint
appearing in both comparisons is one observation, not another replicate.
The year-400 endpoint is a stationary-environment stress scenario.

Keep absence of change, sign disagreement, extinction and too-few-paired-
survivor results visible. Do not infer shared-optimum convergence from access
distance reduction: the disjoint founder supports prohibit a shared optimum.
No mutation or plant immigration replenishes standing variation. No Q1 region
is an input or calibration target. The model can test conditional mechanisms
in island ecology; reproducing actual regional flower evolution is not claimed.

## Outputs

`endpoints.csv`: individual seed trajectories at declared checkpoints, with
reproductive ledgers when available. `condition_summary.csv`: extinction and
joint survival/direction frequencies plus survivor trait summaries.
`selected_vs_neutral.csv`: paired control contrasts.
`between_start_distance.csv`: paired starting-state distances.
`assurance_effort_contrasts.csv`: paired depression and effort interventions
(supplement only). Every output must retain its verification provenance.

Full distribution-counterpart trajectories and unvaried source-pool/fitness-
cost assumptions remain separate outstanding checks; these tables alone do
not certify ecological robustness or finish the larger scientific goal.
