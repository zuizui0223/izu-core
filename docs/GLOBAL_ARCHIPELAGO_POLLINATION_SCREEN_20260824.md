# Global archipelago pollination-state screen — 2026-08-24

## Decision

The programme is no longer limited to the original six qualitative island systems. A global screen now covers **39 archipelago/system units** and keeps them in four evidence tiers instead of forcing every island study into one ABM state.

- **Tier A — 9 strict qualitative state targets**: six protected parent targets plus three new external challenges.
- **Tier B — 15 partial mechanism/propagation systems**: direct evidence for support, effectiveness, dependency, replacement, morphology or reproduction, but a matched transition link is missing.
- **Tier C — 7 filtering/architecture systems**: useful for colonization, persistence, reproductive filtering or network architecture rather than within-system propagation.
- **Tier D — 8 screened gaps**: no source-comparable chain recovered in this pass; this is not evidence that relevant literature does not exist.

The machine-readable registry is `data/design/global_archipelago_pollination_screen_v1.json`.

## Three new strict external challenges

### Caribbean Gesneriaceae — `branches_downstream`

The existing source audit already combines three complementary levels within the same radiation. The 54-species island-mainland comparison reports lower hummingbird visitation on islands without a general island increase in autofertility, while generalized and bat-pollination states occur more often on islands. Independent Antillean experiments show pollen limitation in specialized lineages, no pollen limitation in four generalists, and autonomous assurance in some hummingbird specialists. Evolutionary reconstruction documents repeated transitions in pollination systems and floral form.

This is a strong **branching replication**, not a complete population-level causal bridge. Per-visit pollen effectiveness is still missing and the component studies must not be collapsed into one matched panel.

### New Zealand *Rhabdothamnus solandri* — `propagates_same_direction`

A natural experiment compares depleted mainland bird-pollination function with nearby offshore bird refugia. Reported pollen limitation is 0.69 on mainland sites versus 0.15 on island refugia, seed production per flower is reduced by 84% on the mainland, and demographic structure is poorer where bird function is lost.

This supplies an independent chain:

`bird functional loss -> pollen limitation -> seed-production decline -> demographic decline`.

It challenges the already-frozen same-sign capability; it does not identify the ABM trait-position mechanism.

### Mariana Guam-Saipan — `propagates_same_direction`

The brown treesnake natural experiment gives a second strong independent propagation chain. Bird visitation is high on Saipan and zero on Guam; seed set is significantly higher on Saipan in both *Bruguiera gymnorrhiza* and *Erythrina variegata*; *Bruguiera* seedling recruitment is also higher on Saipan.

This supplies:

`bird extirpation -> loss of bird visitation -> seed-set decline -> recruitment decline`.

The perturbation is specific to snake-driven bird loss and must not be relabelled as a generic isolation effect.

## Important systems that were not forced into Tier A

| Archipelago/system | Tier | Why it matters | Why not strict |
|---|---|---|---|
| Columbretes *Medicago citrina* | B | bees effectively absent; fly replacement; direct pollen limitation and visitor-efficiency experiments | no matched pre-loss or two-sided transition |
| Xisha *Cordia subcordata* | B | near-complete two-island bridge across morphology, visitation, effectiveness and dependency | direct effectiveness/dependency missing on Dong |
| Seychelles multi-plant | B | source-native single-visit reproductive outcomes and breeding treatments | no matched floral-response transition |
| Canary endemic systems | B | direct exclusion, pollen transport and vertebrate/insect function | no comparable archipelago transition |
| Réunion | B | pollinator dependence plus insular floral/pollination shifts | source links are not one matched transition |
| Giannutri | B | honeybee removal changes local resource/network context | plant reproductive endpoint not measured |
| Juan Fernández flora | C | >80% of studied cosexual endemics self-compatible; very rare insect visitation; wind/geitonogamy important | archipelago reproductive syndrome/filter, not a transition |
| Southern Ocean 11 island groups | C | 321-species compatibility/floral-type screen; biotic-pollination reliance constrains distribution | colonization/filtering layer |
| Pohnpei | C | community breeding-system evidence for reproductive assurance/Baker-law filtering | no paired pollinator-functional transition |
| New Caledonia | B | community pollination architecture and introduced-honeybee dominance | no matched loss-to-reproduction contrast |

## Geographic gaps retained explicitly

The current screen also records Aegean archipelagos, Rodrigues, Comoros/Aldabra, Ascension/Tristan da Cunha, Cook/Tonga, Solomon Islands, the Philippine archipelago and Indonesia/Wallacea as Tier D for this pass. These rows mean only that a **source-comparable frozen-state chain was not recovered** under the current screen. They are not negative biological results and should reopen only on a named source or a new prospective measurement route.

## What the nine-system v2 changes scientifically

The protected six-system v1 is unchanged. The new `system_agnostic_multi_system_validation_gate_v2.json` and `system_agnostic_abm_multi_system_validation_v2_frozen.json` apply the already-frozen synthetic capabilities to three external targets without running or retuning the ABM.

The qualitative replication structure becomes:

- branching: **Izu + Caribbean Gesneriaceae**;
- same-direction propagation: **Ogasawara + New Zealand + Mariana**;
- buffering/alternative states: **Hawaiʻi + Channel Islands**;
- reproductive-axis decoupling: **Puerto Rico-Mona Guaiacum**;
- protected falsification: **Dominica Heliconia**.

This is stronger than the original one-example-per-state layout, but it remains **state-class coverage**, not causal mechanism identification.

## What remains closed

1. No real system is yet admitted to the five-gate empirical network-context mapping contract (`matched transition + repeated local support + V_k + E_k + reproductive outcome`).
2. No common effect-size meta-analysis is licensed because estimands and hierarchies remain heterogeneous.
3. Tier B/C systems are not converted into pseudo-replicates simply because their qualitative story sounds compatible.
4. Dominica remains a failed frozen prediction; it is not retuned away.
5. The parent six-system frozen result remains immutable; expansion is versioned as v2.

## Search-frame boundary

The screen uses major oceanic/small-island archipelagos represented in island reproductive-biology reviews plus named searches across Macaronesia, the Mediterranean, Caribbean, eastern/central/western Pacific, southwest Pacific, Indian Ocean and Southern Ocean systems. It is deliberately broader than the prior repository screen, but it is not a literal census of every named island on Earth or every paper. Continental megarchipelagos are retained as explicit screened gaps when no comparable small-island transition was recovered.
