# Execution addendum before full-model outcomes — 2026-10-04

Benchmarks on uniform5/7/9nodes: approximately.003/.024/.108seconds per density step. Use4workers maximum for density and2for ABM while both execute. Model3's adult genotype distribution remains fully joint.

Density grids are nested:5=[0,.25,.5,.75,1],7=[0,.125,.25,.5,.75,.875,1],9=uniform0:.125:1. All density founders and their ABM benchmark controls are first projected to the same5node support. Compare full1000period trajectories in first4history pairs for both settings/rates and both arms. Zero-mutation heat equals jump, so compute it once per grid rather than duplicating. This gives144density cases. ABM benchmark:4histories x4repeats x2settings x2rates x2arms=128cases with projected founders; biological core uses continuous founders.

ABM core stage1:32histories x4repeats x2settings x2rates x2arms=1024cases. Paired history-level bootstrap intervals for investment and assurance far-minus-near at200and1000; all16endpoint comparisons must have halfwidth<=.025 and at least90%paired occupancy. Otherwise complete fixed stage2at64histories x8repeats=4096corecases(total, retaining stage1). If precision is unresolved at max, report unresolved; do not extend seeds to obtain desired signs. Intervals conditional on paired occupancy are explicitly labeled; extinction is reported separately. No rare-attractor or natural-prevalence claim.

Common visitor histories are identical after200periods, using the near trajectory's continuation. Timing units are reproductive periods, not calibrated years. Source and runtime snapshots, atomic per-case receipts and source checks precede execution.
