# Island ecology manuscript reference map

Updated: 2026-08-24

This file separates **conceptual positioning references** from the **source-locked 13-system external challenge**. It is an editorial map for the ecology-first manuscript; it does not create new evidence or change any external-system state assignment.

## A. Main-text conceptual references

### A1. Island reproductive filtering and island syndromes

Use these references to motivate the distinction between colonization/persistence filtering and post-establishment response.

- Grossenbacher, D.L. et al. (2017). **Self-compatibility is over-represented on islands.** *New Phytologist* 215:469–478. DOI `10.1111/nph.14534`.
  - Manuscript role: direct support for breeding system as an island colonization/filtering axis.
  - Use in: Introduction paragraph 1; Discussion 4.1.

- Zell, A.N., Miranda, C.H., Grady, E.L., Grossenbacher, D.L. & Igić, B. (2025). **Island colonization in flowering plants is determined by the interplay of breeding system, lifespan, floral symmetry, and arrival opportunity.** *New Phytologist* 245:420–432. DOI `10.1111/nph.20234`.
  - Manuscript role: global evidence that island occurrence reflects breeding system, lifespan, floral traits and arrival opportunity rather than a single post-establishment response.
  - Use in: Introduction paragraph 1; Discussion 4.1.

- Whittaker, R.J., Fernández-Palacios, J.M. & Matthews, T.J. (2023). **Island evolutionary syndromes in—and involving—plants.** In *Island Biogeography: Geo-environmental Dynamics, Ecology, Evolution, Human Impact, and Conservation*, pp. 283–308. Oxford University Press. DOI `10.1093/oso/9780198868569.003.0011`.
  - Manuscript role: synthesis of proposed island plant syndromes and plant–animal interaction shifts.
  - Use in: Introduction paragraph 1; Discussion 4.1.

- Traveset, A. & Navarro, L. (2018). **Plant reproductive ecology and evolution in the Mediterranean islands: state of the art.** *Plant Biology* 20(Suppl. 1):63–77. DOI `10.1111/plb.12636`.
  - Manuscript role: background for heterogeneity in island reproductive ecology and the danger of treating all island lineages as one trajectory.
  - Use in: Introduction paragraphs 1–2; Discussion 4.1.

### A2. Network context, rewiring and resilience

Use these references to motivate H3 without implying that rewiring is universally protective.

- Bascompte, J. & Scheffer, M. (2023). **The Resilience of Plant–Pollinator Networks.** *Annual Review of Entomology* 68:363–380. DOI `10.1146/annurev-ento-120120-102424`.
  - Manuscript role: network resilience, rewiring, heterogeneity and interaction-level responses to perturbation.
  - Use in: Introduction paragraph 2–3; Discussion 4.3.

- Marjakangas, E.-L., Dalsgaard, B. & Ordonez, A. (2025). **Fundamental Interaction Niches: Towards a Functional Understanding of Ecological Networks' Resilience.** *Ecology Letters* 28:e70146. DOI `10.1111/ele.70146`.
  - Manuscript role: functional interaction-space framing; supports the idea that realized partner identity can change while functional opportunity is redistributed.
  - Use in: Introduction paragraph 2–3; Discussion 4.3.

### A3. ABM / inference references — supporting only

These references are method support and should not lead the ecology-first Introduction.

- Grimm, V. et al. (2005). **Pattern-oriented modeling of agent-based complex systems: lessons from ecology.** *Science* 310:987–991. DOI `10.1126/science.1116681`.
- Grimm, V. & Railsback, S.F. (2012). **Pattern-oriented modelling: a ‘multi-scope’ for predictive systems ecology.** *Philosophical Transactions of the Royal Society B* 367:298–310. DOI `10.1098/rstb.2011.0180`.

Use only in Methods/inference-boundary text if needed. State-separability is not the biological headline.

## B. Strict external island-system challenge — source locked

The authoritative state assignments remain in `data/design/simulation_manuscript_external_system_reference_matrix.json`. The sources below support **observed-state assignment only**. They are not parameter-fitting inputs and do not identify a shared empirical mechanism.

### Branching — 3 systems

1. **Izu multi-taxon Hiraiwa–Ushimaru**
   - Hiraiwa & Ushimaru (2024), DOI `10.1111/1365-2435.14527`.
   - Hiraiwa & Ushimaru (2017), DOI `10.1098/rspb.2016.2218`.
   - Boundary: cross-study response heterogeneity, not same-estimand replication.

2. **Caribbean Gesneriaceae**
   - Martén-Rodríguez et al. (2015), DOI `10.1111/1365-2745.12457`.
   - Martén-Rodríguez & Fenster (2010), DOI `10.1890/08-2115.1`.
   - Martén-Rodríguez et al. (2010), DOI `10.1111/j.1469-8137.2010.03330.x`.
   - Boundary: clade-level recurrence; not one matched population-level causal chain.

3. **Canary Islands / Teide managed-honeybee network**
   - Valido, Rodríguez-Rodríguez & Jordano (2019), DOI `10.1038/s41598-019-41271-5`.
   - Boundary: common network perturbation with plant-specific reproductive responses; do not transport the honeybee mechanism to other systems.

### Same-direction propagation — 6 systems

4. **Ogasawara Psychotria homalosperma**
   - Watanabe et al. (2018), DOI `10.1111/1442-1984.12183`.
   - Watanabe & Sugawara (2015), DOI `10.1093/aobpla/plv087`.
   - Watanabe et al. (2014), DOI `10.1016/j.flora.2014.09.006`.
   - Boundary: qualitative access/pollen-transfer propagation; not randomized historical replacement.

5. **New Zealand Rhabdothamnus solandri**
   - Anderson et al. (2011), DOI `10.1126/science.1199092`.
   - Boundary: bird functional-loss natural experiment; not a numerical fit of the synthetic trait-position mechanism.

6. **Mariana Guam–Saipan bird loss**
   - Mortensen, Dupont & Olesen (2008), DOI `10.1016/j.biocon.2008.06.014`.
   - Boundary: snake-driven bird-extirpation natural experiment; not a universal isolation mechanism.

7. **Seychelles invasive-ant disruption**
   - *Global Ecology and Conservation* (2023), DOI `10.1016/j.gecco.2023.e02413`.
   - Boundary: within-island propagation experiment; not a unique ABM mechanism.

8. **Mauritius Roussea simplex invasive-ant disruption**
   - Hansen & Müller (2009), DOI `10.1111/j.1744-7429.2008.00473.x`.
   - Boundary: ant interference → gecko access/visitation → reproduction; not a universal invasive-ant effect.

9. **Bahamas Pavonia bahamensis after hurricane-associated pollinator loss**
   - Rathcke (2000), DOI `10.1890/0012-9658(2000)081[1951:HCRAPL]2.0.CO;2`.
   - Boundary: source also identifies direct resource limitation; strict propagation state concerns the additional pollination-limitation component.

### Buffering / alternative — 2 systems

10. **Hawaiian lobelioids after bird extinction**
    - Case et al. (2026), DOI `10.1111/1365-2435.70415`.
    - Case et al. (2026), DOI `10.1002/ece3.74123`.
    - Boundary: high reproductive performance can coexist with altered interaction/mismatch context; no empirically identified ABM buffer mechanism.

11. **California Channel Islands Nicotiana glauca**
    - Schueller (2004), DOI `10.3732/ajb.91.5.672`.
    - Schueller (2007), DOI `10.1007/s10682-006-9125-9`.
    - Boundary: autonomous selfing capacity and morphology differ while a current service deficit was not established; historical/establishment alternatives remain open.

### Protected constraint and falsification

12. **Puerto Rico–Mona Guaiacum sanctum — reproductive-axis decoupling**
    - Fumero-Cabán, Meléndez-Ackerman & Rojas-Sandoval (2022), DOI `10.26786/1920-7603(2022)669`.
    - Boundary: visitor context differs strongly while the self/outcross seed-set index remains similar; do not collapse all reproductive axes into one buffering label.

13. **Dominica Heliconia — retained falsification**
    - Temeles et al. (2013), DOI `10.1111/jeb.12053`.
    - Martén-Rodríguez et al. (2011), DOI `10.1007/s00442-011-2043-8`.
    - Boundary: the frozen signed-position prediction failed and remains unretuned.

## C. Main-text citation strategy

Keep the main manuscript readable rather than placing every source in every paragraph.

- **Introduction / syndrome-filtering distinction:** Grossenbacher 2017; Traveset & Navarro 2018; Whittaker et al. 2023; Zell et al. 2025.
- **Introduction / interaction-context rationale:** Bascompte & Scheffer 2023; Marjakangas et al. 2025.
- **Results H5:** cite representative source(s) at the end of each response-state group, while Table 2 / Supplement carries the full 13-system source matrix.
- **Discussion 4.1:** Grossenbacher 2017; Zell et al. 2025; Whittaker et al. 2023.
- **Discussion 4.3:** Bascompte & Scheffer 2023; Marjakangas et al. 2025.
- **Discussion 4.4:** refer readers to Table 2 / Supplement for all 13 source-locked systems rather than implying a pooled meta-analysis.
- **Inference boundary:** Grimm et al. 2005 and Grimm & Railsback 2012 are optional supporting method citations, not the ecological frame.

## D. Reference integrity rules

- Do not cite a system as evidence for an empirical mechanism stronger than its source-locked state assignment.
- Do not cite the 13-system challenge as a prevalence estimate.
- Do not add a source to the strict challenge merely because it supports the manuscript narrative.
- Do not replace a source-locked DOI with a secondary review when the primary source is available.
- Any new conceptual reference may sharpen framing but cannot alter H1–H5, frozen numbers, state counts or protected failures.
