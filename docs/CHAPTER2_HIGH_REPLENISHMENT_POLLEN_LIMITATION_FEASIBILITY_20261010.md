# High-replenishment pollen limitation and a failed saturation feasibility screen

**10 October 2026: source-executed POST-OUTCOME static feasibility analysis only. Not independent history replication or an evolutionary intervention.**

## Model interpretation

The original higher-replenishment (near) and lower-replenishment (far) arms begin with the same visitor assembly but receive different subsequent visitor replenishment. The near arm was NEVER calibrated to a pollen-saturated natural mainland.

The independent historical 64-visitor-history fixed-plant assay (48 plants, fixed autonomous assurance a=0.5, visitor snapshot 400) had raw deficit **0.390148615 near** and **0.494835185 far**. The assay measures raw deficit *after autonomous selfing*, not an outcross fertilization deficit. With delayed selfing,

\[
d_{\mathrm{raw}}=1-\frac{F+a(O-F)}{O}=(1-a)(1-F/O).
\]

Thus the mean fraction of ovules fertilized by outcross pollen is **0.219703 near** and **0.010330 far**. Approximately 39% of ovules on the near arm remain unfilled even after a=0.5 autonomous assurance; the fraction NOT fertilized by outcross pollen is roughly 78%. These quantities are not terminal evolved-population statistics. The values follow from source pollen saturation, functional trait matching, pollen recipient background and visitor-history rules, not from a calibrated mainland/island experiment.

## Executed fixed design and source result

The feasibility check reused original history seeds 76001–76064, both original near/far visitor snapshot 400 states, and unchanged original N48 founder genotypes. Only pollen_budget was multiplied by the prespecified levels 1, 2, 4, 8 and 16. Original baseline raw-deficit means must replay exactly. The frozen admission threshold required mean near outcross F/O >=0.90 AND at least 60/64 near histories individually F/O >=0.90.

| Pollen budget multiplier | Near mean F/O | Near histories meeting 90% | Far mean F/O |
|---:|---:|---:|---:|
| 1 | 0.2197 | 0/64 | 0.0103 |
| 2 | 0.3761 | 0/64 | 0.0197 |
| 4 | 0.5765 | 1/64 | 0.0360 |
| 8 | 0.7662 | 19/64 | 0.0611 |
| 16 | **0.8871** | **48/64** | 0.0926 |

**Predefined within-grid verdict: SUFFICIENCY_NOT_REACHED_IN_FROZEN_FEASIBILITY_GRID.** Even at 16×, both near admission requirements fail. All 640 rows from 64 previously exposed histories × 2 arms × 5 multipliers were retained. At snapshot 400 all 64 near histories had >=1 visitor, but 50/64 far histories had none; increasing pollen budget cannot restore any pollen transfer in those no-visitor states.

Original source run: GitHub Actions workflow 38041114105. Complete source JSON artifact ID 11666036103, 206,902 bytes, SHA-256 c40bf96297405f620ff637d5f875490c7a38d6480726ffcdc3527d479c91a5c7, independently downloaded and checked. Permanent files: data/design/chapter2_near_pollen_sufficiency_feasibility_20261010.json, scripts/audit_chapter2_near_pollen_sufficiency_feasibility.py, tests/test_chapter2_near_pollen_sufficiency_feasibility.py, data/results/chapter2_near_pollen_sufficiency_feasibility_receipt_20261010.json.

## Claim boundary

The main four-setting 64-history prospectively confirmed experiment established reduced floral-investment divergence after assurance evolution **only between the two originally pollen-limited environments at a fixed 1,000-update horizon**. It does not establish the same pattern between a fully pollen-saturated mainland and a severely depleted island. This source-only feasibility screen cannot decide whether that generalization is true, because none of its fixed multipliers satisfied the saturation gate. Do not tune to unregistered multipliers after seeing this result and claim confirmation.

The no-cost delayed-selfing control also has automatic direct incentive for increased assurance when ovules remain unfertilized and viable self seeds are possible. Trade-off settings provide more discriminating biological checks; the explicit assurance-cost case had the weakest attenuation, +0.1007, and near-side investment effect −0.0789.

A separate previously frozen 6,400-reproductive-season deterministic density and genetic input diagnostic failed stationarity; the high-standing advantage over low-standing with mutation reversed between 800 and 1,600. That is **not** a long-horizon rerun of the main four-setting prospective 1,000-update experiment, and much of its deterministic mass becomes sub-individual. Therefore it is a finite-horizon caveat, not a demonstrated reversal of the main primary result.

**No new natural ecology, visitor-history independent replicates, or evolutionary persistence evidence is supplied by this diagnostic.**
