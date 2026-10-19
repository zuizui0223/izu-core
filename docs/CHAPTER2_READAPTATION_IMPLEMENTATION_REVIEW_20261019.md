# Bounded readaptation implementation review

Review range: `b79daac15241a6963d3e56c82a3692b80251d530` to
`1e7522c909e235edff8ab40bf53e85b00e7a133a`.
A fresh read-only reviewer independently ran 87 tests: 82 readaptation and
five existing matched-A/I tests. No scientific donor futures were executed.
The review found one Important issue, no Critical issues and two Minor issues.

## Important issue and verified correction

The independent raw auditor admitted absent or invalid demographic/reproductive
telemetry and altered column labels. State and assay checks did not cover these
fields. This was an arithmetic/schema defect, separate from native biological
probability replay.

Ten corruption cases first failed because the auditor did not reject them:
missing fields, negative counts, NaN returns, changed labels, oversized/wrong
shape, wrong recruitment count, wrong selfed count, wrong parental age sum,
fractional demographic counts and reproductive mass-balance violation.

The correction enforces the complete versioned future field inventory, exact
column labels, dimensions/dtypes, finite/nonnegative values, next-census
recruitment counts, no survival/immigration, parental age/contribution counts,
selfed/outcross counts from parent IDs, and reproductive accounting constraints.
All 97 related tests passed after correction (92 readaptation plus five matched
A/I). This is regression verification of the fix, not a second independent
review or a biological replay certificate.

## Deferred Minor findings

- Generic file publication does not reject every oversized serialized record
  before publication. The normal bounded producer stays within the limit; the
  newly enforced telemetry schema rejects the reviewer's oversized-array case
  before the runtime wrapper publishes it. Generic prepublication size admission
  remains deferred defensive hardening.
- The local-design document's implementation-status paragraph predates the
  source/cohort binding and resource primitives. Use this review and the current
  PR description for implementation status until the final freeze updates it.

## Rulings on matters the reviewer did not certify

1. Native reproductive/assay probabilities and donor-production probabilities:
   remain a preproduction replay gate. Raw arithmetic must never be presented as
   independent verification of those biological operators.
2. New readaptation outcomes, A/I determinism, ordering and natural-history
   causation: no new scientific outcome is claimed. Inference requires the
   approved experiment and analysis, with its existing claim limits.
3. Production dispatch, approval enforcement, complete campaign resume and final
   manifest publication: remain unimplemented orchestration. Single-task
   checkpoint primitives do not make a complete campaign executable.
4. Worst-case memory/disk/runtime: retain the declared resource limits and
   runtime stops; five synthetic samples do not establish a worst-case bound.
5. Original donor/endpoint archive reads: existing live admission receipts are
   retained as executor evidence; the reviewer did not independently repeat them.
6. Live GitHub CI/merge assertions: must be checked separately on the final head;
   a local code review does not certify remote checks or merge state.
7. Complete endpoint/performance reporting and strict/epsilon support diagnostics:
   remain required before scientific closeout. Raw arrays make them possible but
   the current summary interface is not the final scientific report.

Production authorization remains false. No production-ready or central-hypothesis
completion claim follows from this review.

## Subsequent technical replay checks

Same-implementation replay primitives now cover historical fixed/evolving-A
offspring generation, all future arrays and metadata, and common-context assay
values. Four synthetic tests verify exact reproduction and rejection of altered
production/assay values or a substituted stream. The related suite passes 101
tests (96 readaptation, five matched-A/I). No scientific donor offspring or
futures were executed. These checks were added after the review range above;
they are not described as independently reviewed biological validation.

The tested local runtime is Python 3.10.11, NumPy 2.2.6 and SciPy 1.15.3.
At the post-test resource check, available RAM was 431,140,864 bytes, below the
1 GiB start threshold; free disk was 57,963,253,760 bytes. This is a transient
measurement, not permission to bypass the runtime resource gate. Full campaign
orchestration, production approval and final scientific reporting remain pending.

## Actions production gate review after explicit authorization

The user approved the fixed 10,240-future budget and requested GitHub Actions.
A fresh, focused reviewer inspected the new campaign, authorization receipt,
workflow and tests. This is the plan's separate pre-launch dispatch audit, not
a re-review of the previous scientific implementation.

Two Important findings were reproduced as failing regression tests and fixed:
(1) production now fetches full Git history so source admission can read the
immutable f7792629 commit; (2) a re-run attempt with no explicit resume_run
restores the latest retained checkpoint from that same Actions run, failing
closed when none exists. A new dispatch can explicitly select a prior run.
The restored RUN identity must match the exact source, contract and runtime.
The local combined suite passed 113 tests after this one fix pass.

The reviewer verified local tests and inspected allocation, source/configuration,
checkpoint and replay connections, but did not launch Actions or certify Linux
runtime, release downloads, completed campaign audit or measured total costs.
Those remain live execution gates. Proposal execution_authorized=false is
preserved historically; the separate Actions authorization receipt admits the
exact unchanged proposal hash. No scientific donor futures were executed during
this review or its fixes.
