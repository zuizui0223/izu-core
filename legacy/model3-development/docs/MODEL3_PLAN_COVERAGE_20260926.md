# Model 3 implementation-plan coverage audit

2026-09-26. Scope: plan completion, not code implementation or scientific confirmation.

Plan: `superpowers/plans/2026-09-26-model3-island-ecology.md`.
Reviewed against `MODEL3_ECOLOGICAL_COMPARISON_CONTRACT_20260926.md`, `MODEL3_ISLAND_ECOLOGY_REDESIGN_20260926.md`, and the nearest-precedent audit.

| Requirement | Plan evidence | Status |
|---|---|---|
| Preserve frozen results and Q1 independence | Global constraints; Tasks 1, 10 | Specified |
| Explain existing finite/density attenuation | Package A; exact recruitment and individual pollen accounting | Specified; cause remains unproven |
| Direct versus assurance-mediated floral change | Task 4 fixed-state assays; Task 6 inherited assurance; timing/discounting sensitivity | Specified; no claim of clean statistical mediation |
| Arrival, loss, mismatch and recovery | Task 5 temporal replay and assembly; Task 8 contrast families | Specified |
| Distance and oceanic/continental histories | Separate kernels/source supplies; founding/separation initialization and matched-state controls | Specified as idealized histories, not calibrated geology |
| Mutation, drift and immigrant replacement | Task 6 alleles/ancestry; independent random streams; Task 9 denominators | Specified; fixed depression does not model purging |
| Life history and biological time | Parent birth years and realized generation interval; matched annual/lifetime budgets | Specified; seed bank/juvenile delay excluded explicitly |
| Old k ecological analogue | Task 9 reference-panel service covariance and reproductive weights | Specified as a diagnostic, not equality with pooling k |
| S/C/I and transport | Task 9 crossed cells, within-cell noise, fixed weights, held-out regimes | Specified; no forced ranking reversal |
| Numerical comparison | Tasks 1, 2, 7; matched grids and conditional visitor paths | Specified; true PDE is optional and requires derivation |
| Replication and compute scale | Task 8 precision, disjoint cohorts, ceilings, manifest; Task 7 resource pilot | Production numerical choices must be frozen prospectively |
| Concrete implementation | Ten tasks with exact file paths, public interfaces, tests, commands and commit scope | Written, not executed |
| Novelty evidence | Nearest-precedent document; claim exclusions and candidate discrimination | Targeted audit complete enough for design; no priority guarantee |

## Self-review corrections

Added genotype mutation flags to the shared state; assurance timing/costs to the configuration; explicit abundance versus richness modes; and an effective-exposure estimator. These prevent later tasks from inventing an undeclared interface or treating richness loss as abundance loss automatically.

The reproductive sensitivity operators are declared phenomenological model choices, not fitted natural constants. Full production values are deliberately not fabricated in this plan. The executable manifest validator must reject missing scientific values. The future production-design gate is part of implementation, not evidence that a campaign can run immediately.

## Verification performed

Confirmed the ten task headings, existing spec files, baseline hash, independent-Q1 rule, mutation specification, extinction handling, prospective production refusal, and held-out seed specification. Read the contract-to-task mapping and corrected missing interfaces above. The tracked-code diff is empty; the plan is a new untracked documentation artifact. No tests or simulations were represented as run.

## Handoff

The planning objective is satisfied. Implementation remains a separate execution stage requiring review of the written plan and choice of native or delegated execution under the active planning skill. Native sequential execution is recommended because early operator audits constrain later interpretation. Existing baseline numerical results remain unchanged.
