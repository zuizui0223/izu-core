# Q3 continuation execution ledger

Base: `2c3023ba9e06fcc604e554d5711cc5fe3e8187f8` on the isolated PR516 branch.
Task1: implemented (pending final review/CI/approval). Tests: Python3.10
`-m pytest tests -q --tb=short --basetemp=../triangle-continuation-green`
passed109. The new14 continuation tests first failed before implementation.
No native/RNG calls were made for these tests.

Ruling: Existing source staging uses GitHub Git Data API publication with
expected-head checks, not a local Git checkout. Review package therefore names
the exact published base and all changed files; native Git plan helper scripts
are inapplicable. Risk: omitted-file review; mitigate by explicit publish list
and remote blob/hash verification.

Ruling: Preserve failed raw transport in a separate technical-HOLD release,
rather than duplicate it in the eventual scientific release. Final manifest
links its pinned hash/URL; it stays within the original64GiB reservation.
The release ZIP and audit JSON were externally read back and matched exact
SHA256 hashes. Risk: link availability; hashes remain in repository and output.

Ruling: Reserve1 runner-minute for the observed31-second failed shard job;
reduce only final aggregation29minutes, keeping18*15 shard budgets. Prior
cancelled jobs had no steps. Risk: aggregate readback may time out one minute
earlier; failure remains technical HOLD, never partial scientific publication.

Final review: fresh independent reviewer found no Critical/Important/Minor;
independently109 tests passed in6.01seconds. Live prior payload and old approval
rejection verified. Review evidence: docs/reviews/Q3_TRIANGLE_CONTINUATION_REVIEW_20261014.md.

Final: Ruling: live native speed, exact pinned runtime, future release
availability and29-minute publication completion are untested until approval.
Keep runtime gates and hard timeouts; a failure yields HOLD, not a scientific
null or unapproved retry. Cost if wrong: campaign can stop technically.
Final: Ruling: approval/candidate/CI are still pending author gates; no reviewer
or test result substitutes for them. Cost if bypassed: unauthorized execution;
the new activation file remains absent.

Concrete continuation approval: absent. No new activation file exists; the old
manifest is unchanged. No deferred minor findings.
