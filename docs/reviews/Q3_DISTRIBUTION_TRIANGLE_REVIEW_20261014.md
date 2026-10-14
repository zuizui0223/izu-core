# Review: three-policy distribution triangle

Scope: prospective scientific design only. No new futures, raw outcome extraction, simulation, replay or random draws were executed. The published protocol is not modified by this review.

## Verdict and minimality

The proposed triangle is a valid, minimal three-policy design for obtaining BOTH (1) a nondegenerate comparison holding the exact allele support set fixed and (2) a nondegenerate comparison holding allele variance fixed while changing its range, with a common reference and interior mass in every policy. It improves the interpretation of the former family by keeping the centre allele present in the exact-support comparison.

This minimality is conditional on those two contrast requirements. It is not a proof that three new policies are necessary for any scientific improvement over the original experiment. One or two new policies could address a narrower question. Two distinct policies alone cannot provide both requested nondegenerate comparisons: their support widths would have to be both equal (first comparison) and different (second comparison). The existing q=1 restored arm cannot substitute for an arm in the exact-three-point-support comparison because it has no centre mass; the native q=0 arm has only centre mass. Thus, under the stated requirements, all three proposed policies are new and no new native reference is necessary.

## Exact distributions

At N=48, assign H=qN individuals genotype [v-w,v+w] and the remaining individuals [v,v]. The empirical allele probabilities are q/2 at each endpoint and 1-q at v. Every individual's expressed investment is v at intervention; the allele mean is v and population allele variance is qw^2.

| Policy | w | q | H | Lower probability | Centre probability | Upper probability | V |
|---|---|---|---|---|---|---|---|
| A | 1/16 | 1/2 | 24 | 1/4 | 1/2 | 1/4 | 1/512 |
| B | 1/16 | 1/4 | 12 | 1/8 | 3/4 | 1/8 | 1/1024 |
| C | 1/8 | 1/16 | 3 | 1/32 | 15/16 | 1/32 | 1/1024 |

All policies have three occupied support points. A and B have the SAME exact support set {v-1/16,v,v+1/16}; C has a different, wider three-point support set {v-1/8,v,v+1/8}. Equal support cardinality is not equal support set. The full endpoint range is 2w; w is its half-width.

For the stated domain [0,1] and stated v values 0.375, 0.5 and 0.625, both widths are feasible without boundary clipping. This is an algebraic check of the supplied values, not independent validation of recorded input states. Actual state admission must still check the frozen source, population size, allele values and counts before execution.

## Effect definitions and claim limits

For a fixed admitted state i and a prespecified outcome Y, define mu_i(P) as the expected outcome under policy P, averaging over the prespecified carrier-allocation distribution and future stochastic dynamics. Then use two directed contrasts:

- mu_i(A)-mu_i(B): the effect of increasing endpoint mass/heterozygosity and doubling allele variance under the SAME exact support set.
- mu_i(C)-mu_i(B): the effect of widening the endpoint range at the SAME allele variance, with reduced endpoint mass and heterozygosity.

Neither contrast isolates a unique abstract variance or support effect. The assignment changes a whole genotype-distribution policy. In A versus B, carrier count, centre mass, allele frequencies, fourth moment and potential associations with other state features change along with variance. In C versus B, the range, carrier count, centre mass, allele frequencies and higher moments change despite matched variance. For this family the standardized fourth moment is 1/q, equal to 2, 4 and 16 in A, B and C. Keeping an interior allele present removes a binary support-presence difference but does not keep its frequency or its future persistence fixed.

A fixed-state randomized intervention can identify these policy effects without calling carrier allocation a conventional observational confounder. However, carrier identity and its correlations with other loci, location or reproductive state remain parts of the implemented intervention. If the intention is to generalize over those identities, the allocation distribution belongs in the estimand and must be sampled accordingly. A single allocation followed by many dynamic futures estimates an allocation-conditional effect, not the allocation-averaged effect merely because that allocation was initially randomized.

Across states, prespecify the state weights and whether the target is triggered states or an original-slot policy contrast with zero difference at non-trigger slots. Keep blocks separate. Each outcome and effect scale needs its own definition; an event-probability difference and a terminal-mean difference are different effects. Any survival-conditioned terminal estimand must retain its explicit conditioning and cannot be read as an unconditional population effect.

## Nested carrier allocation

A uniform random permutation of the 48 original individual identities can define A from its first 24 identities, B from its first 12 and C from its first 3. Each marginal subset is then uniform at its required size; nesting provides a reproducible coupling across policies. Generate the permutation with a separately specified allocation stream independent of dynamic streams, and freeze how that stream varies across states and paired futures.

Nesting does not hold allocation constant, since carrier counts differ. It also does not guarantee reduced variance or identify a separate carrier-count effect. Preserve the remainder of each individual's state and fix the assignment of allele copies to homologues according to the model's genotype convention; if chromosome phase or linked inheritance is meaningful, its handling must be part of the policy definition. Coupling dynamic streams across arms is an estimation choice and does not remove biological differences in how arms consume or respond to random draws.

## Tradeoff against a matched four-cell design

An appropriate fourth policy D is w=1/8, q=1/8, V=1/512, with 6 heterozygotes. It retains all three support points. Together A/B/C/D form a complete 2 by 2 width-by-variance policy table, unlike a design whose q=1 cell loses its centre point.

On an additive outcome scale, the interaction contrast is (mu(D)-mu(C))-(mu(A)-mu(B)). It measures whether the specified variance-policy contrast differs between the two widths. Its interpretation remains a distribution-policy interaction, not a pure interaction of abstract support and variance mechanisms. Other outcome scales define other interactions and must be fixed in advance.

The triangle supplies the two local comparisons at B but cannot estimate this four-cell interaction or determine whether its conclusions extend to the missing wide/high-variance cell without further assumptions. The fourth cell adds one policy, or one third more new-arm futures at equal allocation, and buys that interaction plus both directions of replication across the factorial table. If the scientific question needs only the two B-anchored contrasts, the triangle is sufficient and cheaper. If it asks whether a range effect depends on variance, or a variance-policy effect depends on width, use the four-cell design.

No new native arm is required to identify the two within-triangle contrasts. Omitting it means the new experiment directly estimates no contemporaneously paired native-versus-triangle contrast. Existing native/restored results remain useful context, but reusing them as a controlled reference requires an explicit compatibility and coupling contract.

## Recommendation

Use the triangle as the smallest design for the two expressly stated local questions, and label its effects by their complete policies. Freeze carrier-allocation averaging, state weights, outcome scales and endpoints before execution. Retain the fourth-cell option only if interaction or cross-width generalization is part of the actual question. This review authorizes no execution and establishes no empirical effect direction.
