# Campanula Channel Identification

A field-design, causal-identification, and constrained-simulation repository for asking a deliberately narrow question about island floral-trait variation:

\[
W(z)=F(z)E(z).
\]

For a predeclared trait \(z\), can a difference between island regimes be assigned to

- **local reproduction** \(F(z)\), or
- **establishment / reachability conditional on viable seed output** \(E(z)\),

rather than merely described as a difference in flower size, mating system, visitor identity, or island position?

## Current empirical state

The repository is currently a **three-channel focal Campanula calibration plus a prediction-locked cross-lineage regime-transition programme**, not a completed multi-species meta-analysis.

- floral size and multilocus outcrossing are retained as continuous erosion across the focal island series;
- autonomous reproductive capacity shows a source-locked Oshima-to-no-Bombus second-transition step;
- nectar-guide and visible-signal analyses are not adopted and contribute no current direction, breakpoint, or effect estimate;
- no independent specialist lineage is yet eligible for the positive holdout;
- one open-generalist lineage supplies a usable three-regime negative control;
- no public-photo ROI proposal is eligible for broad specialist release; and
- `environment_only` remains unranked until climate, area, isolation, and history enter an explicit comparison likelihood.

The comparative target is not a universal island cline. Each eligible lineage is tested against competing response shapes:

```text
no response
smooth cline
step at large-Bombus -> B. ardens
step at B. ardens -> no effective Bombus
two-step response
explicit environment/history alternative
```

The current counts, claim boundaries, and next admissible actions are generated from committed tables:

```bash
python scripts/report_current_evidence_state.py \
  --markdown-out artifacts/current_evidence_state.md \
  --json-out artifacts/current_evidence_state.json
```

See [`docs/CURRENT_EVIDENCE_STATE.md`](docs/CURRENT_EVIDENCE_STATE.md) and [`docs/REGIME_TRANSITION_COMPARATIVE_DESIGN.md`](docs/REGIME_TRANSITION_COMPARATIVE_DESIGN.md). When an older pilot or simulation document conflicts with the generated state, the generated state and its machine-readable source tables take precedence.

## What this repository does

- records the minimum theorem-compatible measurement design for the factorisation above;
- distinguishes direct measurements from proxies whose calibration must be stable or independently checked;
- keeps published patterns, prospective field measurements, and pollinator-specific claims separate;
- compares cline, threshold, no-response, and environment/history response shapes;
- permits continuous, ordinal, binary, and occupancy channels only through separate observation models;
- uses open-generalist taxa as negative controls for shared pollinator-regime breakpoints;
- generates a current evidence/readiness report so discovery counts and failed operators cannot be mistaken for empirical replication;
- provides a lightweight readiness checker for a proposed sampling design;
- provides constrained life-history simulations for comparing explicitly declared mechanisms against predeclared observation intervals;
- ranks future measurements by how strongly they distinguish the parameter candidates still compatible with current observations; and
- keeps unfinished nectar-guide work outside the current evidence state.

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

The simulation layer does not estimate an unobserved cost from a trait alone. It retains the **set of parameter values compatible with all declared observations**, then makes the remaining uncertainty explicit. A successful virtual reconstruction is not evidence that the same mechanism generated the field pattern.

## What it does not claim

A visit count is not automatically a measurement of local reproduction. Flower-size means, mating-system estimates, pollinator turnover, and occupancy alone do not identify \(F\) versus \(E\).

A high-ranked measurement is not automatically the best field protocol: feasibility, sampling variance, biological relevance, and cost still require an explicit design check.

The factorisation is a declared model choice. It does not claim that all natural processes are multiplicative or independent.

## Repository boundary

This is the active empirical design home for the Campanula/Izu channel-identification programme extracted from `microdonta`.

Nectar-guide mechanism models remain available as future design modules, but no unfinished guide dataset is part of the adopted empirical state.

## Relationship to RACH causal invariants

[`rach-causal-invariants`](https://github.com/zuizui0223/rach-causal-invariants) is the separate general-methods repository. It provides finite qualitative-program grammars, robust-admissibility classifications, coverage labels, and exact known-truth observation-channel calibration. It does not specify floral fitness, island geography, pollinator guilds, pollen deposition, recruitment, or any Campanula parameter.

This repository owns those biological assumptions: the \(F(z)E(z)\) factorisation, island-regime definitions, response-shape contracts, observation units, and field protocols. A predeclared subset may be translated into a RACH candidate universe to audit logical consequences; that translation is not empirical validation of a biological mechanism.
