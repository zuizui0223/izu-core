# Island pollination ABM mechanism state — 2026-08-22

## Current scientific position

The empirical programme and the ABM now support a more specific question than a universal island syndrome:

> A pollinator-functional environment can shift in a broadly common direction, while plant lineages diverge in downstream response because they begin at different positions in functional trait space. Local ecological support and partner effectiveness can then reallocate or bias those response branches.

This is **not yet an empirically identified causal law**. The ABM identifies a minimal synthetic mechanism; the empirical programme shows recurrent heterogeneity and one independent starting-state pattern, but a direct signed plant-position × pollinator-environment × reproductive-response test is still missing.

## Falsification ladder

### v2 — lineage dependency / assurance heterogeneity

Adding lineage-specific pollinator dependency, reproductive assurance and trait-adjustment rates removed the structural requirement for a universal negative reproductive response, but positive responses were rare.

Decision: `lineage_heterogeneity_can_generate_sign_branching_but_v2_remains_strongly_decline_biased`.

Interpretation: dependency/assurance heterogeneity can permit branching but did not explain its breadth.

### v3 — partner service quality

Geography-independent partner quality in `[0.2, 1.8]` did not broaden the response distribution under the old many-partner accumulation rule.

Decision: `partner_service_quality_heterogeneity_alone_is_insufficient`.

### v4 — fixed visit budget

v4 removed the artificial rule that more pollinator types automatically imply more visitation. The same total visit opportunity is distributed across partner types.

Held-out Izu qualitative validation survived across the full retained saturation envelope:

- best-match decline is the majority outcome at every setting;
- positive and negative reproductive responses both occur;
- known Izu sign frequencies were not fitted.

Decision: `v4_survives_heldout_izu_at_qualitative_mechanism_level`.

### v5 — support-preserving local reweighting

Prospective Menorca validation failed badly: empirical local Shannon and plant-niche-overlap amplitude were far beyond the frozen v5 predictive envelope.

Interpretation: reweighting a fixed local partner support is insufficient.

### v8 — pair-support variation

v8 opened local pair support. Prospective Cabrera validation reproduced pair-set turnover but still produced local networks that were too dense and too weakly variable in weighted architecture.

Interpretation: pair support matters, but a missing upstream local plant/resource-opportunity layer remained.

### v9 — local plant opportunity before pair support

v9 added local plant/resource availability before pollinator/pair support. It has the required synthetic capability. The first new full-v9 candidate, Martinique, failed a source-measurement gate before targets: independent floral quadrats did not cover all interaction-observed plant endpoints at Site × Period scale. Martinique therefore neither confirms nor falsifies v9.

### v10 — effectiveness retested after structural corrections

v10 put partner effectiveness on top of v9 while keeping matched quality-OFF and quality-ON networks identical.

648 lineage contrasts:

- quality changed reproductive contrast magnitude in 501;
- quality caused 17 matched response-sign flips;
- positive responses were 151 OFF versus 150 ON;
- mixed-sign configurations were 18 OFF versus 18 ON.

Decision: `v10_partner_effectiveness_changes_branch_identity_without_broadening_positive_tail`.

Interpretation: effectiveness affects which lineage occupies which branch, but is not the missing generator of aggregate branching.

### v11 — downstream four-factor factorial

A 16-cell factorial tested local support, dependency heterogeneity, assurance responsiveness and partner effectiveness.

The decisive result was the all-four-OFF state:

- 157 positive / 131 negative contrasts across pooled runs;
- mixed-sign run fraction 0.417;
- two-sided branching remained.

Local support strongly reallocated branch identity and shifted the response distribution negative, but downstream dependency heterogeneity produced zero matched sign changes.

Decision: `two_sided_branching_persists_with_all_four_tested_downstream_factors_off`.

Interpretation: the generator of lineage branching was already upstream of those four downstream modifiers.

### v12 — residual upstream lineage factors

v12 then froze those four downstream modifiers OFF and prospectively tested the remaining lineage attributes:

1. initial trait-position heterogeneity;
2. trait-adjustment-rate heterogeneity;
3. assurance-ceiling heterogeneity.

The v12 all-ON residual state exactly reproduced the frozen v11 residual counts.

Only one drop-one ablation collapsed same-run lineage branching:

- **initial trait heterogeneity OFF:** mixed-sign run fraction `0.4167 -> 0`; mean within-run branching balance `0.2569 -> 0`;
- trait-adjustment heterogeneity OFF: no aggregate branching loss;
- assurance-ceiling heterogeneity OFF: no branching loss.

When all three residual factors were OFF, pooled stochastic runs still contained both positive and negative contrasts, but every lineage inside a given matched run responded identically. This separates between-run environmental stochasticity from within-environment lineage branching.

Decision: `v12_residual_lineage_factors_exhaust_within_run_branching_in_declared_model`.

## Minimal synthetic mechanism now supported

```text
common pollinator-environment shift
          ×
pre-existing lineage position in functional matching-trait space
          ↓
lineage-specific opportunity / service change
          ↓
reproductive response branch
```

Then:

```text
local plant/pollinator/pair support
+ partner effectiveness
```

can shift branch identity and directional bias without being necessary to create the underlying two-sided branching.

## What changed scientifically

The previous working explanation gave reproductive dependency a central role as the likely branch generator. The current ABM does **not** support that strong reading. Downstream dependency heterogeneity is unnecessary for branch generation conditional on the frozen upstream state.

The better working hypothesis is now:

> **State-dependent response hypothesis:** island pollinator-functional change does not impose one plant response. Its effect depends first on where a lineage already lies in the relevant plant–pollinator functional trait space. Dependency, assurance, local ecological opportunity and partner effectiveness can modify magnitude or branch allocation after that initial state dependence.

Dependency remains biologically important and Issue #91 remains necessary for direct service/dependency calibration. It is simply no longer justified as the primary synthetic explanation for response-sign heterogeneity.

## Independent empirical consistency already present

The Southwest Pacific flower-size analysis predates v12. Among 88 source-coded animal-pollinated mainland–island pairs:

- `LR = log10(FI/FM)` versus `log10(FM)` slope = `-0.150995`;
- island-cluster 95% CI = `[-0.30406, -0.07252]`;
- family-cluster 95% CI = `[-0.24834, -0.02076]`;
- leave-one-island slopes are all negative.

This is independently consistent with **starting state influencing island response shape**. It is not a direct validation of the pollinator-matching mechanism. The response algebraically shares the mainland measurement with the predictor, and the source does not identify mainland-size reliability; under the declared classical-error sensitivity, the cluster interval remains wholly negative only if reliability exceeds about `0.926`.

## Why Izu cannot yet directly confirm v12

The ideal focal empirical variable is a **signed** plant position relative to the pollinator functional environment, for example:

```text
plant tube length (mm) - source-native pollinator functional center (mm)
```

Izu has source-native species × site tube means in millimetres. However:

- numeric pollinator proboscis values are still unrecovered: `0/209` current named taxa;
- the public 2024 archive does not expose a source-native quantitative plant × pollinator pair table sufficient to reconstruct a plant-specific signed partner center;
- `TM_sp_z` is available but is an alignment/matching metric, not a signed position around the functional optimum.

Therefore the preferred signed-position test remains blocked rather than being filled with guild midpoints or taxonomic proxies.

## Current proof ladder

| Claim | Current status |
|---|---|
| Island plant responses are not universally directional | empirical support across independent systems |
| Common-ish upstream functional/matching constraint can coexist with downstream response branching | empirical Izu pattern + held-out qualitative v4 support |
| Pre-existing trait-position heterogeneity can generate same-environment lineage sign branching | identified as the minimal source inside the declared ABM |
| Local support changes branch allocation / directional bias | strong synthetic ablation result |
| Partner effectiveness can change individual branch identity | synthetic matched-ablation support |
| Reproductive dependency is the primary generator of sign branching | **not supported by current ABM** |
| Signed plant position relative to pollinator functional optimum causes real island response branching | **not yet empirically identified** |

## Next decisive evidence

Do not add another generic ABM layer now.

The next high-value step is an empirical test with compatible units:

1. plant matching trait measured before or at the baseline regime;
2. pollinator functional trait/environment on the same scale;
3. a predeclared signed plant-position metric;
4. downstream effective-service or reproductive response;
5. at least one independent island system not used to choose the mapping.

The mapping must be frozen before its downstream outcome is inspected. Izu can serve as the focal direct test only after the missing pollinator-trait/weight information is recovered; otherwise the search should move to a new independent system rather than weakening the construct.
