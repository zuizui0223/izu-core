# Model3 K32: Which visitor features accompany matching-direction reversal?

## Current scientific location

The original Model3 K32 old-history expected matching-high allele direction was
negative early and positive late in one archived visitor history 26110601.
After recognizing the result, eight newly generated visitor RNG histories
26110602..26110609 were evaluated. Four of eight (budget8) or five of eight
(budget3) exhibited the same strict negative-to-positive reversal, while
other histories did not. These are POST-OUTCOME exploratory source simulator
histories, not natural island populations or preregistered confirmation.

This analysis uses those eight original simulated histories **as they stand**
rather than choosing more seeds after seeing which histories switch.

## Biologically grounded descriptors

The source reproducer uses visitor-specific Gaussian matching affinity
exp(-((matching_trait - optimum)/breadth)^2), combined with flower
investment, visitor effectiveness, donor export, donor/recipient competition,
and maternal seed allocation.

We calculate a deliberately limited *visitor-only* proxy at matching
trait 0.25 and 0.75, with no fictitious individual plant observations:

    service(m) = mean_visitor(effectiveness *
                   exp(-((m - optimum)/breadth)^2))

    preference = service(0.75) - service(0.25).

If no visitor types are present, service is defined as zero, and
functional visitor richness is zero. This descriptor is **not**
canonical whole-population reproductive success, pollen delivery,
female fecundity, or a causal selection gradient.

For each of the eight visitor years, report functional richness,
mean optima/effectiveness, matching affinity at low and high
phenotypes, and their difference.

The two **a priori fixed features within this follow-up** for
year8 prediction are the FIRST TWO years' mean matching
preference contrast and mean functional visitor richness.
These have no source year3..8 look-ahead. Separately record
full-eight-year average preference/richness, and late-minus-early
changes, but classify them RETROSPECTIVE descriptors only:
they are prohibited from entering the early-year forecast.

## Entire-history held-out prediction, no leakage

For each budget independently, use only the eight NEW history seeds.
The old source discovery seed 26110601 is excluded from both
fitting and scoring.

For every history h:
1. Train on the OTHER SEVEN visitor histories.
2. Standardize each feature using the TRAINING SEVEN means
   and standard deviations only.
3. Fit a deterministic two-feature, intercept-unpenalized ridge
   regression with **fixed lambda=2**, no outcome-driven tuning.
4. Predict history h's exact source-model matching-high expected
   one-generation allele direction at start of reproductive year8,
   conditional on its same-history original source survivors.
5. Compare continuous mean-square prediction error and sign
   accuracy to a training-only mean/intercept predictor, the
   training-only majority sign, and naive persistence of
   the first-year source matching expected-direction sign.

Test splits are by VISITOR RNG history, not by the 128
demographic source paths within the same history.
Budget8 and budget3 share the EXACT same eight visitor
RNG history seeds and are thus not sixteen independent
environmental replicates.

This is an n=8 **post-selection sensitivity audit**.
A low or high predictive accuracy on eight histories
cannot license a general ecological forecasting model,
a p-value, feature selection, or Nature-level biological
claim. The simple ridge model is only a predeclared
competitor to a trivial baseline. If it performs worse
than the baseline, record that negative result.

## Descriptive environmental associations

Pearson correlation between year8 expected matching direction
and each of the full list of visitor descriptors is reported
for transparency, **without using the correlations for
predictor selection**. A future ecological feature is not
allowed into the first-two-year prediction. The fixed 8
different simulator-generated visitor histories are too
few to distinguish stochastic association from response
to evolving genotype/census states.

No new visitor simulations beyond the existing
26110602..26110609, no prospective frozen Chapter2
histories 37110801..37110864, no natural island sites
and no mutation/survival/immigration or original
source reproduction edits.

## Commands and CI evidence scope

    pytest -q tests/test_model3_k32_visitor_environment_predictors.py
    python -m scripts.audit_model3_k32_visitor_environment_predictors \
      --budget8 exploratory-histories-budget8.json \
      --budget3 exploratory-histories-budget3.json \
      --out exploratory-visitor-environment-prediction.json

The PR420-only CI job model3-k32-new-visitor-history-stress
regenerates exact original source histories, tests feature
source/chronology leakage, and archives the FULL per-history
outcomes plus the new visitor signature/prediction report.
NUMERICAL claims must wait for a successful source-linked
CI run and raw artifact inspection. The PR remains Draft.


## Executed source-locked results

The test suite and actual source-run ecological predictor
[GitHub Actions 37952017304](https://github.com/zuizui0223/izu-core/actions/runs/37952017304),
job `model3-k32-new-visitor-history-stress`, **PASSED**
on SHA `b744edbcb3abc1f1d40e9c3d21b35dbf6a426cce`.
The [full archived source histories and ecological predictor report
artifact 11626158325](https://github.com/zuizui0223/izu-core/actions/runs/37952017304/artifacts/11626158325)
has SHA256
`72f5313267de32de814e92c9c04a05121717b37e9ef0bc754cf4f3256fbb474f`.
The artifact contains BOTH 8-year visitor-history original
source genetic-dynamics JSONs (budgets 8 and3) and
`exploratory-visitor-environment-prediction.json`.
The compact committed evidence is
`data/results/model3_k32_visitor_environment_prediction_20261010.json`.

### Early visitor information does not improve held-out forecast

The forecast was trained on seven **different visitor
RNG histories** and predicted the eighth. This was
repeated eight times for each budget; the reference seed
26110601 was excluded from fitting and scoring.

| Year8 source matching-high expected allele direction | Budget8 | Budget3 |
|---|---:|---:|
| New history groups in leave-one-out evaluation | 8 | 8 |
| First-2-year visitor affinity/richness ridge sign accuracy | 5/8 | 6/8 |
| Training-only majority sign accuracy | **5/8** | **6/8** |
| Year1 allele expected-direction sign persistence accuracy | 3/8 | 2/8 |
| Ridge continuous held-out MSE | 0.000064006 | 0.000031267 |
| **Training-only intercept held-out MSE** | **0.000053662** | **0.000021051** |

The fixed 2-feature ridge DOES NOT outperform the
training-only source-history intercept baseline:
sign accuracy is identical but the continuous
held-out MSE is GREATER in both resource regimes.
This is a valuable negative check against premature
forecasting from a few intuitive visitor descriptors.
The one-year expected matching allele direction
also performs poorly as a simple persistence
forecast of the late direction.

### Descriptive temporal associations, NOT early forecasts

| Pearson r with observed source year8 matching expected direction across eight new histories | Budget8 | Budget3 |
|---|---:|---:|
| First-two-year high-minus-low effective affinity | +0.351 | −0.119 |
| First-two-year functional visitor richness | −0.268 | −0.566 |
| Eight-year mean high-minus-low effective affinity | +0.539 | +0.090 |
| **Late-two-years minus early-two-years matching effective-affinity contrast** | **+0.540** | **+0.782** |
| Eight-year mean visitor richness | −0.122 | −0.096 |
| Late minus early visitor richness | −0.245 | −0.163 |

The higher retrospective association with CHANGING
matching preference under budget3 suggests a
hypothesis worth testing in a genuinely independent
study. But it is calculated using the FULL visitor
trajectory, including future conditions, and therefore
cannot support an early-year forecast. The budget3
association is higher than budget8 despite the SAME
eight ecological RNG seed histories, illustrating
genotype/census-dependent model responses. There
are only eight distinct synthetic visitor histories,
and multiple descriptive descriptors were examined
AFTER earlier outcomes, so do not attach uncorrected
significance claims to these correlations.

Source examples: history 26110606 has first-two-year
high-minus-low matching effective affinity about +0.564,
but its final-versus-initial preference contrast is
approximately −0.597, and source matching-high
expected direction in year8 is negative under both
budgets (about −0.00103 and −0.00399). Conversely
seed 26110603 has early effective preference
about −0.087 and late-minus-early preference
about +0.273, with positive year8 source
matching expected directions about +0.01387
and +0.00829. These are *examples of ecological
co-occurrence*, NOT isolated visitor causal
effects because parental genotype histories also
differ across simulation seeds.

### Consequences for the scientific claim

- The original source genetic mechanism, with exact
  selfed-seed × inherited HIGH allele weighting,
  **does not yield a robust visitor-only early predictor
  of matching allele evolutionary direction** from
  the fixed two descriptors used here.
- Time-varying visitor matching conditions MAY matter,
  consistent with prior 8×8 parent-state × visitor
  transplantation. But the present ecological
  correlation cannot distinguish environment change
  from endogenous parental genotype/census changes.
- The main value of this stage is narrowing what
  CANNOT yet be predicted using ecological variables
  alone, not a new predictor validated across natural
  archipelagos.
- The eight ecology RNG histories were selected
  after the first discovery and represent a single
  generator, 128 nested demographic source paths
  per visitor history, shared across both budgets.
- The frozen prospective Chapter2 history cohorts
  remain unused. The original source biology was
  not modified; no natural pollinator experiments,
  independent island systems or SDE/SPDE validation
  were produced.
