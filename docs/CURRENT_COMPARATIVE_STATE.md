# Current comparative island evidence state

Updated: 2026-08-23

## Programme question

The inferential unit is the **independent island system**, not Izu or any one focal taxon.

> Across independent island systems, which upstream pollinator-functional changes recur, which downstream response branches follow, and what determines whether those changes propagate into reproductive or floral evolutionary response?

Izu/*Campanula* remains a prepared mechanistic anchor. Missing Issue #91 field rows do **not** block the programme.

## Current state vocabulary

The programme now keeps five logically distinct outcomes rather than forcing every system into one island syndrome:

- **same-direction propagation**;
- **downstream branching**;
- **buffering / alternative mechanism**;
- **counterdirectional / failed prediction**;
- **reproductive-axis decoupling**, where one reproductive index is stable while another realized reproductive outcome changes.

Missing and adjacent links remain explicit rather than being encoded as zero.

## Clearest empirical contrasts

- **Ogasawara *Psychotria homalosperma*** — current physical access failure at the hidden S-morph stigma aligns with directional pollen transfer and strong morph-specific field fruit asymmetry: bounded `propagates_same_direction` case.
- **Hawaiian lobelioids 2026** — signed bill–flower mismatch predicts pollen contact / nectar robbing, while fruit and seed performance remain high in a closely overlapping contemporary study: genuine buffering boundary, mechanism not yet identified.
- **California Channel Islands *Nicotiana glauca*** — greater autonomous selfing / trait differences coexist with no detected current island service deficit: buffering/alternative-history case, with establishment filtering and assurance both live.
- **Izu multi-taxon panel** — broadly lower corrected matching coexists with divergent pollen and tube responses: `branches_downstream`.
- **Dominica *Heliconia*** — the first frozen signed-position direction prediction failed: `counterdirectional`; no rescue retuning.
- **Puerto Rico–Mona *Guaiacum sanctum*** — strong visitor-assemblage contrast and similar self/outcross seed-set ISI coexist with negligible autogamy, but Mona open reproduction is pollen-limited relative to outcross and realized multiplicative fitness is lower: `reproductive_axes_decouple`, **not** whole-reproduction buffering.

The Guaiacum correction is frozen in `data/results/guaiacum_propagation_state_correction.json`.

## Why the Guaiacum correction matters

The previous shorthand treated similar ISI (`0.60` versus `0.63`, P = 0.77) as a buffered reproductive response. That was too broad.

ISI is a **selfing/outcrossing seed-set ratio**. It is not total reproductive dependency and not realized open reproductive performance. The same source reports negligible autogamy, pollen limitation on Mona under open pollination relative to supplemental outcross, and lower Mona multiplicative fitness for open/outcross progeny.

Therefore:

```text
stable breeding-system index
!=
stable realized reproduction
```

Guaiacum is retained as a valuable **visitor-composition -> effective-service mapping reference**, not as a demonstrated reproductive buffer.

## ABM mechanism state

The falsification-driven ABM ladder now separates four synthetic roles.

### 1. Branch generator: pre-existing lineage position

v12 identifies pre-existing lineage position in functional trait space as the minimal generator of same-environment, within-run sign branching in the declared ABM. Removing initial trait heterogeneity collapses within-run two-sided branching.

This is a synthetic mechanism result. The frozen Dominica projection shows that a simple signed-position direction rule does not transfer universally to real systems.

### 2. Network context / local support: replicated buffering-capable branch allocator

With autonomous assurance set to zero, local support ON versus OFF was tested on matched global opportunity networks.

Initial frozen block:

- support-OFF reproductive declines: 89;
- sign rescues: **2/89**;
- magnitude rescues: 52/89;
- worsening: 37/89.

Independent frozen block:

- support-OFF reproductive declines: 96;
- sign rescues: **16/96**;
- magnitude rescues: 85/96;
- worsening: 11/96.

Thus network context has a **replicated synthetic sign-buffering capability**, but the same mechanism can worsen outcomes. It is best interpreted as a context-dependent branch allocator with buffering capacity, not a universal protective process.

Results: `data/results/network_context_buffering_capability_ablation_frozen.json` and `data/results/network_context_buffering_capability_robustness_frozen.json`.

### 3. Autonomous assurance: robust weak attenuation, non-robust sign rescue

The initial v14 block contained one sign rescue among 202 service-decline contrasts. That event did not replicate:

- independent exact-design block: **0/216** sign rescues, 207 magnitude rescues;
- broader support envelope: **0/525** sign rescues, 510 attenuations.

Therefore the stable synthetic property of the current assurance route is **magnitude attenuation**, not reliable sign-level buffering. The initial 1/202 event remains recorded rather than erased.

### 4. Partner effectiveness: branch-identity modifier

v10 shows partner effectiveness changes individual branch identity, but it does not generate the aggregate two-sided branching distribution by itself.

## Empirical mechanism admission remains closed

Synthetic capability is not empirical mechanism identification.

The common admission interface is frozen at `data/design/buffer_mechanism_abm_admission_interface.json`.

Current demonstrated buffer-candidate portfolio:

- Hawaiʻi lobelioids — autonomous assurance is an exact-taxon historical candidate for *Clermontia lindseyana* and *C. pyrularia*, but no same-context numeric dependency mapping exists;
- *Nicotiana glauca* — assurance / establishment-filter candidates are source-supported, but the strongest links are not one same-season matched transition.

Both remain `candidate_only_no_abm_admission`; mapping-ready = 0, empirically admitted = 0.

Guaiacum has been removed from this portfolio and is retained separately as a service-mapping / axis-decoupling reference.

## Frozen empirical network-context prediction

The key empirical quantity is now predeclared as:

```text
rate-weighted effective service
= sum_k(visit rate_k x direct per-visit effectiveness_k)
```

A real network-context/service-redundancy buffer requires composition or global opportunity change **plus** maintained/rescued rate-weighted effective service and maintained reproduction. Visitor richness, occurrence or visitation alone do not establish redundancy.

If direct effective service is still reduced while reproduction remains high, the explanation must move downstream to assurance, resource/demographic compensation or another measured filter.

The prediction contract is frozen in `data/design/network_context_empirical_prediction_freeze.json`.

For Guaiacum, `data/design/guaiacum_network_context_mapping_preflight.json` freezes the required visitor-specific rate × effectiveness mapping without inventing missing effectiveness values.

## Current proof ladder

| Claim | Current status |
|---|---|
| Island plant responses are not universally directional | empirically supported |
| Common-ish upstream functional change can coexist with downstream branching | empirical Izu pattern + synthetic support |
| Pre-existing lineage state can generate same-environment branch signs | identified inside declared ABM |
| Network context can produce strong sign-level buffering | replicated synthetic capability, bidirectional |
| Autonomous assurance reliably produces sign-level buffering | **not supported**; attenuation is robust, sign rescue is not |
| A real island system is empirically mapped to the synthetic network-buffer route | **not yet** |
| Guaiacum is a whole-reproduction buffer case | **rejected/corrected** |
| Dominica validates the frozen signed-position direction | **rejected** |
| One universal island buffer mechanism is identified | **no** |

## Next admissible work

1. Keep the empirical network-context prediction and mechanism-admission rules frozen.
2. Seek or prospectively measure visitor-specific **visit rate × direct per-visit effectiveness** in an existing system before assigning the synthetic network-buffer route to it.
3. Use Guaiacum as a service-mapping reference, not as a buffered-outcome proof.
4. Keep Hawaiʻi and Nicotiana as true buffer/alternative-mechanism candidates until a matched mapping becomes available.
5. Continue Issue #91 in parallel when real data arrive; it is one direct calibration route, not a programme prerequisite.
6. Do not tune support strength, assurance parameters or seed blocks to known island outcomes.

## Claim boundary

Do not infer a universal island response, do not pool noncommensurate response axes into one coefficient, and do not treat a stable breeding-system index as stable realized reproduction. Synthetic ABM state-class reproduction is weaker than empirical mechanism identification. Dominica remains failed; Guaiacum remains axis-decoupled; Hawaiʻi/Nicotiana remain empirically unmapped buffer candidates.
