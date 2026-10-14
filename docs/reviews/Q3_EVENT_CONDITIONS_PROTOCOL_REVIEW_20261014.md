# Q3 event-conditions protocol review

Reviewed: `docs/CHAPTER2_Q3_EVENT_CONDITIONS_PROTOCOL_20261014.md`.
Scope: mathematical threshold/history restrictions and prospective genotype family only. No raw outcomes were extracted; no biological simulation, replay, or random draws were performed. This review does not validate the supplied archive hashes or empirical inputs.

## Verdict

No critical or important mathematical finding. The protocol is suitable for publication before the new pathwise extraction. Its outcome-informed exploratory designation and its distribution-policy interpretation appropriately limit the claims.

## Mathematical checks

- With the shared prefix including census t, there are exactly T=200-t later censuses. If no event has completed through t, the trailing eligible run k is at most 19. Thus T+k>=20 is the correct necessary optimistic condition; equality allows completion at census 200. If an event already completed, future failures cannot remove it.
- Eligibility is monotone in mean investment for a fixed baseline and the stated predicate. Under occupied censuses and supported means, only the four tabulated patterns are possible. Native future eligibility is constant. When the centre is ineligible, a restored loss is impossible; when the centre is eligible, a restored gain is impossible. In the two extreme support classes both paths have identical future eligibility. These conclusions also require the shared census-t eligibility to match, which the protocol checks via expressed I.
- Reconstructing native history with the prefix through t plus T later copies of v is consistent with the inclusive 0..200 event definition. The separate instruction using original years strictly before t plus future years t..200 avoids double-counting the trigger census.
- The confirmation gain bound must use centre-ineligible inputs with no pre-existing event and enough time, with support-excluded states removed. In particular, if no gain-possible input survives those restrictions, its gain bound is zero independently of observed outcomes. The actual inventory is deliberately not assessed here.
- For qN heterozygotes [v-w,v+w] and remaining homozygotes [v,v], equal weighting of the 2N allele copies gives mean v and population allele variance qw^2. Every listed q, V and heterozygote count is correct at N=48. Expressed investment is v for every individual at intervention.
- Matched-variance and matched-width contrasts change other distributional features. The protocol correctly limits interpretation to assigned genotype-distribution policies. Four cells support a factorial interaction contrast once an outcome scale and execution contract are fixed; three cells cannot supply the full four-cell interaction without additional assumptions.

## Feasibility clarification verified

Verified final protocol SHA256: `b3baf3a7909a1557451f4197398870b1574121b6533489381fef0744601264a0`.

The revised protocol explicitly requires N=48, integral qN, and admitted values v-w and v+w, checked against every admitted state and frozen source. It prohibits clipping, rescaling, replacement and selective state removal to repair a failure. This resolves the nonblocking feasibility clarification raised during review. Algebraic feasibility is appropriately distinguished from model-wide feasibility. No outstanding revision request remains.

The later allocation contract should define the actual heterozygote subset policy and the outcome scale for any interaction. The current requirement to freeze genotype subset allocation and endpoints provides an appropriate place for those details.


