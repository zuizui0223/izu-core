# Original clock source checkout correction

The reviewed PR503 head is183a386f272fd3aa49429c2cdc24aba7c34c8361. Source/Spec review found the main PR497→500–503 route consistent with its frozen1,536-case/128-cluster, phenotype-matched design, but ordinary Windows checkout changed LF source bytes to CRLF. Exact Git-blob admission correctly rejected those changed bytes before any model replay. For example, registryf18eae09 became9c901169 and reproduction95314698 became038bb5f4 under CRLF representation.

The correction sets `text eol=lf` only for clock JSON/scripts and the five pinned original model modules. It does not normalize bytes inside the scientific readers, change any pin, modify a model function, enable the pilot, change an event or rewrite an output. A real Git fixture checks both core.autocrlf=true and false against ten unchanged frozen source/input anchors and three producer/reader/packager source byte strings. Files are removed only inside that isolated fixture so checkout conversion is genuinely exercised rather than skipped as up to date. The Windows-style case failed before correction; both cases pass afterwards.

For this existing clean corrective checkout,27 affected source/input files were refreshed from their exact HEAD Git bytes only after verifying the old representation differed solely by CRLF. Git renormalization left every original protected blob unchanged. An existing checkout needs an equivalent safe refresh or a new checkout; adding attributes alone does not force Git to rewrite files already considered up to date. Never discard unrelated local edits to perform this refresh.

The native producer's five source-byte gates pass after refresh. The checkout/input-inventory/six-shard/external-reader/factorial-summary/package checks pass on Windows, except the existing actual-symlink test cannot execute without the Windows symlink privilege; that test remains unchanged and must run in Linux CI. These are source and synthetic-byte/report checks, not new registered200-update histories.

## Separate numerical environment limit

LF preservation does not solve cross-BLAS floating arithmetic. PR498 already records that matching NumPy2.2.6 alone does not guarantee identical final bits on all machines; the PR503 replay reader deliberately checks exact annual ledger hashes and replayed genotypes. A different numerical environment may therefore STOP even with correct source bytes. That STOP must be retained and diagnosed, not converted to biological disagreement or bypassed by relaxing hashes. A full replay-environment contract and demonstrated actual pilot replay remain separate requirements.

## Single active implementation route

Use the PR497→500–503 registryf18eae09 route for this correction: AL/I case keys and257-member ZIPs. The sibling PR498/499 registry072151 route uses w24/i keys and259-member ZIPs; it remains separate provenance and cannot be substituted into the PR503 reader/packager. Neither route has produced an admitted scientific pilot here. Assurance/investment accessibility interventions do not establish a continuous ecological reversal boundary or a natural-order persistence benefit.
