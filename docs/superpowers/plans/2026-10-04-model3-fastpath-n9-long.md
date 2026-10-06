# Nine-node long integrated admission

Prerequisite: all eight n9/40 cases verified against saved arrays and frozen
source hashes. Run the same eight cases, history76001, to1000 periods.
Keep n9 grid, founder support on5 nodes, mutation0.01, biological rules,
rounding1e-8, 16-million-value allocation cap and one worker unchanged.
Compare compressed and exact same-grid density at every period; retain
checkpoints200/400/1000. Accept only all8 complete, normalized L1<=1e-5,
trait gap<=1e-6, mass gap<=1e-5, negative mass<=1e-10, no occupancy mismatch.
Preserve failures; no tolerance tuning. This admits solver accuracy only,
not n9 grid adequacy. No17+ production follows automatically.
Use a separate runner and gate_n9_1000 directory; preserve live sources.
