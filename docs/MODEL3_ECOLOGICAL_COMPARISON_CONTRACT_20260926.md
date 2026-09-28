# Model 3 ecological comparison contract

Date: 2026-09-26. Status: prospective design, not executed or frozen production parameters. Companion: `MODEL3_ISLAND_ECOLOGY_REDESIGN_20260926.md`. Preserve archived Model 3 at 4c4347e148197b43ddbb231931cd733b5f79f720. Q1 is motivation, never a fitting target. No target rank ordering or desired floral direction is an acceptance criterion.

## 1. Ecological questions and estimands

Primary question: when do changes in effective pollination produce reduced floral investment, through which reproductive pathway, and when do finite island populations fail to realize or reverse that response?

Second question: after an interruption or mismatch in effective pollination, do comparable islands return to comparable floral states, or retain differences because of establishment history, demographic loss and depleted variation?

Measure inherited resident change separately from replacement by immigrant descendants. Retain origin ancestry, realized selfing, population counts, allele frequencies, heterozygosity, trait variance, parentage and reproductive ledgers. Founder ancestry fraction is descriptive; it does not by itself identify a causal resident-only response after admixture. Record distributions and ancestry-stratified outcomes with their changing denominators.

For each declared island regime and horizon, report:

- occupancy probability and first-extinction time, plus recolonization events;
- probability of uninterrupted founder-lineage persistence, with ancestry definition explicit;
- survivor-conditional mean and distribution of trait change from its own initial state;
- signed individual-minus-density mean bias, mean absolute paired discrepancy and sign disagreement separately;
- genetic variation and reproductive return trajectories, not just terminal traits;
- recovery of demography and traits relative to the matched no-interruption counterfactual.

Never put a zero trait at extinction. For a contrast conditional on both arms surviving, report the number and identity of eligible pairs and both marginal survival probabilities. This survivor-selected contrast is descriptive, not the unconditional total causal effect. Occupancy and trait responses remain separate outcomes.

## 2. Mechanisms that require different counterfactuals

### Direct return on attraction

Fix autonomous assurance capacity, the distribution of plant genotypes, density and background floral resources in a standardized reproductive assay. Vary visitor activity/abundance separately from functional match and effectiveness. Change focal investment within admissible support and measure expected maternal and paternal allele contributions through the reproduction and inheritance operator.

Holding assurance capacity fixed does not hold realized selfing fixed: less outcross fertilization leaves more ovules eligible for delayed selfing. Therefore this assay estimates the total effect at fixed capacity, not automatically a non-selfing direct effect. For the narrow direct component, report the outcross ledger and its local response separately; compare an assurance-disabled assay at the identical census/genotypes without allowing demographic collapse first. That short assay is not a viable long-term ecological treatment in every regime.

The cost coefficient stays fixed when activity changes. Reduced return-to-cost is not increased physiological cost. Compare the declared allocation cost with zero-cost and alternative-cost diagnostic arms. A zero-cost arm is a mechanistic intervention, not a claim about natural flowers.

### Selfing-mediated response

Stage A uses fixed assurance capacities and records both raw and viable selfed offspring. Stage B adds a heritable assurance capacity, independently inherited from access and investment in its declared baseline. Do not impose a negative genetic correlation between selfing and investment to manufacture a syndrome. Genetic covariance and pollen/ovule discounting are explicit sensitivity structures, not silent defaults.

A fixed-versus-evolving assurance contrast measures the full feedback including abundance and altered selection. It is not a natural direct/indirect effect decomposition. Fixed depression tests a declared offspring viability penalty; claims about purging, evolving load or heterosis require a separate load model.

### Finite population response

Compare standardized selection assays at identical states, then trajectories allowed to change state. Identical visitor histories are not identical selection pressures once density, genotypes and mating opportunities differ. Within each visitor history use multiple independent demographic/inheritance realizations, with founder realizations crossed or held fixed as the estimand requires.

The currently observed attenuation is a property of the combined individual/density comparison, not yet attributable to drift. Mainland and island have equal finite capacities in existing pairs; add large-source/small-island contrasts before presenting the effect as specifically due to small island populations.

## 3. One-step finite-population benchmark

The archived `next_population` draws adult survivors, then Poisson potential recruits, caps retained recruits at available space, and samples parental pairs and Mendelian alleles. The density map instead caps expected births at space after expected survival. These are different operations.

For a fixed individual state containing n plants, capacity K, uniform survival s and total expected viable births Lambda:

- S ~ Binomial(n,s), B ~ Poisson(Lambda), independently under the archived operator;
- retained recruits R = min(B, K-S);
- E[R] = sum over j=0..n of P(S=j) E[min(B,K-j)];
- for integer v>=0, E[min(B,v)] = sum over b=0..v-1 of b P(B=b) + v P(B>=v).

Handle v=0 and Lambda=0 explicitly. Use stable probability/survival computations and analytic limits, not factorial overflow. Because the minimum is concave, E[R] <= min(Lambda, K-sn). Thus the deterministic cap can overpredict expected retained numbers even at identical current states. This inequality concerns counts, not the sign of trait bias.

Expected child genotype counts equal E[R] times the normalized parental-pair/Mendelian offspring distribution under the archived uniform thinning rule. Expected surviving genotype counts equal s times current counts. A normalized ratio of expected counts is NOT the expected trait mean conditional on survival. Derive that estimand separately or estimate it with explicit conditional Monte Carlo uncertainty.

This benchmark is exact only for the archived order of reproduction, survival and recruitment, uniform survival, and no added immigrant competition. Re-derive when the ecological operator changes. Iterating the one-step conditional expectation is not the expectation of the nonlinear stochastic trajectory.

## 4. Finite pollen exclusion contract

In the archived pollen matrix, donor pollen is allocated among recipient affinities plus background loss and the individual donor-recipient diagonal is then set to zero. This discarded dose is not redistributed. Same-genotype different individuals remain eligible outcross partners.

An exclusion diagnostic must preserve this denominator and loss contract. Simply setting the genotype-class diagonal to zero is wrong. Removing individual exclusion would permit within-individual pollen in the nominal outcross channel; treat that arm as an operator diagnostic, never as biologically valid outcrossing. The biologically interpreted finite model retains exclusion and explicit selfing.

Before any aggregate finite correction is used, reproduce individual-matrix totals exactly for tiny populations including identical genotypes, one plant, two plants, no visitors and multiple visitors. Include conservation of exported, received and discarded pollen.

## 5. Comparison hierarchy and interpretation

1. Archived ABM and archived density model: reproduce existing evidence without modifications.
2. Exact conditional one-step benchmark on the same finite state: quantify count truncation and offspring expectation without a trajectory closure claim.
3. Matched aggregate finite-state operator: only admitted after exact tiny-state pollen/inheritance checks; compare at fixed finite census.
4. Stochastic individual trajectories versus the declared large-population density operator: combined trajectory effect, with numerical refinement.
5. Optional controlled sampling diagnostics: census sampling and genotype sampling can be separated only after specifying consistent states and conditioning. Forced-census sampling is a diagnostic; it changes demography and is not a natural island population.

Do not sum endpoint differences between these levels as independent additive causal contributions. Report interactions and order dependence where sequential replacements differ. Demographic stochasticity and genetic drift emerge from overlapping reproductive events; their partition depends on the intervention definition.

Grid convergence must be established separately for the genotype density approximation. Capacity scaling holds initial density, resource density, mutation per gamete and declared per-capita migration fixed; a separate fixed-total-arrival series asks the ecological island-size question. Do not confuse these two large-K limits. External visitor fluctuations persist in the conditional density model.

## 6. Arrival, loss and mismatch experiments

Two experiment families are necessary:

**Controlled temporal interventions:** replay the same visitor states/identities in different predeclared orders, keeping duration and total exposure fixed where possible and adding a common final recovery segment. This isolates ordering conditional on the schedule multiset. Identity and trait composition must be retained; matching richness alone is insufficient. Differences in delivered pollen caused by evolved plant state are outcomes, not quantities to forcibly equalize.

**Ecological assembly:** independently model seed arrival, visitor arrival, establishment, local loss and resource support along a connectivity gradient. Histories generated by this process need not share total exposure. These test bundled ecological consequences; do not label them pure order effects.

Oceanic founding and continental separation use distinct initialization processes, with matched present conditions and observation time since the relevant event. Include matched-initial-state controls to distinguish history from simply assigning different founder diversity. Avoid geological labels for arbitrary initial states: provide what is inherited, what arrives, what disappears, and what continues to connect.

Visitor establishment presupposes sufficient background floral resources or explicitly depends on available resources. No unexplained permanent pollinator community on a plant-empty island. Background support is fixed or independently manipulated; the focal-plant model is not whole-island coevolution.

Recovery interventions separate effective visitor restoration, seed immigration and mutation. Seed immigration supplies both individuals and alleles: use demographic-match controls (immigrants drawn from current resident genotype distribution where defined) alongside source-genotype immigrants, with no-resident cases handled separately. These are counterfactual diagnostics, not naturally identical immigrants. Track replacement so apparent recovery is not automatically called adaptation of the original lineage.

## 7. Time, replication and transfer

Time is reproductive years; generation time is derived from the age/parentage process, not equated with years for overlapping generations. Compare interruption and recovery durations against both realized generation time and visitor autocorrelation. Initial selection direction is insufficient evidence for long-term convergence or recovery.

Mutation/immigration replenishment must be explicit in long-term campaigns. Acceleration requires preservation or derivation of the relevant relative rates; increasing mutation to save runtime is a different biological regime unless a justified scaling is established. A PDE is optional, and only named after deriving the relevant continuous-time/trait limit. The valid first counterpart remains the discrete sexual-inheritance operator.

Prospective production design must freeze meaningful effect thresholds, supported trait range, numerical error tolerance, horizons, independent seeds and endpoint precision before inspecting production results. Use a disjoint pilot for execution cost and operator verification. Do not select only trajectories where deterministic approximation fails. A uniform or predeclared space-filling regime sample estimates generality; boundary-enriched samples estimate local mechanism and have separate weights.

S/C/I analyses cross plant starting states and visitor histories with repeated within-cell demographic/inheritance/mutation draws. Report within-cell variation separately. Visitor and seed-arrival histories can form distinct factors if crossed; combining them into C requires declaring the joint distribution. Partition occupancy and trait estimands separately. Rank transport is evaluated on held-out regimes with fixed factor ranges/weights and uncertainty, not by transferring an old C-I-S narrative.

## 8. Acceptance evidence for implementation planning

Required implementation tests: archived result replay; no-arrival/no-mutation limits; empty-island recolonization; pollen and allele conservation; exact one-step expectation versus enumeration; forced-state assays with unchanged genotypes; distinct initial-state and visitor random streams; chronology replay; ancestry accounting; failure on unsupported biological units; grid refinement; and report denominators retaining extinct cases.

Before production, implementation must produce a machine-readable manifest specifying all mechanisms, units, sampling arms, random streams, sources, hashes, expected case counts and unimplemented claim boundaries. Planned test names and commands belong in the file-level implementation plan. This contract specifies scientific correctness; it is not evidence those tests have run.
