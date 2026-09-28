# Ecology Letters cover letter — V0.4

**Status:** scientific draft; author metadata, archive DOI and submission declarations remain to be completed.

Dear Editors,

Please consider our Letter, **“Effective independence is a second-order coordinate, not a nonlinear ecological state,”** for publication in *Ecology Letters*.

Ecologists routinely replace structured systems by scalar equivalents. This is useful when the property being matched is explicit: effective population size matches a specified drift or inbreeding process, effective species numbers match a diversity value, and synchrony corrections can match aggregate variance. Our Letter asks what happens when a variance-equivalent effective number is promoted from a variance summary to a descriptor of a nonlinear ecological response.

We derive a sharp boundary. In a bilinear state–community model, aggregation and synchrony collapse exactly onto `k_eff`, and community (`C`) and state-by-community (`I`) variance share the same multiplier. For a smooth nonlinear response, however, equal `k_eff` fixes the second cumulant but not higher cumulants. A common-factor construction gives explicit third- and fourth-cumulant terms along an exactly constant-variance contour. More importantly for the response decomposition, an exact quadratic mixed-response expansion gives

`C = b^2 tau + b d mu3 + (d^2/4) Var(Z^2)`

and

`I = Var(X)[c^2 tau + c e mu3 + (e^2/4) Var(Z^2)]`.

At fixed variance and symmetric source noise, higher moments change `I/C` unless the pure and mixed response curvatures satisfy the restrictive alignment `e^2 b^2=c^2 d^2`. The contribution is therefore not only a counterexample: it identifies the order at which variance-equivalent sufficiency breaks and a response-level condition for when that missing information changes ecological determinant order.

We then test the mechanism in two nonlinear ecological response classes. A frozen plant–pollinator model crosses the bilinear `C/I` boundary as community trajectories are pooled. A structurally separate adaptive consumer–resource model reproduces that phase across a broad parameter grid. We deliberately retain a failed prediction: before opening the setting-level grid, we predicted that stronger Holling-II fourth-order curvature would increase reversals. It did not. Reversal counts declined from 41 to 38 to 32 across handling values 1, 2 and 4. This falsification redirected the mechanism from scalar curvature to mixed state–community geometry.

We then froze a revised intervention before running six previously unused seeds. Across all 18 combinations of resource count, matching width and handling, feedback knockout (`alpha=0`) produced 0 `C/I` reversals in 108 block-by-seed comparisons, whereas active state adjustment (`alpha=0.15`) produced 52. Every discordant pair was in the predicted direction. The intervention revealed that feedback does not merely amplify interaction variance: it creates a community-dominated low-aggregation regime that subsequently crosses into interaction dominance. This fresh validation turns a post-hoc pattern into a tested phase-shaping mechanism.

We also distinguish two routes by which equal variance-equivalent independence can fail. A clone-mixture construction changes discrete trajectory support along an exact equal-`k_eff` contour. A separate shared-event construction preserves independent partner identities yet still produces different response decompositions at similar variance-equivalent `k_eff`. We therefore treat support non-equivalence and higher-order distributional non-equivalence as distinct mechanisms rather than merging them into one explanation.

### Novelty relative to related work

The manuscript does not claim that synchrony effects, Jensen's inequality or effective-number constructions are new. Keitt et al. showed that spatial synchrony changes the effective number of fluctuating subpopulations; Ruel & Ayres formalized the relevance of nonlinear averaging; and recent work has linked aggregation, dispersal, synchrony and stability. Our contribution starts after those facts: **we identify the mathematical order and mixed-response condition under which a second-moment effective number ceases to be sufficient for ecological response, then test a derived mechanism with a fresh intervention.**

### Companion manuscript and overlap disclosure

A separate companion manuscript from the same repository, currently routed to *Oikos*, is titled **“Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching.”** That paper uses the frozen plant–pollinator model to address a different ecological question: how realized richness, composition and starting state partition heterogeneous responses to pollinator-community reorganization, including a six-seed `k={1,2,4,8,16}` scaling result. The present Letter reuses that frozen model and scaling output as one motivating nonlinear system; those shared quantities are not claimed as new here.

The new material in this Letter is the variance-equivalent sufficiency question and its analytical treatment, including the higher-cumulant common-factor derivation, the exact quadratic mixed-response condition, the separate adaptive consumer–resource model, the prespecified failed scalar-curvature test, the fresh-seed feedback intervention, and the exact/identity-preserving equal-`k_eff` challenges. The *Oikos* manuscript does not make the `k_eff` sufficiency claim, does not contain the higher-order theorem or mixed-curvature condition, and does not use the consumer–resource or equal-`k_eff` analyses as its inference. We will disclose the companion manuscript in the submission system and provide it to the editors if requested. We will not submit the two manuscripts in a way that obscures their shared model provenance.

All code, frozen design objects, negative and positive prediction receipts, and machine-readable results are maintained in `izu-core`. A permanent public archive DOI will be inserted before submission.

Sincerely,

[Corresponding author name]  
[Affiliation]  
[Postal address]  
[Email]  
[Telephone / fax if required]

## Author declarations to complete before submission

- [ ] Lane A / *Oikos* manuscript has been submitted first, or its exact status is disclosed to the *Ecology Letters* editors.
- [ ] Companion manuscript is uploaded or supplied if requested by the journal.
- [ ] All authors have approved submission and authorship order.
- [ ] The manuscript is not under consideration elsewhere in a way that violates either journal's policy.
- [ ] Conflict-of-interest statement confirmed.
- [ ] Funding statement confirmed.
- [ ] Authorship contribution statement completed.
- [ ] Corresponding-author full contact details completed.
- [ ] Public data/code archive created and DOI inserted in manuscript and cover letter.
- [ ] Recommended and opposed reviewers / editorial board members supplied with conflict reasons where applicable.
