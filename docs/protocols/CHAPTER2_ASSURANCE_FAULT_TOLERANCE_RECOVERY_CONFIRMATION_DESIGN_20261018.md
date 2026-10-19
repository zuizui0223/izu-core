# Chapter 2: prospective Q3 fault buffering versus genetic recovery

**2026-10-18 / NON-EXECUTABLE DESIGN, NOT REGISTERED CONFIRMATION.** This is
one workstream within PR #590's sole developing NEE Article. It neither starts
a biological campaign nor authorizes one. Old registered Q1-Q4, the 384
both-inconclusive trial, the source-only 2,304 HIGH-I exclusions, and the
2-by-2 synthetic pilot are retained with their original inferential rank.

## Three article questions retained

**Q1 (supported within Model3):** Is evolution of A necessary for I to
decline under reduced effective pollination? No under the tested conditions;
fixed expressed A=0.5 still self-fertilizes.

**Q2 (genetic clock and actual return distinguished):** When does a living
population lose the alleles necessary for its founder-mean I to be attained?
Is the full maternal+paternal fitness effect of increasing I positive under
the **specific imposed returning visitors**? Genetic structural clock t_G
is NOT the stochastic no-return time t_star.

**Q3 (new randomized test):** Does allowing A to evolve change genetic
upper-support loss while also changing persistence and short-horizon
reproductive fault buffering? **No effect direction is selected.**

## Before studying any new outcomes: the two policies

### Pre-assignment phenotype matching is essential

**Correction after code review, before any future confirmation:** "same genotype" alone does NOT guarantee comparable initial expressed assurance. In the earlier bundled-policy exploratory pilots, all adults in the fixed-A arm expressed exactly 0.5 but original evolving-A adults varied in phenotype because each inherited allele was independently drawn. Such a study changes initial A heterogeneity AND ability to evolve, so it cannot isolate the causal effect of evolvability alone.

For a genuinely focused NEW study, require EVERY initial adult in BOTH policy arms to express precisely A=0.5, while the inherited A gene remains polymorphic. A prospective technical construction is each adult's diploid A allele pair assigned from the balanced categories (0.25,0.75), (0.5,0.5), (0.75,0.25), with source-paired alleles summing to exactly one, 16 adults of each category for 48 founders. Matching/M and investment/I genotype alleles, all individual IDs, birth records and allele-origin identity are unchanged. Both historical policies receive the SAME constructed PlantState, and only the ASSURANCE EXPRESSION POLICY differs after start. Keep A mutation off in both policies for this strict-access primary; genetic assortment and segregation can generate expressed-A variance in subsequent offspring. Starting allelic diversity is not equal to initial expressed phenotype variance.

A fail-closed construction/validation helper is implemented in `scripts/chapter2_q3_balanced_assurance_founders_20261018.py` with pure-source tests. DO NOT use it to silently retrofit or re-run the already-frozen PR #596 6×6 exploratory variance pilot. That pilot may inform the variance of its original bundled policy effect but is not pure A-evolvability inference. An independent post-design variance calibration with matched t0 A expression must precede any causally identified confirmatory Q3 effect test and its full #585 power/SESOI method gate.

Cross NEW independent founder-genotype draws (F) with NEW independent
functional visitor-history draws (V). Each F-by-V cell receives both
historical policies from exactly the same t=0 genetic state, visitor history
and prespecified demographic master-stream identity. These are a
two-axis factorial, not F*V independent islands. The generator *names*
and master seeds match; after policy trajectories diverge the algorithm
need not consume the same number of random draws and individual events
are NOT synchronized.

- `fixed`: expressed assurance A remains 0.5, self-fertilization is
  available. Record both expressed A and inherited latent A alleles.
- `evolving`: expressed A comes from its diploid alleles with standing A
  variation seeded BEFORE any environment intervention. All t=0 founders
  share exact DNA with fixed-arm founders. Do not introduce a beneficial
  extra mutation mechanism only in evolving-A histories.
- Lock I mutation and plant seed immigration at ZERO in BOTH policies
  for the primary strict allele-access theorem; the A mutation decision
  must also be IDENTICAL across arms. Proposed first study: A mutation
  off in both, standing A polymorphism on at t=0. Independent mutation-
  enabled follow-up is a distinct sensitivity, not mixed into main clock.
- Keep primary historical cost/timing as costless delayed selfing; use
  prior selfing, pollen discount and direct assurance cost as distinctly
  labelled prespecified generality strata. NO assumption that a constant
  A=0.5 is a no-selfing policy.
- Model3 finite diploid operators, full maternal+paternal+viable-self
  ledger, K=48, no adult carryover, source background/cost parameters
  are the intended biological source. No new sex locus or genetic load.

The visitor time line must be explicit: pre-exposure full functional
visitors; low-service period; imposed complete and non-recolonizable
functional visitor removal at T_E; follow-up beyond T_E. Candidate
engineering schedule T_E=35 from the **tiny original synthetic pilot**
is not a biologically calibrated time; it is a proposed fixed intervention
setting to be reviewed without adaptive selection. Period and horizon
(e.g. 100 years) remain PENDING a separate run-resource review.

## Primary event state machine: no survivor-only policy contrast

One case is one originally assigned F,V,demographic-repeat,policy path.
Define I_star = that case's original t0 mean I and max_I(t) of living
diploid I alleles. Assume no I mutation, no seed immigration.

- `alive_accessible`: living and max_I(t) >= I_star.
- `alive_closed`: living and max_I(t) < I_star, hence the exact
  founder-level target cannot be reached in descendant-only inheritance.
- `extinct`: no living plants; no I value, no manufactured zero allele.

Genetic loss `G` is the FIRST living census transitioning to
`alive_closed`. Extinction `E` is the first extinct census. Competing
first event is whichever occurs first. G can be followed by E; its
competing cumulative-incidence label is still G. E occurring before G
is not imputed genetic closure. With no mutation/immigration, the source
allele-support maximum never rises; past G cannot revert in descendants.

For each t, report all original-assignment denominators:

```
CIF_G(t) = P(first genetic G by t before E)
CIF_E(t) = P(first extinction E by t before G)
P_access_alive(t) = P(currently living with upper HIGH-I access)
P_alive_closed(t), P_extinct(t), P_alive(t)
CIF_G(t) + CIF_E(t) + P_access_alive(t) = 1
P_access_alive(t)+P_alive_closed(t)+P_extinct(t) = 1
```

Use initial policy contrast (evolving minus fixed) of CIF_G(tau) and
P_alive(tau) as candidate two co-primary targets, **subject to pre-outcome
scientific minimum effect (SESOI), alpha correction and the #585 power
gate**. Also display both policy curves, truncated mean time alive
AND genetically accessible, and t_G distribution *only with competing
extinction respected*. Do not use a conditional mean t_G among losses
as the A-policy causal effect. A process with more deaths can show fewer
G events even without conserving ancestral alleles.

`scripts/chapter2_assurance_access_competing_risks_20261018.py` is the
pure input/endpoint algebra and strict loss/extinction conservation
contract. Its synthetic tests are **NOT biological histories**. Neither
the source paper nor the original registered co-primary choices change.

## Functional tolerance and selection are separate state diagnostics

At an ORIGINAL occupied genotype state, use native source-reproductive
operators with identical plant population, matching, ovule budgets and
functional visitor treatments to measure:

1. `FT_maternal` = ratio of expected viable maternal seeds with zero
   effective outcross fertilization to idealized complete outcross
   fertilization for the SAME state. Under delayed selfing this is the
   OVULE-WEIGHTED `(1-delta)*A`. Costs affect absolute ovule numbers, so
   distinguish this ratio from absolute output and from persistence.
2. The sensitivity of expected maternal seeds to random success q,
   requiring a prespecified distribution of q; the source identity
   `Var(Y)=O^2[1-(1-delta)A]^2 Var(q)` assumes O,A fixed and is NOT a
   descendant viability / geometric population growth result.
3. With an externally specified fixed functional returning visitor
   assemblage (as opposed to just counting visitor types), compare
   expected pollen delivery, maternal outcross and paternal siring at
   the SAME plant genotype. A positive efficacy check is required before
   a return failure is assigned to plants.
4. Assay source-local signs `beta_I^return` and `beta_A^return` with
   full genetic maternal+paternal+selfing fitness. Analytic monomorphic
   gradients and actual finite polymorphic-population probes have
   different scopes and must not be substituted for each other. A
   zero beta_A under cost-free delayed selfing is neutrality, NOT proof
   of an irreversible A phenotype.

The cheap primary historical clock requires **NO simulated restored
descendants**. A SMALL, separately bounded calibration subset may
branch from saved genotypes with restored functional visitors versus
a prospectively defined matched sham. Same stream master seed per
environmental comparison, no environment-indexed demographic seed.
Common random numbers do not guarantee eventwise draw synchronization.
The calibration reports real finite-H conditional return and
unconditional survival; neither calibration nor an arbitrarily sparse
time grid proves t_star.

## Pooled inference and prospective precision: hard stop before biology

The PRE-OUTCOME design is not the legacy 8 synthetic historical paths,
the 144 nested futures or the already observed 2,304 source histories.
Independent founders and independent visitor histories must be sampled
with NEW disjoint SHA-identified source/seed namespaces. Both policy arms
are paired within F,V,repeat; demographic repeats remain nested.
Uncertainty must resample the two independent axes, retaining both
policies and all temporal states together. Do not treat F*V or future
streams as independent island systems. The founder-by-visitor interaction
and within-cell noise are not separable from the earlier 2x2 pilot
alone. Survivor-only analyses are descriptive, not primary causal policy
contrasts.

**Before execution, complete issue/merged PR #585's required contract:**
verified independent pilot SHA, new study ID, pilot stream namespace
different from the registration namespace, source non-overlap, two
independent source counts, founder/visitor/interaction baseline AND
adverse variances for both endpoint targets, independently justified
SESOIs, at least 80% joint directional sensitivity screening under
familywise alpha 0.05, all original case/update/resource ceilings,
and explicit science-method approval. #585's normal MDE is only
a scenario proxy, NOT exact power and NOT an execution authorization.
Until these fields are real and reviewed, **HOLD_NO_CONFIRMATORY_RUN**.

Candidate endpoint scientific relevance, time scale, cost, smallest
effects and block counts remain intentionally UNSPECIFIED rather than
inserting unsupported numbers. A future design can choose a bounded
pilot to estimate variance or abandon a costly and uninformative
confirmatory study. This plan must not be renamed into the
`chapter2_future_registered_*.json` auto-gated namespace before
independent pilot variance and all fields are genuinely available.

## Evidence status at drafting

Existing verified source-level counts: 1,455/2,304 archived HIGH-I
upper-support losses while occupied, 1,201/2,048 in four-visitor-present
static contexts; no positive-after-return beta_I or historical
evolvable-vs-fixed A assignment in that cohort. Separate 2x2 synthetic
historic pilot: one evolving-A t_G=39 after artificially imposed
T_E=35, 0/4 fixed-A closures by t45; this is not a causal clock
contrast. Historical original Q1 supports no A-evolution requirement
for I decline. Collective viable-seed versus focal total genetic
selection can differ in some source conditions, but population-wide
fitness optimum or evolved group harm remains unconfirmed.

The full science question is **functional reproductive robustness
without necessarily retained evolutionary reconfigurability**, not an
assumed universal insurance-versus-advertising trade-off. The data
must be permitted to support faster closure, slower closure, no change
or opposed survival/access responses.
