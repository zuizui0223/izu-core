# Continued isolation versus imposed common environment

The completed experiments were paired by reproductive setting, mutation probability, visitor-history seed and demographic replicate. All2,048 far pairs match exactly through the first200 updates. From update201 onward one retains strong isolation, while the other receives the exact weak-isolation visitor continuation. Near references are shared. Source output task/hash checks precede comparison.

At endpoints200/400/1000, all three populations must survive for a triplet to contribute to trait comparisons. Occupancy and excluded triplets are reported separately. History means of eligible demographic repeats are bootstrapped5,000 times for descriptive95% intervals. Period200 experiment differences are exactly zero in every setting, rate and trait. This is an exploratory comparison of already completed, frozen experiments.

For delayed selfing with capacity cost0.5 and mutation probability0.01, all512 triplets survive at period1000:

| Contrast | Investment | Selfing capacity |
|---|---:|---:|
| Sustained far minus near | -0.3133 [-0.3310,-0.2954] | +0.1003 [+0.0899,+0.1108] |
| Equalized far minus near | -0.1301 [-0.1492,-0.1124] | +0.0558 [+0.0455,+0.0664] |
| Sustained far minus equalized far | -0.1832 [-0.1978,-0.1688] | +0.0446 [+0.0373,+0.0522] |

The same-environment intervention attenuates the isolation contrast relative to continued isolation, but does not eliminate it within800 subsequent updates. This supports finite-horizon history dependence. It does not establish irreversible degeneration, alternative attractors, equilibrium, or recovery under natural recolonization: environmental equalization was imposed experimentally.

Matching-position intervals include zero for the three displayed contrasts. All four setting/mutation combinations and all three endpoints are retained in `data/results/model3_exposure_experiment_comparison_20261005.json`; the focal illustration must not replace that complete report. Timing and selfing-capacity cost differ jointly between settings.

The script `scripts/compare_model3_exposure_experiments.py` verifies task and output hashes, pre-intervention equality, complete sustained-run keys, shared survivors and zero initial experiment difference. Interval values differ slightly from earlier summaries because the explicitly paired comparison uses its own fixed resampling seed; point estimates for fully surviving cells agree.

These are ABM conclusions. High-resolution positive-mutation deterministic/diffusion comparison and the fixed-capacity intervention remain pending.
