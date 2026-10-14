# Final review: Q3 event results and distribution triangle

Reviewed the event-conditions results document, distribution-triangle document, triangle constructor and triangle tests against the recorded state/pair tables, summary, independent verification receipt and feasibility receipt.

## Verdict

No remaining substantive scientific, implementation or evidence-consistency finding. The documents distinguish demonstrated restrictions, observed paths and unexecuted policy effects. The proposed triangle has the stated conditional minimality; its two contrasts do not identify unique abstract support or variance effects. No new biological execution is implied by this review.

## Evidence checked

- Verified all four output hashes listed in `INDEPENDENT_VERIFICATION.json` against the current state table, pair table, summary and provenance. Verified the receipt's verifier hash against the current verifier script. The receipt documents independent raw recomputation of all 20 fields in each of 64 state rows and 3,904 pair rows; this final review did not rerun raw future extraction.
- Confirmed reported counts, support-class inventories, original-slot terminal differences and refixation cross-tabulations against `SUMMARY.json`. Confirmed from the CSVs the unique window exclusion at confirmation r6, t=197, k=0, in the support-excluded class. Confirmed the confirmation upper-refixation event-timing assertions and absence of upper-refixation-before-completion cases among both-event paths.
- Verified the feasibility receipt's constructor hash and archived allele-domain-source hash. Read the archived PlantState validation showing the admitted allele domain [0,1].
- Independently reconstructed the deterministic allele edits for all 183 policy/state combinations directly from the 61 archived ORIGINAL trigger states, without importing the constructor. Each resulting little-endian float64 allele-array hash matches its receipt. All states have shape (48,3,2), their I copies equal the recorded v, all policy support sets and exact variances match, and individual expressed values are unchanged. No raw future paths were extracted during this check.
- Independently ran all three relevant test modules: **35 passed**. An initial test invocation selected a temporary directory whose parent did not exist and produced one fixture-setup error; rerunning with an existing-parent workspace temporary location yielded 35 passes. This was a reviewer invocation-path issue, not a test or implementation failure.

## Scientific interpretation

The input support classes and shared-history restrictions justify the direction bounds on occupied paths. They do not predict exact event counts or establish unrestricted extinction-outcome bounds. The results document states those conditions and explicitly retains the unresolved original primary and confirmation margin conclusions.

Refixation is treated as a descriptive post-intervention witness. The results do not convert its association into a fixation-prevention effect. The illustrative expectation/event example is algebraic and its mixture probabilities are explicitly not fitted model probabilities.

A and B share the exact three-point support set; B and C share allele variance. All three policies preserve individual expression at intervention, while allele frequencies, carrier counts and other distribution properties change. The document states these limits, uses an existence-only deterministic construction witness, and defers random carrier allocation and its estimand to a fixed execution contract. The optional fourth cell has the correct six-carrier count and would add the missing factorial policy contrast.

## Completion boundary

The descriptive readout and genotype-construction feasibility are supported by the reviewed evidence. Future triangle effects remain unknown. This review provides no approval to generate new biological futures and does not replace the later endpoint, allocation, precision, resource and execution contract.
