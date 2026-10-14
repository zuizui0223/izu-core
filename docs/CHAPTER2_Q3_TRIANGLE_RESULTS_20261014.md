# Q3 distribution policies: a main-block event effect, without replicated direction

The approved 26,352-path experiment completed, including native replay of every path and external readback of all raw archives. At the same three-point allele support, increasing the heterozygous carrier fraction from 1/4 to 1/2 increased the historical threshold-event probability in the main fixed-state block: A minus B = 0.05772569, simultaneous conditional 95% interval [0.00847761, 0.10697378]. The confirmation interval crosses zero. No directional contrast is resolved in the same direction in both blocks. All terminal-mean directions remain unresolved.

Thus support alone does not determine the event probability in the main block: two policies with identical support produced a resolved event contrast. This identifies the effect of the complete carrier-distribution assignment under the frozen conditional target. It does not identify a unique abstract variance component, a fixation-prevention effect, or a natural-history cause. The original 64-pair primary and the old PR #514 confirmation 0.01 question remain unchanged and unresolved.

## Frozen comparison and evidence

The [prospective design](CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md) fixes two B-anchored contrasts, two endpoints, and two blocks. The [continuation contract](CHAPTER2_Q3_TRIANGLE_CONTINUATION_20261014.md) changes admission/accounting after the preserved zero-science technical HOLD; it does not change scientific seeds, policies or estimands.

| Policy | Half-width w | Carrier fraction q | Heterozygous individuals / 48 | Allele variance q w² |
|---|---:|---:|---:|---:|
| A | 1/16 | 1/2 | 24 | 1/512 |
| B | 1/16 | 1/4 | 12 | 1/1024 |
| C | 1/8 | 1/16 | 3 | 1/1024 |

Carriers have alleles [v-w,v+w]; other individuals have [v,v]. Every individual's initial expressed I remains v. A/B hold the exact support set fixed; B/C hold allele variance fixed. Other genotype-distribution properties change. Fresh nested allocation is drawn for each state/triplet, followed by the frozen coupled dynamic streams. There are 144 triplets at each of 61 trigger states and three non-trigger zero-policy slots, retaining 32 original slots per block.

The estimand is allocation-and-dynamics averaged, fixed-state, and conditional on all three coupled arms surviving to census 200. All 8,784 observed triplets passed that gate. This observation does not establish survival probability one or change the target into an unconditional population effect. Futures are not new independent founder populations.

- Reviewed source: `47bdc41aadb1eb27262b2b54f852db68bfed90aa`.
- Approved activation: `3519e8704420bd3b7ce378e5678efb61bf66da50`; activation SHA256 `ef075456e80c4adf132816523519bb210c4ffba69029cf4bd4b6f6aa6611aea9`.
- [Completed run 38533099249](https://github.com/zuizui0223/izu-core/actions/runs/38533099249): all 18 shards and final verification/publication job succeeded, attempt 1.
- [Published release](https://github.com/zuizui0223/izu-core/releases/tag/q3-distribution-triangle-20261014): 18 raw archives and three JSON documents, 21 assets total. The tag points to the activation commit. Raw ZIP bytes total 1,612,337,879.
- Compact exact documents and the delivery receipt are in [`data/results/q3_triangle_20261014`](../data/results/q3_triangle_20261014). `READOUT.json` SHA256 is `7a3d5bf9cfd032cc625a3ae23a5a461123eec450aa0f17b48a917c28c01926c5`; `CAMPAIGN_MANIFEST.json` is `8cd325bee8abaf609b85fa3f4eec1e60d96b0e6f88ec29d70d6c62d06f7ad5e7`; `INDEPENDENT_VERIFICATION.json` is `84843bca983665b95daa6a4cb2747248708f133b079a25b245b4429b9d413754`.

## All eight frozen decisions

`D_A = I_B - I_A`, `D_C = I_B - I_C`: positive means lower terminal mean under A or C. `G_A = E_A - E_B`, `G_C = E_C - E_B`: positive means more historical events under A or C. The event is the original-baseline minus current-mean threshold of 0.05 sustained for 20 consecutive eligible censuses in years 0..200, including the shared pre-intervention history.

Intervals are the predeclared simultaneous conditional 95% Hoeffding family, with no observed-variance substitution. Values below are rounded to eight decimal places; exact values and classifications are in `READOUT.json`. Operational equivalence means the entire interval lies within +/-0.01 for mean differences or +/-0.05 for event-probability differences. These are reporting margins, not established ecological minimum effects.

| Block | Contrast | Estimate | Simultaneous interval | Direction | Operational decision |
|---|---|---:|---|---|---|
| Main | D_A | 0.00452225 | [-0.00163376, 0.01067826] | unresolved | unresolved |
| Confirmation | D_A | 0.00338123 | [-0.00267467, 0.00943714] | unresolved | equivalent within +/-0.01 |
| Main | D_C | 0.00026802 | [-0.00896600, 0.00950203] | unresolved | equivalent within +/-0.01 |
| Confirmation | D_C | -0.00014835 | [-0.00923221, 0.00893551] | unresolved | equivalent within +/-0.01 |
| Main | G_A | 0.05772569 | [0.00847761, 0.10697378] | positive | unresolved |
| Confirmation | G_A | -0.00303819 | [-0.05148544, 0.04540905] | unresolved | unresolved |
| Main | G_C | -0.04904514 | [-0.09829322, 0.00020294] | unresolved | unresolved |
| Confirmation | G_C | 0.00585938 | [-0.04258787, 0.05430662] | unresolved | unresolved |

The main G_A interval excludes zero but does not lie above the five-percentage-point operational margin. The main G_C upper limit is positive, approximately 0.000203: a negative point estimate is not a resolved negative effect. Neither contrast establishes a replicated event direction, and the different block classifications do not establish an interaction. No interaction test was registered.

The equal-variance B/C terminal-mean contrast is operationally equivalent in both blocks, with unresolved direction. This is evidence for a bounded difference between these particular policies, not identical trajectories, zero support effects in all settings, or universal sufficiency of variance. A/B terminal-mean equivalence is established only in confirmation; its main interval slightly exceeds +0.01. There is no event equivalence decision.

| Raw historical event count | A | B | C | Triggered triplets |
|---|---:|---:|---:|---:|
| Main | 2,074 | 1,808 | 1,582 | 4,464 |
| Confirmation | 2,856 | 2,870 | 2,897 | 4,320 |

These are counts among triggered futures. Contrast estimates use all 32 original slots, including zero-policy slots: for example main G_A = (2074-1808)/(32*144). Do not divide those count differences by triggered triplets to reinterpret the reported estimand. Survival pattern 111 has 8,784 triplets; every other pattern has zero.

## Answer to the central question

The [existing-record analysis in PR #515](CHAPTER2_Q3_EVENT_CONDITIONS_RESULTS_20261014.md) gives a pathwise explanation for the original mean/event discrepancy. Under the original restoration width, the main starting states allow event gains and forbid losses on occupied paths; confirmation allows losses and forbids gains. Its frozen baselines, allele support and shared history constrain eligibility differently. A lower expected terminal mean therefore need not increase a 20-census historical-event probability. This logical explanation is not replaced by the new experiment.

The new intervention adds a causal policy comparison beyond that support argument. With identical support, A versus B changes main-block event probability. Therefore the exact support set alone is insufficient to characterize that probability over these assignments. Allele frequencies and genotype composition matter as a complete policy, although the present contrast cannot attribute their effect uniquely to variance. The corresponding confirmation effect remains unresolved. The experiment does not establish a universal positive effect of increasing carrier fraction or variance.

For B versus C, equal initial allele variance accompanies a wider support and fewer carriers. The terminal-mean differences are bounded within the declared +/-0.01 convention in both blocks; event directions are unresolved. Consequently this experiment neither establishes a general support-driven event effect nor supports the claim that widening support necessarily increases events. It also does not establish a reversed effect from the negative main point estimate.

Temporal information remains essential to the historical endpoint. In the verified original archive, all 72 confirmation losses refixed at the upper endpoint before an event could complete, but 424 confirmation paths with events also refixed at that endpoint after or at event completion. Five main event gains subsequently fixed at the upper endpoint. These observations show why terminal fixation alone cannot reconstruct the event. They do not estimate the effect of preventing fixation: refixation is post-intervention, and selecting paths by it changes the comparison population.

The triangle did not intervene on persistence maintenance, trigger time, observation horizon or native-versus-restored assignment. Their causal policy effects are still unmeasured here. In particular, its small mean differences among A/B/C do not contradict PR #514's native-versus-restored mean effects: the interventions, allocation law and conditional comparison are different.

## Why abstract components and maintenance remain unidentified

Within this three-point family, variance is V=q w², and the fourth central allele moment is q w⁴. At fixed w, changing V necessarily changes q, heterozygote count and higher moments. At fixed V, changing w necessarily changes q. A/B and B/C identify two well-defined assignment contrasts; they do not independently manipulate a variance coordinate while all genotype properties remain fixed. Such a request needs an explicitly defined family of distributions, not extra repetitions of these same three policies.

A constructive nonidentification example makes the extrapolation limit explicit. Write h=1/16 and let F(w,q) be any response surface agreeing with the three policy responses. Then F_c(w,q)=F(w,q)+c(w-h)(q-1/16) agrees at A, B and C for every c, because A/B have w=h and C has q=1/16. At an untested admissible assignment with w different from h and q different from 1/16, these surfaces disagree. For an event-probability surface the construction can be restricted to a neighborhood with interior probabilities and sufficiently small c. This is a response-surface identification argument, not a claim that arbitrary F_c is generated by the frozen native model. It shows that the three assignments alone cannot identify a unique response surface or effects of additional assignments without extra structural restrictions or direct interventions.

Likewise, an observed association between refixation and events is compatible with different responses to a hypothetical maintenance policy, because that policy was never assigned. To measure such an effect requires specifying exactly when and how alleles are reintroduced or redistributed, what happens to carrier identity, heterozygosity, expressed I, reproduction and ancestral labels, and what control receives otherwise. The [maintenance feasibility proof](CHAPTER2_Q3_MAINTENANCE_FEASIBILITY_20261014.md) shows that positive variance cannot be restored at endpoint fixation while preserving both the mean and the original support interval; a proposed isolated operation with all those constraints is impossible. Timing effects require a defined time or horizon intervention with a target that separates elapsed opportunity from different biological starting histories. Each would require its own frozen estimand, randomization, resources and approval. No such new biological experiment is performed or activated by this report.

## Verification, consumption and reproduction

Production used 3,343,680 annual native updates; independent replay used the same. Continuation fixtures used four updates. Including the prior preserved HOLD's four fixture updates, total consumption was 6,687,368 native updates, below the original 6,687,392 cap. Scientific paths total 26,352, not doubled by counting replay as new trajectories. The manifest retains the previous zero-science HOLD and cumulative reservation of 300 runner-minutes; this reservation is not an assertion of 300 minutes actually consumed.

Every raw trajectory stores individual IDs, alleles, ancestry labels, mutation flags, birth years, census offsets and parentage, with assignment permutation and source/seed identities. The producer independently replayed fields and parentage; the publication reader verified archived members and recomputed endpoints, weights, intervals and classifications. `INDEPENDENT_VERIFICATION.json` reports `INDEPENDENT_SUMMARY_MATCH` for 8,784 triplets and 64 slots, with zero native updates in publication. Publication downloaded every uploaded raw archive and matched its bytes/hash. The additional local delivery check downloaded the three compact documents and matched all 21 asset sizes/digests to the manifest and GitHub API. It did not locally repeat native replay or download all raw ZIPs again. Content hashes identify the evidence; GitHub platform immutability is not asserted.

For read-only inspection, download the three documents from the release and compare their hashes above. For full raw-only recomputation, use the pinned `verify_q3_triangle_archives_20261014.py` functions `verify_shard`, `verify_campaign` and `verify_summary`, together with `q3_triangle_contract_20261014.py:summarize` and the frozen preflight at the activation commit. Download one named shard at a time and verify against its manifest hash. These readers make no native updates. Do not rerun the activated production workflow: its one-time admission and cumulative budget are exhausted.

## Scope of completion and remaining work

The approved triangle campaign and its two policy contrasts are complete and preserved, including unresolved and equivalent outcomes. It supplies a main-block fixed-support event effect and bounded equal-variance terminal-mean contrasts, while preserving the earlier support/history explanation. A complete replicated directional mechanism has not been demonstrated. Abstract component attribution, persistence-maintenance effects and timing interventions remain unidentified or unmeasured as described above; they are not labelled solved. The broader Q3 goal therefore remains active pending its evidence/requirements review and any necessary separately specified intervention. Q1/Q2/Q4, manuscript integration, other chats' order-effect work and natural-history causation are outside this report. Main is not merged.
