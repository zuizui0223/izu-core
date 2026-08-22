# ABM v12 empirical candidate: Eastern Caribbean Heliconia

## Current decision

`admit_heliconia_as_next_v12_source_candidate_but_keep_target_closed_until_raw_bytes_and_visit_weights_are_locked`

This system is valuable because it contains, within one ecological programme:

- plant corolla length in millimetres;
- a strongly dimorphic hummingbird pollinator functional axis;
- pollinator sex-specific visitation;
- plant-level seed fitness;
- repeated populations and years;
- prior independent floral-pollinator morphology measurements that can define the mapping without using the later seed-selection outcome.

It is **not** literature-blind: the 2013 paper's qualitative selection results are already known. The prospective contribution is therefore restricted to a newly frozen exact derived-statistic test using raw plant-level data, not a claim of fully held-out discovery.

## Selection dataset

Temeles et al. 2013, Journal of Evolutionary Biology, DOI `10.1111/jeb.12053`.

Dryad: `10.5061/dryad.64835`.

The public dataset lists three plant-level XLS files:

- *Heliconia bihai* floral-trait and seed-set data;
- *H. caribaea* red-morph data;
- *H. caribaea* yellow-morph floral-trait and seed-set data.

The paper reports 30-40 focal plants per site, mean corolla length from 5-10 flowers per plant, seed set per plant, and 12 h/site pollinator observations with hummingbird species and sex recorded.

The current execution environment can see the Dryad landing metadata but could not retrieve the individual XLS bytes. Therefore no new plant-level target is calculated yet.

## Independent mapping source

Martén-Rodríguez et al. 2011, Oecologia, DOI `10.1007/s00442-011-2043-8`.

For Dominica it reports:

- female *Eulampis jugularis* bill length: `26.6 ± 0.12 mm`;
- male bill length: `19.8 ± 0.36 mm`;
- female-associated *H. bihai* corolla: `47.8 ± 0.43 mm`;
- male-associated *H. caribaea* corolla: `35.8 ± 0.22 mm`.

The two source-native ecological anchors define, before any new seed-fitness calculation:

```text
expected corolla (mm)
  = 0.8588235294 + 1.7647058824 × pollinator bill center (mm)
```

This line is a **Dominica two-anchor calibration**, not a universal flower-bill geometry law.

## Signed-position test to open only after source recovery

For a population × year × morph:

1. derive the pollinator bill center from source-native sex-specific visitation weights;
2. map that bill center to expected corolla length using the frozen 2011 calibration;
3. define signed position as

```text
plant mean corolla - expected corolla
```

4. then, and only then, test whether signed position predicts the direction or magnitude of female-fitness selection on corolla length using source-native seeds per plant.

If sex-specific visitation weights for a population/year cannot be recovered, that unit is withheld. The flower phenotype cannot be used to choose the pollinator sex after the fact.

## Why this is a strong discriminator

The v12 ABM predicts that initial position in a functional matching space can create divergent response branches under a common environmental shift. *Heliconia* provides multiple co-occurring lineages/morphs whose floral traits correspond to male/female pollinator morphology but whose natural selection on corolla length differs among lineages and contexts.

A frozen signed-position test can therefore fail in informative ways:

- no relation between signed position and corolla selection;
- relation only in the specialized *H. bihai* branch;
- relation disappears when pollinator visitation mixture is represented;
- seed fitness is better explained by another plant axis such as bract number.

Any of these outcomes would refine or falsify the current v12 interpretation rather than trigger parameter tuning.

## Boundary

Do not use the published 2013 selection-gradient signs to modify the mapping. Do not infer missing visit weights from flower morphology. Do not call this a universal optimum or a fully held-out validation. Raw selection bytes and the visit-weight schema must be recovered and locked first.
