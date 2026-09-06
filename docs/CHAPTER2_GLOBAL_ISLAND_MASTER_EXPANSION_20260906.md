# Chapter 2 geography-independent global-island expansion

Updated: 2026-09-06

## Decision

The simulation layer is sufficiently structurally robust to stop using additional synthetic tuning as the main task. The empirical programme therefore returns to breadth **before** the final Izu zoom.

The previous 111-target search frame is retained as a completed search frame, but it is no longer treated as the outer boundary of world-island coverage. Its own audit already states that 111 is not the number of island systems on Earth. The next empirical phase instead begins from a geography source that was constructed independently of the Chapter 2 literature search.

## Independent geography anchor

A historical artifact in `zuizui0223/island` provides a Global Islands v3 / WCMC-USGS-derived island table:

- source repository: `zuizui0223/island`
- source commit: `f1462cd1aa76b2703bc2df159996a4ab65510a25`
- historical path: `legacy/v1/artifacts/data_global_islands/global_islands_over20km2.csv`
- blob: `42f31df81db250ebfe46b35ebce6cb1c52b19fc9`
- threshold: island polygons >= 20 km2
- candidate polygons: **4,663**

This table is a **geographic audit frame**, not 4,663 independent ecological systems. Individual polygons can be parts of one archipelago, names and plate labels contain historical-source artifacts, and the >=20 km2 threshold excludes many small islands. The correct use is therefore:

1. identify named geographies absent from the literature-built 111-target frame;
2. aggregate them into defensible island/archipelago systems;
3. search those systems under the same source gate;
4. keep source gaps visible;
5. only later decide whether any system adds manuscript value.

This breaks the circularity in which an island entered the universe only because a relevant paper had already been found.

## First master-gap tranche

The first tranche selected 20 conspicuous geographies absent verbatim from the 111-target frame. It deliberately includes major continental islands, Arctic/North Pacific systems and temperate South American systems that the earlier eight-macroregion frame undersampled.

The 20 systems are:

- California Channel Islands;
- Chiloé;
- Newfoundland;
- Spitsbergen / Svalbard;
- Hainan;
- Borneo;
- Sulawesi;
- New Guinea;
- Hokkaido;
- Tierra del Fuego;
- Mindanao;
- New Britain;
- Palawan;
- Kodiak;
- Flores;
- Halmahera;
- Bougainville;
- New Ireland;
- Buru;
- Shikotan.

All 20 now have a documented first review state in `chapter2_global_island_master_gap_wave1_20260906.csv` and `chapter2_global_island_master_gap_wave2_20260906.csv`.

## What the new systems add

### California Channel Islands — colonization filtering versus current selection

Schueller (2004), DOI `10.3732/ajb.91.5.672`, compares *Nicotiana glauca* on the California mainland with Santa Catalina and Santa Cruz Islands. The island populations had higher capacity for self-pollination, especially on the more recently colonized island, but island plants were not visited less frequently or more variably by hummingbirds and current selection for selfing was not detected.

This is a high-value **falsification/alternative-process** case. It blocks a shortcut from island selfing traits to present-day inferior pollinator service and instead supports establishment filtering/history as a plausible explanation. It does not provide the complete Chapter 2 transition-coordinate contract.

### Chiloé — community identity and reproductive output in the same comparison

Rovere et al. (2006), DOI `10.4067/S0716-078X2006000200008`, compared a coastal Chiloé population of *Embothrium coccineum* with an Andean Puerto Blest population. Both populations were strongly self-incompatible and pollinator dependent, but their visitor assemblages differed strongly. Chiloé was dominated by *Elaenia albiceps*, while Puerto Blest was dominated by *Sephanoides sephaniodes* with *Bombus dahlbomii*. Natural-pollination efficiency also differed.

This is unusually useful because realized community composition, controlled breeding treatments and reproductive output occur in one comparative study. It still lacks a documented historical partner-loss/arrival trajectory.

### Newfoundland — an explicit island prediction that fails

Thompson, Hermanutz & Innes (1998), DOI `10.1139/b98-059`, explicitly tested the expectation that island colonization and reduced pollinator diversity should favour breakdown of heterostyly toward self-compatible homostyly in *Menyanthes trifoliata*. The predicted selfing advantage was not recovered; tested populations remained highly self-incompatible and homostyly did not provide the expected advantage.

This is retained falsification, not a failed example to discard.

### Tierra del Fuego — local interaction disruption reaches fruit set

Traveset, Willson & Sabag (1998), DOI `10.1046/j.1365-2435.1998.00212.x`, directly measured flower visitation and nectar robbery in *Fuchsia magellanica* across habitats in western Tierra del Fuego. Effective hummingbird visitation was rare and spatially restricted; a nectar-robbing bird was abundant, and experimental/observational evidence linked robbery to an approximately 20% reduction in fruit set.

This adds a direct local-filtering / interaction-quality route to reproductive consequence. It is a high-value reality case but not a historical island-mainland transition.

### Process-rich systems without a transition series

Additional direct process evidence was recovered for:

- **Svalbard:** 43 populations of nine *Saxifraga* species; self-compatibility and spontaneous selfing quantified (`10.1006/bojl.2001.0450`);
- **Hainan:** visitor identity, breeding treatments and fruit set across three altitudes in endemic *Impatiens hainanensis* (`10.3724/SP.J.1003.2014.13243`);
- **Borneo:** floral biology, pollinator trapping and breeding systems in native *Goniothalamus* (`10.1038/srep35674`);
- **Sulawesi:** bee community composition, landscape/local filtering and experimental fruit set in 15 coffee agroforestry systems (`10.1046/j.1365-2664.2003.00847.x`); retained as process evidence rather than natural-island response evidence because it is an agricultural system;
- **New Guinea:** experimental fig-wasp transfers and reproductive isolation among six sympatric dioecious *Ficus* species (`10.1111/j.1558-5646.2012.01727.x`);
- **Hokkaido:** visitor observations and pollination experiments in a rare endemic plant (`10.1111/njb.04121`).

These systems enlarge process vocabulary but do not manufacture an island transition where none was measured.

## Explicit source gaps are part of the result

The geography-driven second wave did not recover qualifying local plant-response mechanism studies for every large island. Mindanao, New Britain, Palawan, Kodiak, Flores, Halmahera, Bougainville, New Ireland, Buru and Shikotan remain `initial_source_gap` or bounded-source states under the current search.

Examples of bounded evidence are retained without promotion:

- Flores has a recent expert-vouchered endemic-plant checklist, including 46 single-island endemic vascular plants, but not a pollination-process chain (`10.3897/phytokeys.273.184780`).
- Halmahera has local butterfly/food-plant and bee-forage inventories, but those do not establish pollination effectiveness and plant reproductive response (`10.30598/makila.v18i1.10634`).
- Mindanao has Rafflesia distribution and general carrion-fly pollination evidence, but no matched Mindanao-local effectiveness-to-reproduction primary study was admitted in this pass.

A geography remains in the review even when a strong mechanism paper is absent. That is the central difference from literature-first expansion.

## Combined 20-system measurement result

Across the first 20 geography-driven systems:

- primary-source-verified mechanism entries: **10/20**;
- direct plant response: **10/20**;
- direct breeding / assurance state: **9/20**;
- direct realized community shift or process contrast: **7/20**;
- direct local filtering: **2/20**;
- direct source functional state in the frozen Chapter 2 sense: **0/20**;
- direct partner loss: **0/20**;
- direct partner arrival/replacement: **0/20**;
- full Chapter 2 contracts: **0/20**.

This is the strongest current empirical diagnosis from the expansion. Geography-independent searching readily adds outcomes, breeding systems, visitor communities and local interaction effects. It does **not** readily add the historical turnover coordinates that were the strongest sign-stable regime drivers in the simulation.

Thus the process-measurement bottleneck survives a deliberately different sampling frame. That is more informative than simply adding more positive examples.

## Candidate value-review queue

Four systems currently merit a later, separate manuscript-value review:

1. California Channel Islands — very high falsification value;
2. Chiloé — direct community/reproductive comparison;
3. Newfoundland — explicit failed island-selfing prediction;
4. Tierra del Fuego — direct interaction disruption to fruit set.

They are **not yet added** to the active 42-entry / 37-label manuscript breadth. Promotion remains separate from discovery.

## Frozen boundaries remain unchanged

This expansion does not alter:

- active descriptive breadth: **42 research entries / 37 exact geographic labels**;
- frozen formal identifiability audit: **25 research entries / 21 exact labels**;
- frozen full contracts: **0/25**;
- formal external prediction: **`not_evaluable`**.

The 20 new geography states are a review layer, not a new validation denominator.

## Next scientific step

Do **not** zoom to Izu yet.

The next task is to extend the geography-independent master-gap queue beyond this first 20-system tranche, with special attention to:

- additional East and Southeast Asian large islands;
- North Pacific / Bering / Arctic systems;
- South American and sub-Antarctic systems not already nested in the Southern Ocean synthesis;
- source-native Japanese and Russian searches for the Kurils;
- small-island supplementation below the current >=20 km2 master threshold.

Only after this world confrontation stops adding materially new response/process/falsification states should Chapter 2 perform the final Izu mechanistic-resolution zoom.
