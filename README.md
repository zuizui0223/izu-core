# Campanula Channel Identification

A field-design and causal-identification repository for asking a deliberately narrow question about island floral-trait variation:

\[
W(z)=F(z)E(z).
\]

For a predeclared trait \(z\), can a difference between island regimes be assigned to

- **local reproduction** \(F(z)\), or
- **establishment / reachability conditional on viable seed output** \(E(z)\),

rather than merely described as a difference in flower size, mating system, visitor identity, or island position?

## Current development mainline

The mechanistic chain is **not yet causally identified**. The active development target is Issue #91: collect the first real direct effective-pollinator dependency pilot for *Campanula microdonta* and move from a field-ready contract to measured plant-level dispersion, coverage/loss, and precision. Reliability of the final direct-dependency predictor is a separate repeated-final-estimand calibration problem, not an automatic output of the focal pilot.

The immediate empirical path is:

```text
first real six-channel field bundle
-> preflight and checksum freeze
-> linked plant / effort / visit / SVD / treatment / fruit / seed records
-> structural dependency admission
-> between-plant SVD and treatment dispersion
-> pilot variance / coverage-loss estimates
-> absolute precision target
-> confirmatory design

separate final-estimand calibration, if empirical reliability is required
-> independent non-overlapping plant panels for repeated taxon x site x season targets
-> calibration-scope dependency reliability
-> transportability review
-> only then possible replacement of synthetic dependency_reliability
```

Technical SVD recounts estimate pollen-count repeatability only; within-plant flowers or visits and biological dispersion from one unrepeated panel do not identify final predictor reliability.

Until that path is populated with real field data, the repository does **not** claim historical pollinator-loss causation, an Oshima--Toshima causal boundary effect, or a cross-lineage dependency-by-functional-environment interaction.

In parallel, cross-archipelago work may close a missing link in an already source-audited mechanism bridge. The current strongest near-complete bridge is the Xisha *Cordia subcordata* two-island system; it still lacks Dong-specific direct single-visit effectiveness and controlled reproductive-dependency measurements. Source-controlled gates such as the Weigela / Ligustrum / Hosta queue stay parked until genuinely new lawful source material arrives.

Machine-readable routing lives in [`data/design/active_development_mainline.json`](data/design/active_development_mainline.json). The narrative companion is [`docs/ACTIVE_DEVELOPMENT_MAINLINE_20260813.md`](docs/ACTIVE_DEVELOPMENT_MAINLINE_20260813.md).

## Current scientific state

The source-locked focal Campanula calibration currently retains:

- **floral size:** continuous erosion across the focal island series;
- **multilocus outcrossing:** continuous erosion;
- **autonomous reproductive assurance:** a second-transition step;
- **visible signal / nectar-guide channel:** blocked-unmeasured and prospective only;
- **historical Bombus causation:** not identified; and
- **universal Izu-flora rule:** not supported as a current claim.

External morphology shows directional recurrence in two independent systems under the declared OLS + island-cluster analysis, but no pooled universal island coefficient is admitted. Measurement-error identification is unresolved, and the formal cross-system fit remains closed because compatible same-family effects are not replicated across enough independent system clusters.

See [`docs/CURRENT_EVIDENCE_STATE.md`](docs/CURRENT_EVIDENCE_STATE.md) for the canonical claim boundary. When an older pilot, simulation, discovery note, or manuscript fragment conflicts with the generated/current state, the source-locked registries and current-state contracts take precedence.

The current counts and claim boundaries can be regenerated from committed tables:

```bash
python scripts/report_current_evidence_state.py \
  --markdown-out artifacts/current_evidence_state.md \
  --json-out artifacts/current_evidence_state.json
```

## What this repository does

- protects source locks, canonical result registries, negative admission states, and claim-boundary regressions before implementation cleanup;
- defines the direct field measurements needed to distinguish effective service from reproductive dependency;
- freezes and audits linked plant, observation-effort, visitor-contact, single-visit pollen-deposition, pollination-treatment, fruit, seed, and optional parentage records;
- distinguishes direct measurements from proxies whose calibration must be stable or independently checked;
- keeps published patterns, prospective field measurements, and pollinator-specific claims separate;
- compares cline, threshold, no-response, and environment/history alternatives only where the required observation model is declared;
- uses source-native or independently replicated systems as falsification / bridge evidence without converting heterogeneous observations into a universal coefficient;
- retains a small set of constrained diagnostic tools only when they enforce a current claim boundary or measurement decision; and
- keeps unfinished visible-signal work and exhausted discovery routes outside the active evidence path.

## What is not the development mainline

The following do not advance the current scientific admission state by themselves:

- historical nectar-guide / visible-signal inference from public images;
- a universal island-dwarfism coefficient;
- accumulating more island counts without independent-system replication;
- treating visitor occurrence or identity as pollinator effectiveness;
- repeating an already exhausted source-recovery route;
- formal meta-analysis before compatible same-family replication exists; or
- adding simulation complexity that does not change an admission or field-measurement decision.

Historical implementations and failed routes remain recoverable from Git and PR history; their scientific lessons are summarized in [`docs/RESEARCH_TRIALS_RETROSPECTIVE.md`](docs/RESEARCH_TRIALS_RETROSPECTIVE.md).

## Response domains

A lineage may enter through one of several explicitly separated domains:

| domain | examples | what it can test |
|---|---|---|
| quantitative trait | flower size, outcrossing rate, bagged capsule set | within-lineage cline or step |
| binary/ordinal state | SI/SC, autonomous reproduction absent/present, accessible/restrictive floral form | regime-associated state transition |
| interaction state | effective guild, partner breadth, legitimate-contact class | ecological rewiring, after effectiveness gates |
| island occupancy | species present/absent by island | filtering or range truncation, not trait evolution |

Raw occurrence is never converted into a floral phenotype. An occupancy analysis asks whether a dependency class crosses a regime boundary less often than a control class; it does not show that an extant island population evolved a particular trait.

## Generalist falsification

Open-generalist lineages are not assumed to be absolutely invariant. The prospective prediction is narrower: they should not repeatedly share a specialist-specific breakpoint at the same pollinator-regime boundary. The primary contrast is therefore a dependency-class × boundary interaction, with climate, area, isolation, history, observation effort, and lineage dependence modelled explicitly.

## Simulation boundary

Any retained simulation or diagnostic layer is a design or identifiability aid, not evidence that the same mechanism generated the field pattern. Synthetic recovery, candidate ranking, or a successful virtual reconstruction cannot substitute for direct effectiveness, reproductive-dependency, provenance, and uncertainty measurements.

## What it does not claim

A visit count is not automatically a measurement of local reproduction. Flower-size means, mating-system estimates, pollinator turnover, and occupancy alone do not identify \(F\) versus \(E\).

A high-ranked measurement is not automatically the best field protocol: feasibility, sampling variance, biological relevance, and cost still require an explicit design check.

The factorisation is a declared model choice. It does not claim that all natural processes are multiplicative or independent.

## Repository boundary

This is the active empirical design home for the Campanula/Izu channel-identification programme extracted from `microdonta`.

The active tree is intentionally narrower than its Git history. Exploratory public-photo pipelines, broad literature-discovery machinery, legacy synthetic stress suites, and other completed one-off trial implementations are kept out of the current execution surface once their reusable scientific lesson, provenance state, or negative result has been frozen.

## Relationship to RACH causal invariants

[`rach-causal-invariants`](https://github.com/zuizui0223/rach-causal-invariants) is the separate general-methods repository. It provides finite qualitative-program grammars, robust-admissibility classifications, coverage labels, and exact known-truth observation-channel calibration. It does not specify floral fitness, island geography, pollinator guilds, pollen deposition, recruitment, or any Campanula parameter.

This repository owns those biological assumptions: the \(F(z)E(z)\) factorisation, island-regime definitions, response-shape contracts, observation units, and field protocols. A predeclared subset may be translated into a RACH candidate universe to audit logical consequences; that translation is not empirical validation of a biological mechanism.