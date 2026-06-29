# Campanula Channel Identification

A field-design, causal-identification, and constrained-simulation repository for asking a deliberately narrow question about island floral-trait variation:

\[
W(z)=F(z)E(z).
\]

For a predeclared trait \(z\), can a difference between island regimes be assigned to

- **local reproduction** \(F(z)\), or
- **establishment / reachability conditional on viable seed output** \(E(z)\),

rather than merely described as a difference in flower size, selfing, or visitor identity?

## What this repository does

- records the minimum theorem-compatible measurement design for the factorisation above;
- distinguishes direct measurements from proxies whose calibration must be stable or independently checked;
- keeps published patterns, prospective field measurements, and pollinator-specific claims separate;
- provides a lightweight readiness checker for a proposed sampling design;
- separately checks whether a proposed nectar-guide comparison is still association-only because of site, display, nectar, plant-condition, or time confounding;
- provides a constrained life-history simulation layer for comparing explicitly declared mechanisms against predeclared observation intervals;
- ranks proposed future measurements by how strongly they distinguish the parameter candidates still compatible with current observations;
- provides a nectar-guide mechanism model that separates guide effects on visitation, legitimate handling/pollen placement, and guide-expression cost;
- allows restricted compound guide routes, such as visit attraction plus delayed-selfing assurance, rather than forcing all mechanisms into mutually exclusive named scenarios;
- extends that model, in explicit layers, to paternal success, pollinator guilds, late inbreeding depression, temporal variation, genetic-versus-plastic expression, and spatial recruitment;
- tests finite-sample operating characteristics: simultaneous-interval coverage, virtual-truth retention, unique recovery, empty compatible sets, and residual ambiguity;
- provides an optional density-dependent establishment response for seed-addition or cohort-follow-up designs.

The simulation layer does not estimate an unobserved cost from a trait alone. It retains the **set of parameter values compatible with all declared observations**, then makes the remaining uncertainty explicit. The measurement-ranking layer identifies which proposed observable would split that remaining set most strongly at a predeclared assay resolution. The guide-evolution layers specify which intermediate observation is needed before a proposed evolutionary mechanism can be used in a field-facing claim. The scenario-recovery layer asks whether those observations actually discriminate competing mechanisms before field data are collected. See [the simulation specification](docs/constrained_life_history_simulation.md), [the measurement-ranking specification](docs/discriminating_measurements.md), [the nectar-guide mechanism model](docs/nectar_guide_mechanism_model.md), [the full six-layer guide-evolution model](docs/guide_evolution_model.md), [the scenario recovery workflow](docs/guide_scenario_recovery.md), and [the pre-data robustness protocol](docs/robustness_protocol.md).

## Guide-evolution layers

```text
1. maternal + paternal genetic contribution
2. guild-resolved visit, handling, deposition, and export
3. late inbreeding depression after seed set
4. temporal fitness and geometric mean performance
5. genetic guide baseline versus plastic expression
6. spatial dispersal, establishment, and capacity-limited recruitment
```

These layers are deliberately modular. Do not activate a layer merely because it exists: activate it only when its required intermediate quantity is measured or has a defensible calibration.

## Competing scenario workflow

```text
M0 null guide
M1 guide → visits
M2 guide → handling / pollen placement
M3 guide-expression cost
M4 assurance compensation
M5 visit and/or handling + assurance or cost
M6 paternal export and siring
M7 spatial establishment
M8 fully mixed
```

A coarse terminal outcome such as recruit number should generally leave several scenarios compatible. The model becomes useful when intermediate measurements—guild-resolved visits, contact/pollen deposition, cross type, paternity, or patch recruitment—reduce that compatible set. A candidate set must include plausible compound routes; otherwise the correct result may be an empty set rather than an honest statement of ambiguity.

## What it does not claim

A visit count is not automatically a measurement of local reproduction. Likewise, flower-size means, selfing rates, and pollinator turnover alone do not identify \(F\) versus \(E\).

A successful simulated reconstruction is not proof that its mechanism generated the field pattern. It is only a compatibility result conditional on a declared life cycle, parameter ranges, measurement intervals, and observation model.

A high-ranked measurement is not automatically the best field protocol: its feasibility, sampling variance, biological relevance, and cost still require an explicit field-design check.

A positive nectar-guide relative-performance contrast is not itself evidence that guides evolved by that mechanism. It must be paired with heritable or otherwise genetically grounded guide variation, a measured intermediate pathway, and comparison against selfing compensation and E-stage explanations.

The factorisation is a declared model choice. It does not claim that all natural processes are multiplicative or independent.

## Repository boundary

This is the active empirical design home for the Campanula/Izu channel-identification program extracted from `microdonta`.

The model architecture can now represent the major routes by which nectar-guide variation could affect long-term genetic contribution. It does **not** make those routes identifiable without data: every guide-evolution claim still requires a declared life cycle, a common census scale, measured intermediates, a competing-model comparison, and an operating-characteristic check under the planned field observation model.
