# Q3 actual results and claim review

Decision: **PASS for the completed fixed-design result and the bounded interpretation below.** No native update, replay, new seed, or duplicate artifact download was performed by this reviewer.

## Evidence inspected and independently checked

Production is identified by GitHub run `38508868485`, commit `d92ac4324b6e1c8924dcc8e5f30e0750088a3acf`, and execution-manifest SHA256 `54549eeec37a225526883fad4f08ae11a417a87b12adede05346425114d83c93`.

The completed publication, admission, synthetic-fixture, resource, independent-replay, independent-readout and READOUT receipts were inspected. The artifact contains 7,808 scientific paths / 3,904 registered pairs. The replay receipt records 990,720 native replay updates, 4,992,640 state-field checks and 990,720 parentage checks. Four fixture updates are explicitly separate from scientific replicates.

The reviewer independently read all 3,904 archived pair receipts and recomputed the three estimates and interval widths using separate arithmetic, without importing the producer's summary. All match the published readout. Exact case/replicate coverage, production/replay update totals, state/parent check totals, and per-case secondary-event counts also agree. The budget contains exactly 3,905 unique reservations: one four-call synthetic fixture reservation and one production-plus-single-replay reservation per pair, totaling 1,981,444 calls.

The completed external raw-only check was then inspected. Its status is `EXTERNAL_ALL_MEMBERS_RAW_LAYOUT_AND_PRIMARY_READBACK_PASS`; it binds the exact execution/preflight/source bytes and all 7,808 raw endpoints to their pair receipts, verifies all 12,042 archive members, and reports 998,528 saved censuses. Its recorded verifier hash matches the previously reviewed external checker. It used zero native calls. Secondary events were not rederived by this external checker; their complete onboard independent check and the reviewer's receipt-level arithmetic remain the evidence for those summaries.

Final reported remote disk use is 980,265,810 bytes, below 17,179,869,184 bytes. Total reserved/actual native calls are 1,981,444, below 1,981,472. The final publication receipt plus external check reports 1,823.6523724 conservative worker seconds, below 28,800. This is the recorded scientific execution/verification accounting, not a claim about every human-review activity or total CI job time.

## Registered primary result

All 3,904 pairs survived in both arms (main 1,984; confirmation 1,920); the all-pairs-survive gate passes. The three no-trigger slots remain policy zeros. The contrast is native minus restored terminal mean I, using original-slot weights.

| Original-slot average | Estimate | Simultaneous conditional interval | Direction | Practical classification at delta = .01 |
| --- | ---: | --- | --- | --- |
| All 64 slots | 0.01674493154 | [0.01379478227, 0.01969508081] | Positive | Positive |
| Main, 32 slots | 0.02093378703 | [0.01672758706, 0.02513998700] | Positive | Positive |
| Confirmation, 32 slots | 0.01255607605 | [0.00841827414, 0.01669387796] | Positive | Unresolved |

The intervals have the protocol's simultaneous conditional coverage guarantee of at least 95% for the three registered means, under the fixed source states and independent fresh-stream assumption. They are not per-state or new-founder intervals.

**Directional replication is positive:** both block intervals are wholly above zero. **Practical replication above .01 is not established:** the confirmation interval straddles .01, despite its point estimate exceeding .01. It is also not an equivalence result.

## Permissible conclusion

> For the two fixed original-state blocks, the specified one-time restoration to I alleles v ± 1/16 lowers expected terminal mean I relative to unchanged fixation, averaged with original-slot weights under the registered fresh-future coupling and conditioning on paired survival. Both block intervals support this direction. The .01 operational threshold is exceeded by the all64 and main intervals; whether the confirmation average exceeds .01 remains unresolved.

“Restoration promotes terminal I reduction in both fixed blocks” is acceptable only when accompanied by those policy, averaging and paired-survivor conditions. Prefer the explicit wording above over an unqualified statement about variance, natural evolution, or persistence.

## Claim ceilings retained

- This is an outcome-informed follow-up for fresh futures of fixed states. The original primary remains `unresolved_unchanged`; it is not replaced or retroactively declared positive.
- The result is not independent founder replication, and it does not establish every state's expected direction. It is not an unconditional average treatment effect, a pooled survivor mean, or an effect for natural populations.
- Zero observed extinction is not zero extinction risk and does not demonstrate a survival/persistence benefit. The design's survival categories are descriptive.
- The intervention is a diagnostic, one-time allele restoration. It is not natural mutation or continuing maintenance of genetic variation.
- The contrast does not separately identify support-width, allele-variance, refixation-mediated, or remaining-duration contributions. Initial among-individual expressed I variance is unchanged by restoration; “variance effect” would therefore also require specifying which variance is meant.
- The common expected block direction under this target does not uniquely prove that the original mixed signs were caused by noise. The old and new inferential targets/conditioning differ, and fixed-state heterogeneity and mechanism attribution remain unresolved.
- No Q1 ecological threshold, Q2 causal order, Q4 assurance-first survival benefit, manuscript integration, or main merge is established by this result.

## Immutable result identities

- Inner scientific archive SHA256: `8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e` (410,326,692 bytes).
- READOUT SHA256: `10e72db05792292e31862733d57b79589abc12ea3eec62caab64018a05d58cef`.
- External readback receipt SHA256: `f0962abe3a5ca66e36d81de1e7111c970bd29960f93f44f55d76a41f866b0d21`.
- External verifier SHA256: `db54db56f9dbc5904934ef371e76236905a90f9eb6da8ba7420d03837875c3df`.

Reviewer scratch evidence: `actual-receipt-arithmetic.json` and `audit_actual_receipts.py`. The scratch arithmetic receipt was generated before the external check finished, so its `external_all_raw_readback_still_required` field describes that intermediate moment; the external PASS inspected above closes that requirement. This report does not substitute for reviewing the final results document's wording against these limits.
