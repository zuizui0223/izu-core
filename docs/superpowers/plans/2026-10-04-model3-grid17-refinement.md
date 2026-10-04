# Additional 17-node precision stage

Subsequent user instruction: determine required resolution before additional
full computation. This stage is prepared but pending, NOT an automatic next
run. See `2026-10-04-model3-resolution-screen.md` and
`docs/MODEL3_RESOLUTION_SCREEN_20261004.md`. The completed operator screen
does not justify declaring17 sufficient; computational feasibility must be
resolved before authorizing its full execution under the current plan.

User requested additional numerical precision on 2026-10-04 while the fixed
13-node stage was active. Four of its 32 cases were complete; three did not
meet the existing 9-to-13 terminal tolerance. This is an outcome-informed
numerical refinement, not a new prospective ecological test.

Preserve the complete 13-node run without modifying its sources or restarting
valid cases. Then run all 32 positive-mutation conditions on 17 uniform allele
nodes: both reproductive settings, four original histories, near/far arms,
original jump and heat-FV operators. Do not select cases by effect direction
or numerical success. Retain 1,000 generations, the same five-node projected
founders, mutation probability .01, width .05, and all ecological parameters.
All three traits evolve. No ABM rerun or ecological retuning is required.

Compare 13-to-17 and retain 9-to-13 diagnostics. The terminal criterion remains
maximum absolute difference among the three trait means < .01 for every case.
Also report full-trajectory differences and population masses. Passing a finite
refinement check is not a continuum theorem. Approximation error between jump
and heat is interpretable only after checking resolution in each branch.

Seventeen allele nodes imply 3,581,577 unordered three-locus diploid genotype
states and 4,913 gametes, about 4.75 times the 13-node genotype state count.
Do not run this simultaneously with the two 13-node workers on this 16-GB host.
Use one worker in an isolated child process per case to release all cached
arrays between cases. Before the full stage, measure a short setup/step timing
and peak-memory probe after the 13-node workers exit. It must use the same
biology but supply no ecological acceptance criterion. Retain its resource
record. If memory is insufficient, preserve the pending stage and assess an
algebraically equivalent memory improvement; do not silently reduce the grid,
traits, conditions or horizon, or alter the mutation operator.

The runner must refuse an incomplete or corrupted 13-node predecessor, verify
source archives on resume, retain atomic case receipts, and record predecessor
identity. Summaries must reject missing/corrupt receipts and initial-state
mismatch. Preserve all failures and do not declare the full goal complete
merely because one fixed numerical budget has been exhausted.
