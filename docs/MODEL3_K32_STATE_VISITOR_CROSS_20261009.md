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
