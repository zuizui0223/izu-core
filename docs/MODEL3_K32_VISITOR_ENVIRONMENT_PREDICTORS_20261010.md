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
