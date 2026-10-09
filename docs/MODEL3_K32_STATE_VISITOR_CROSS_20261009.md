# Model3 K32: Cross original parental state and archived visitor year

## Main question

The exact expected allele direction for the source matching locus changed
from negative to positive over eight years in the original archived old
visitor history. Does the temporal reversal reflect changes in the
population's genotype/census state, annual visitor conditions, or
interactions of both? Previous original time-series evaluations sampled
only the diagonal combination of source state year and visitor year.

This new diagnostic evaluates the **complete 8×8 grid** of those
time indices, using the original Model3 reproduction function and
full finite-genetic expected allele transmission. It does NOT
modify the source reproduction or test new ecosystems.

## Source protocol

- K=32, mutation=0, adult survival=0, seed immigration=0,
  original canonical Chapter2 prior_selfing setting, four engineered
  3-locus founders and full joint diploid genotype support (27 classes).
- Reproduce 512 **nested demographic population trajectories**
  under the ONE old archived visitor history 26110601 ("near"),
  years 1–8, with exactly the pre-existing source Markov transition
  and identical source RNG seed protocol.
- Archive their integer original parent genotype census C_t at
  the start of each reproductive year t=1..8. Only the diagonal
  C_t × V_t is used to ADVANCE the population.
- Select ONE stable comparison cohort of replicate identities
  still living at parent state year8, before the eighth reproduction.
  This conditions on later occupation but avoids inadvertently
  changing the list of demographic replicates when comparing earlier
  versus later timepoints.
- For every original parent C_t in the cohort, evaluate **all
  eight archived visitor snapshots V_v** with unmodified
  reproduce(C_t,V_v). For each (t,v), calculate the
  conditional expected next high-allele frequency shift
  at matching, investment, assurance loci, and exact
  self, outcross father, outcross mother components.
- Off-diagonal C_t × V_v results are **one-step temporal
  transplant counterfactuals only**. They are NOT separate
  autonomously evolved islands or new independent histories.

Each of the 64 cells has the same rep identity list and the
same denominator. Exact child expected means follow the
unchanged mother/father/self pair-weight identities.

## Attribution with explicitly limited causal meaning

Let D(t,v) be the cohort-averaged expected matching-allele
direction under original parental genotype/census state at
source year t and archived visitor snapshot year v.
Use t=0 and t=7 for start and last parent years (source
year labels 1 and 8 in JSON); v=0 and v=7 likewise.

Define A=D(0,0), B=D(0,7), C=D(7,0), D=D(7,7).
Then exact endpoint direction change is D-A. Two
ordered decompositions are:

    state_first = C-A, visitor_second = D-C
    visitor_first = B-A, state_second = D-B

and their order-symmetrized contributions are

    state = 0.5[(C-A)+(D-B)]
    visitor = 0.5[(B-A)+(D-C)]
    interaction = D-C-B+A

so state+visitor=D-A, exactly.

The state-year term includes **evolved parent allele frequencies,
multilocus genotype structure, census and prior demographic
selection/segregation history**. The visitor term includes ONLY
the contrast between visitor snapshots from this ONE fixed old
history at the selected genotype state. Both can act jointly.
These numbers are algebraic two-order allocations, NOT separately
causal natural selection coefficients.

Also compute double-centered 8×8 cohort means:

    D(t,v)=grand_mean + state_marginal(t)
                     + visitor_marginal(v) + residual_interaction(t,v).

This descriptive decomposition gives full-year patterns beyond
the first and last year, and makes temporal interaction visible.
It does not establish independent random visitor sampling.

For the early-late 2×2 cross, **paired demographic Monte Carlo
SE** is calculated using the same retained replicate path
across all four cells; the sample size represents one source
history's nested demographic simulations, not independent
island/environment replicates.

## Scientific decision logic

- If D(7,0)>0 but D(0,0)<0, even holding the original
  EARLY visitor snapshot, late source parents have a positive
  matching-allele expectation. Thus the parental
  state/census distribution is sufficient to account for
  the direction reversal in the engineering cross.
- If D(0,7)>0 but D(0,0)<0, the late visitor condition can
  reverse direction even in the same early source
  parental genotype state.
- If neither isolated transplant changes sign but D(7,7)>0,
  a state–visitor interaction is necessary within these
  four snapshot means.
- If both transplant comparisons reverse the sign,
  multiple sufficient pathways occur under this old history.
- Conditions such as increased viable selfed-seed intensity
  and maternal seed success are still jointly determined
  by the source reproductive rules, not independently
  manipulated biological mechanisms.

The statements above refer to **expected source reproductive
filtering on frozen genotype states**. They do not identify
selection, drift, field pollinator adaptation, or whether
later positive direction can recover ancestrally lost alleles.

## How to reproduce

    pytest -q tests/test_model3_k32_state_visitor_cross.py
    python -m scripts.audit_model3_k32_state_visitor_cross --budget 8 --draws 512 --out state-visitor-budget8.json
    python -m scripts.audit_model3_k32_state_visitor_cross --budget 3 --draws 512 --out state-visitor-budget3.json

Existing core CI runs a PR420-only job
model3-k32-state-visitor-cross, validates complete 8×8
paired-cohort Mendelian/parental-component consistency,
source provenance, exact two-order algebra and archives
the original complete grid as JSON.

**Release gate:** no numerical attribution until a
successful source-locked execution and raw JSON verification.
The source code under scripts/model3_island remains unchanged;
the frozen prospective confirmatory visitor seeds 37110801-64,
natural island observations, geographical INLA and
continuous Ito SDE/SPDE validation are not accessed.


## Source-verified state × visitor results (2026-10-09)

The strict source-locked
[GitHub Actions run 37906280933](https://github.com/zuizui0223/izu-core/actions/runs/37906280933)
completed the `model3-k32-state-visitor-cross` job successfully
on SHA `a30f3676ced251f1c35ce30bbd6f585c6046ecfb`.
The [full two-budget 8×8 JSON archive, artifact 11604264037](https://github.com/zuizui0223/izu-core/actions/runs/37906280933/artifacts/11604264037)
has SHA256
`f3df76d366ea5c54a69930b0205db6d6318be784830efeb08e15a1d652ec9afe`.
The compact permanent result is
`data/results/model3_k32_state_visitor_cross_20261009.json`.

The complete 8×8 source conditional expectation grid, original
diagonal mean directions for the three loci, self/father/mother
components and paired demographic MC standard errors are in
the RAW artifact. At year8 source *parent* start, there were
512 budget8 and 506 budget3 paths alive; these SAME
replicate identities define every cell (including the initial
genotype/year1 parent states), so there is no change of
comparison cohort across time, but there is selection
on being alive by source parent year8.

### Four source-state × visitor-year conditions

These are matching-locus expected offspring high-allele
frequency changes **relative to the current parent
population**, not changes from the historical founder allele
frequency. For example, swapping visitors does NOT allow
genetic trajectories to evolve in the swapped environment.

| Original genotype-parent state × archived visitor snapshot | Budget 8 | Budget 3 |
|---|---:|---:|
| Year1 parents × year1 visitor | −0.062815 | −0.062815 |
| Year1 parents × year8 visitor | −0.046189 | −0.046189 |
| Year8 parents × year1 visitor | **−0.001723** | **+0.001798** |
| Year8 parents × year8 visitor | **+0.005533** | **+0.006607** |

Thus old visitor-year8 conditions in the UNCHANGED
initial parent state do **not** themselves reverse
the matching high-allele direction; it remains negative.
The evolved year8 source parental genotype/census states
account for most of the shift toward positive direction.
Under budget8 they need the late visitor condition
to cross zero; under budget3 the evolved source
parent states already cross zero under the early visitor
snapshot. This is a condition-specific, source-model
result rather than a universal adaptive mechanism.

### Two-order symmetric 2×2 accounting and Monte Carlo errors

| Quantity for matching allele expected direction | Budget8 | Budget3 |
|---|---:|---:|
| Actual diagonal year8 minus year1 | +0.068348 ±0.000635 MC SE | +0.069422 ±0.001097 |
| **Symmetrized source-parent-state contribution** | **+0.056407 ±0.000587** | **+0.058704 ±0.001056** |
| **Symmetrized visitor-year contribution** | **+0.011941 ±0.000099** | **+0.010718 ±0.000097** |
| State share of the sum | ~82.5% | ~84.6% |
| Visitor share of the sum | ~17.5% | ~15.4% |
| Interaction difference-in-differences (NOT an extra additive main effect) | −0.009370 ±0.000197 | −0.011817 ±0.000193 |

State and visitor components sum EXACTLY to the
early/late diagonal contrast, with the interaction
allocated half to each in the two-order mean.
The interaction must not be added again to those
two contributions. Their MC errors capture only
original source demographic-path variation nested
under a **single** archived visitor history.

### Original source reproductive channels

The source selfed-seed contribution to matching-high
expected direction was −0.034895 in the year1
parent group. By year8 it became **+0.011981**
(budget8) or **+0.010327** (budget3). In contrast,
source outcross father and mother components
were both negative in the year8 diagonal cells:
approximately −0.003230 and −0.003219
(budget8), and −0.001861 and −0.001859
(budget3). The exact positive final direction
is the sum of these contributions.

This explains how selfing-associated allele
transmission under the original source population
can change direction while pollen-mediated
outcross components are still negative.
But selfed-seed contribution is a **population
genetic transmission covariance**, not the
isolated causal effect of activating selfing.
It may change simply because allele/genotype
frequencies, reproductive effort, parental
identity and census change together.

### What the experiment does NOT solve

The majority assigned to the "source parent
state" contains genetic background, assurance
locus frequency, floral investment locus,
population size and accumulated demographic
drift. It is NOT a 82–85% causal fraction
uniquely attributed to reproductive assurance
or auto-selfing. The visitor contribution
compares two years of ONE archive visitor
trajectory, not randomly sampled or
independent pollinator environments.

The 8×8 crossing identifies which
*frozen-genotype + old-visitor snapshot*
combinations can produce positive one-step
matching-allele direction. It does not
establish how real pollinators changed or
cause a year8 population to arise from
a year1 visitor transplant. No frozen
prospective confirmatory histories, natural
island measurements or continuously valid
SDE/SPDE inference were used.
