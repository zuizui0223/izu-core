# PR #420: Pathwise reproductive direction versus finite sampling (2026-10-09)

## Objective and fixed experiment

Determine whether an eight-generation mean-genetic response arises from a
systematic **source-conditional reproductive direction**, while preserving
finite segregation/recruitment noise as an explicit martingale component.

Source model remains frozen: capacity K=32, mutation rate=0, 8 synchronized
annual updates, adult survival=0, seed immigration=0, canonical Chapter 2
`prior_selfing` parameters. Use only archived visitor history **26110601**
(near) for years 0–7 and the established engineered four-founder,
27-class, three-locus diploid genotype support. The 512 trajectories per
budget are nested demographic replicates of ONE environment; there are
**zero new independent visitor-history replicates**, no natural-plant
observations and no use of prospective 37110801–37110864 histories.

Two budgets: 8 (main) and 3 (resource-stress sensitivity). The same
unmodified `scripts/model3_island/reproduction.py` mating weights,
individual pollen self-exclusion, capped Poisson census, and exact full
diploid Mendelian genotype law generate every transition.

## Exact decomposition

Let (p_{t,g}) be the realized parental genotype frequency, and
(q_{t,g}=Q_g(C_t,E_t)) the conditional next-child genotype probability
from canonical reproduction. For surviving offspring population N>0,
let `p_next` be realized child genotype frequency:

```text
p_next - p = (q - p) + (p_next - q).
```

The **first** term is a directional offspring-production/mating/filtering
operator (not a uniquely causal "natural selection coefficient").
The **second** is finite segregation and multinomial offspring-sampling
noise, mean-zero conditional on `C_t,E_t,N>0`. It is not a synthetic
independent neutral-drift intervention.

Use the three high-allele frequencies (`.75` allele at each locus) as
the linearly inherited metrics: matching, floral investment, reproductive
assurance. Because the two alleles at each source locus are `.25/.75`,
the corresponding source mean trait is **0.25 + 0.5 * high allele freq**.
The same exact identity holds for cumulative frequency/trait changes.

For a trajectory surviving all eight generations, the sum of each source
direction and finite noise is exactly the net frequency change. Extinct
trajectories are counted separately and do NOT receive fictitious zero
trait/frequency means. Conditional-on-survival endpoints require a
selection-conditioning caveat.

For surviving paths, variation across replicates also obeys

```text
Var(total) = Var(cumulative filter) + Var(cumulative sampling)
           + 2 Cov(cumulative filter, cumulative sampling).
```

Because the direction is state-dependent, the two accumulated components
need not be independent: finite sampling changes future parent genotypes
and hence future reproductive filtering. **Therefore the individual
variance terms are not additive causal fractions**; the covariance can
even be negative and substantial.

## Source-verified eight-generation results

Source-run CI <https://github.com/zuizui0223/izu-core/actions/runs/37885303545>
dedicated `model3-k32-pathwise` job completed **successfully**.
Full raw output: <https://github.com/zuizui0223/izu-core/actions/runs/37885303545/artifacts/11595743566>;
permanent compact receipt:
`data/results/model3_k32_pathwise_direction_sampling_20261009.json`.

*Values are changes in high-allele frequencies, not natural phenotypic
measurements or selection gradients.*

| Budget | Survivors | Match: filter / noise / net | Investment: filter / noise / net | Assurance: filter / noise / net |
|---|---:|---|---|---|
| 8 | 512/512 | -0.13049 / +0.00861 / -0.12189 | -0.29640 / -0.00848 / -0.30487 | +0.48094 / -0.00337 / +0.47757 |
| 3 | 501/512 | -0.10630 / +0.02197 / -0.08433 | -0.31965 / -0.00906 / -0.32871 | +0.48519 / +0.00271 / +0.48790 |

The directional-filtering response is qualitatively consistent across
both resource budgets. It is a property of this source model/old visitor
history, not a confirmation about islands or independent environments.

### Selection-by-history and covariance

For budget 8, surviving accumulated component variance across 512
trajectories:

| Trait high-allele freq change | Filter variance | Sampling variance | 2 covariance | Total variance |
|---|---:|---:|---:|---:|
| Match | .009954 | .047835 | +.003672 | .061461 |
| Investment | .005773 | .038246 | -.011894 | .032125 |
| Assurance | .014111 | .019688 | **-.032208** | **.001591** |

At budget 3: assurance variance filter .023722, sampling .029569,
twice-covariance **-.051765** and total **.001526**.

**Critical boundary diagnostic:** assurance starts with high-allele frequency
0.5000 in all engineered founders. Among surviving trajectories it ends at
**0.97757** (budget 8) and **0.98790** (budget 3), close to the upper bound
of 1. This severe frequency ceiling alone constrains realized endpoint
variance and can induce negative correlations between the cumulative
source-filter term and the cumulative sampling residual. The covariance
is therefore **not sufficient evidence of stabilizing selection or
biological canalization**. A frequency-boundary-matched neutral or
counterfactual comparison would be required to isolate feedback from
a nearly deterministic saturation ceiling. All are Monte Carlo
moment estimates of survival-conditioned histories. The covariance
reduces endpoint heterogeneity markedly. A plausible interpretation is
that directional reproduction responds to the stochastic state reached
earlier, but **a causal stabilizing selection mechanism is not
identified by this covariance alone**. Test alternative payoffs and
genuine neutral counterfactuals separately before applying biological
labels.

## Exactness, validation and stopping rules

The telescoping identity and per-state conditional multinomial covariance
are mathematical identities for the frozen source transition (under
positive recruited offspring census); they are checked on every path
with tests. The Monte Carlo ensemble statistics are NOT mathematical
theorems or independent ecological replication.

Run:

```bash
python -m scripts.audit_model3_k32_pathwise_selection_drift --out pathwise-budget8.json --budget 8 --draws 512
python -m scripts.audit_model3_k32_pathwise_selection_drift --out pathwise-budget3.json --budget 3 --draws 512
pytest -q tests/test_model3_k32_pathwise_selection_drift.py
```

The canonical `.github/workflows/ci.yml` includes a PR#420-scoped
`model3-k32-pathwise` job which verifies source provenance and
archives JSON. The original biology files remain unmodified.

**STOP:** No pure adaptive selection coefficient, causal genetic-drift
fraction, cross-island transfer, natural genetic validation, continuous
Ito SDE or full SPDE has been demonstrated. The viable next scientific
question is whether an externally defined *neutral-mating/fecundity
counterfactual* would change the direction or endpoint covariance; such
an intervention must be reported as different biology rather than
mislabeling it frozen canonical Model 3.
