# Q3 joint method-review candidate: genetic access and demographic rescue

**18 October 2026 — proposed method-review package, NOT a registered or started confirmation.**
Single paper: PR #590. Source branch: PR #597, commit
`98a0f2de98a6572bc4789c0431f44c45f283400e`. Old model operators, pilots,
registered Q1–Q4 decisions and the two descendant stream families are unchanged.

## What is now specified

The two co-primary targets are separate, unconditional population-level contrasts:

1. **Genetic access (G):** evolving-minus-fixed A difference in cumulative
   incidence of FIRST loss of the allele range needed for each population's
   own founder-mean I, while alive and before extinction, through census80 in
   the B=8 no-visitor control branch. Death before genetic closure is competing
   extinction, never zero-valued I or a discarded row.
2. **Demographic rescue (S):** the historical A-policy by budget interaction,
   `[P(alive80|E,B4.5)-P(alive80|F,B4.5)]
    -[P(alive80|E,B8)-P(alive80|F,B8)]`.
   All originally allocated populations count, including deaths before the fork.

A nominal **0.10 absolute effect** is proposed for BOTH design margins. It means
one additional initially allocated population per ten changes outcome, or one
net additional survivor per ten in the interaction. This is a transparent,
normative study-resolution choice, not an effect inferred from favorable
pilot results, not a natural-island conservation threshold, and NOT independently
approved. A methods reviewer must endorse or revise it BEFORE registration.
The old 22.22-point result is not the margin, and statistical significance is
not equivalent to demonstrating an effect of at least ten points.

## Use the variance of the outcome actually planned

The future G endpoint is a B8 branch after the common t35 history. Accordingly,
its variance assessment must not rely only on the original uninterrupted pilot.
Three related source checks are retained separately: the original equal-A pilot,
and the already executed B8 continuations in stream90 and stream104. They share
six founder and six visitor levels and are NOT independent added cohorts.

| Paired genetic-loss differences | Founder | Visitor | Interaction | Within-cell noise |
|---|---:|---:|---:|---:|
| Original pilot | .0233333 | 0 | .0655556 | .2777778 |
| B8 continuation, stream90 | 0 | .0333333 | .0083333 | .4305556 |
| B8 continuation, stream104 | .0283333 | .0227778 | 0 | .5138889 |
| Componentwise envelope | **.0283333** | **.0333333** | **.0655556** | **.5138889** |

The old stress assumption of .40 for within-cell noise is SMALLER than the
measured .5138889 in a relevant control branch; it is not adverse for this
particular component. The proposed sensitivity scenario is therefore
**(.05 founder, .05 visitor, .20 interaction, .65 within-cell)**. These values
exceed all recorded component estimates and are explicit conservative stress
assumptions, NOT estimated population-variance upper confidence limits.
Truncated zero estimates do not prove zero true visitor/founder heterogeneity.
For S, baseline components use the envelope of BOTH stream-family estimates,
not whichever stream yields an easier power result.

## Independent backgrounds rather than repeated copies of the same background

For R nested demographic repetitions and F,V independent source counts, the
unchanged #585 proxy uses

```
SE² = variance_F/F + variance_V/V
      + (variance_FxV + variance_demographic/R)/(F*V).
```

At the ten-point margin under the proposed stress, equal-axis candidates are:

| Repeats per F×V cell | Smallest square F=V passing the proxy | Round-up to batches of 8 | Unique updates with a shared prefix |
|---|---:|---:|---:|
| 1 | 133 | **136** | **4,624,000** |
| 2 | 130 | 136 | 9,248,000 |
| 4 | 128 | 128 | 16,384,000 |

**Proposed candidate: F=V=136, R=1.** The pilot had R=2 to estimate interactions
and within-cell variation separately. The new candidate spends its budget on
independent source levels instead. Its final data cannot separately estimate
interaction and demographic noise, but their COMBINED contribution remains
relevant for inference on the mean paired-policy contrast. This is a comparison
of prespecified equal-axis alternatives, not a proof of a globally optimal design.

At 136×136×1, the normal screening MDEs are:

| Endpoint | Source-envelope baseline | Proposed adverse scenario |
|---|---:|---:|
| G: genetic-loss difference | 7.76 percentage points | 9.85 points |
| S: rescue interaction | 1.61 percentage points | 9.85 points |

With exactly known normal variances, the calculation gives a union-bound joint
correct-direction probability >=.81855 at true effects .10 for both outcomes.
That is ONLY an algebraic check of the approximation: it does not establish
Model3 power, actual confidence coverage, robustness of estimated variances, or
behavior of near-boundary binary outcomes. No simulated biological data were
created for this calculation.

## Complete history/fork budget, without disguising repeats as environments

There are two historical A policies and two future B arms, with ONE demographic
realization per F×V×policy. Every t0 plant has A expression exactly .5 in both
policies, but segregating A alleles remain. I/A/M mutation, seed immigration
and adult survival remain off. The original source K=48, direct assurance cost
.5, delayed selfing and six-to-one-to-zero visitor history are retained.
At t35, clone ALL histories into B8 and B4.5 and follow 45 updates to t80.
No actual pollinator-return descendant branch is included in these primary tests.

- 18,496 independent-axis crossings (not 18,496 independently drawn islands).
- 36,992 policy-specific common histories ×35 = 1,294,720 prefix updates.
- 73,984 terminal branches ×45 = 3,329,280 future updates.
- **Unique shared-prefix computational ceiling: 4,624,000 updates.**
- Existing #585 rectangular ceiling: 73,984 full paths ×80 = 5,918,720 updates.
  This deliberately double-counts the common prefix and is a conservative budget,
  NOT a claim that duplicate prefixes will be independently simulated.

The old #585 validator is unchanged. It accepts the rectangular layout with
ONE demographic replicate; a separate exact prefix/fork budget is audited.
No repeat was relabeled as an independent environment to satisfy its schema.

Reserved candidate founder seeds 401001..401136 and visitor seeds
402001..402136 do not overlap the named pilot cohorts. Demographic master keys
use the distinct study namespace and 128-bit hashes of stage/F/V, omitting
policy and budget to retain pairing. The 36,992 reserved stage keys have no
collisions. No biological stream has been consumed and no new founder population
has been sampled. Matching generator identities is not eventwise coupling.

## Prospective interpretation rules

Two two-sided 97.5% marginal intervals are intended, with Bonferroni familywise
alpha .05. The final interval procedure and its operating characteristics must
be reviewed; no exact coverage is claimed for an unvalidated bootstrap.

- Both lower bounds >0: evidence for the two POSITIVE directions under this model.
- Both lower bounds >.10: additionally demonstrate that both effects exceed the
  chosen minimum margin. The present power target concerns detecting direction
  at a true .10 effect; it does NOT provide 80% power to prove the effect exceeds .10.
- A negative G interval with positive S would instead support more survival and
  less closure, not the proposed positive-closure combination.
- Intervals crossing zero mean unresolved direction. Only intervals contained
  in the prespecified [-.10,+.10] equivalence band support small effects under
  that resolution. Lack of significance is not equivalence.

Even joint-positive results would not establish genetic mediation, a social
optimum, naturally evolved island syndromes, or the stochastic post-return
flower-recovery time t*. Necessary inherited allele access is not actual
recovery. These are strict claim limits, not optional discussion qualifications.

## Gate and evidence status

The unchanged source-pinned #585 evaluator returns
**GO_FOR_METHOD_REVIEW_NOT_EXECUTION** for both endpoints under both scenarios.
The scientific status is still
**HOLD_PENDING_INDEPENDENT_METHOD_AND_OPERATING_CHARACTERISTIC_REVIEW**.
The JSON remains outside `chapter2_future_registered_*.json`; no new study is
registered or authorized, and no Model3 evolutionary histories were started.

The remaining review is substantive: endorse the normative effect margins,
assess whether stress components cover plausible uncertainty, validate the
final bounded-outcome/two-axis confidence procedure and planned stopping rules,
and approve the implementation, archive location and actual resource allocation.
Do not interpret a machine-checkable numerical PASS as approval of those choices.

## Reproduce

```
python -m scripts.review_chapter2_joint_method_plan_20261018 --out-dir NEW_DIRECTORY
pytest -q tests/test_q3_joint_method_review_20261018.py
```

Nine new tests cover source counts, variance envelopes, invalid extinct controls,
#585 pass/fail, exact branch budgets, disjoint source proposals, unsupported
execution flags, significance-versus-equivalence semantics and normal-proxy scope.
The validator copy used locally has the exact Git blob
`099e6f7fb4bac354cf9e49de0afc3783fcb05346` from the live repository; no gate logic
was changed. The two data inputs likewise match their retrieved Git blob IDs.
