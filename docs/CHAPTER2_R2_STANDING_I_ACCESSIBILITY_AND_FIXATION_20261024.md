# R2: a negative expected-I direction does not guarantee that the lowest available I allele fixes

**2026-10-24 — source-authenticated, retrospective Model 3 result. No new independent biological histories or prospective frequency-threshold test.** This follows source-exact original-genome replays #633 and #634. The registered R1–R5 results, R4 G/S and independently founded R2 four-setting overall **INCONCLUSIVE** judgment remain unchanged.

## Question

In the original 384-path pollen factorial, A (reproductive assurance) and M (plant–pollinator matching) were already monomorphic at census 30 in **24 paired source populations**, while floral-investment trait I still had standing diploid allele variation. In **22/24** with strong prior pollen limitation, the imposed decline in visitor activity generated an **extra negative expected one-generation I shift** in *every one* of the genetically authenticated source states (source result #633). After the **original** 50 subsequent updates, all 22 visitor-decline populations had fixed I (source result #632). How often did each population fix the **lowest I allele value available at the shock**, rather than a higher inherited value?

This asks about **genetic availability, fixation and contingency** within the previously studied finite model. It does not assume that a negative source conditional expectation makes eventual fixation of the lowest allele certain.

## Exact native and original ZIP readback

Two mutually independent technical access paths now check the same 22 source cases:

- **Original external Actions source ZIP**: run [39233450099](https://github.com/zuizui0223/izu-core/actions/runs/39233450099), artifact **12178257738**, original ZIP SHA256 `10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e`. The raw reader first validates all 384 source trajectories, original ZIP/internal file digests, original matched-future identities, and the exact census30 A/M-fixed subset.
- **Independent native-genome technical replay without the ZIP**: original source founder/visitor seeds and original Model 3 are admitted against frozen kernel/protocol SHA checks. Each of the same 22 original source pairs replays the original 30-update prefix and both original 50-update futures; it requires exact matches to **each of 22 census30 and 44 terminal full-genome SHA fingerprints** retained in the original ZIP-derived immutable roster (blob SHA `6b04ee9a5cd6c2342e397c6c69539688474b391f`). No new independent population or alternative biological parameters are introduced.

The original census30 genotype contains 48 diploid plants, hence **96 I allele copies per source**. For each paired source, the reported quantity is the **minimum numerical I allele value actually present** at census30, together with that allele's source copy count and the terminal monomorphic I value in each future.

## Original-source result: accessibility and exceptions

| Original A start | Strong-pollen source pairs | Decline futures fixed to the lowest accessible I value | Decline futures fixed to a higher accessible value |
|---:|---:|---:|---:|
| 0.3 | 16 | **15** | 1 |
| 0.5 | 6 | **5** | 1 |
| **Total** | **22** | **20** | **2** |

The 22 visitor-decline fixed-I values are **I=0.25 (9), I=0.50 (12), I=0.75 (1)**. These are *different reachable minima depending on which alleles survived the original 30-update prehistory*. For instance, sources whose lowest surviving allele is I=0.5 **cannot** reach I=0.25 afterward in the frozen no-mutation/no-immigration source. A single preferred destination across all founder genomes is therefore neither observed nor genetically accessible.

In the **two cases that did not fix the lowest available I**, that lower allele was especially uncommon at the moment of treatment:

| Original source | Starting A | Census30 I allele values (diploid copy counts) | Fixed I after decline | Matched control final I |
|---|---:|---|---:|---:|
| Founder 810102 / demographic repeat 4 | 0.3 | **0.50: 6/96**, 0.75: 90/96 | **0.75** | 0.75 |
| Founder 810110 / demographic repeat 3 | 0.5 | **0.25: 4/96**, 0.50: 92/96 | **0.50** | 0.50 |

In both exceptions, the source-authenticated *one-generation genetic parental expectation* at the identical census30 state **still favored lower I under the imposed visitor decline** relative to control (differences **−0.00114437** and **−0.00077062**, respectively; archived original full-genome source readback, Actions [run 39929844856](https://github.com/zuizui0223/izu-core/actions/runs/39929844856)). Yet the lower I allele was eventually lost in *both* source futures, producing an **exactly zero final I treatment contrast**. These are real cases of **directional conditional expectation without guaranteed realization**, not a contradiction of the parental expected-return computation.

Among the other **20 sources** where the lowest I allele did fix under decline, its census30 count was **at least 16/96**. The two higher-fixation cases had only **4/96 and 6/96** low-I copies. These ranges separate *this retrospectively selected original 22-case cohort*, but **do not define a valid biological frequency threshold** or demonstrate a sharp phase transition. The ranges, cohort, and cutoff-like gap were examined **after seeing the original outcomes**; sampling is nested in only **11 independent founder IDs**. Some rare alleles can fix under other conditions, and these two examples cannot measure a general fixation probability at any allele frequency.

## Consequences for the ecological/evolutionary hypothesis

The original model supports a qualified, **genetic-access boundary**: an environment can favor reduced floral investment in expected parentage, yet (i) the smallest attainable I endpoint depends on which lower-I alleles remain after earlier history, and (ii) low-copy variants can disappear through finite realized reproduction even when a negative static reproductive sorting signal exists. Genetic support is therefore a **state constraint on realizable outcomes**, not just a parameter that determines the sign of selection.

The original same-genotype source treatment comparison already shows the negative I expected shift in every strong-history source at census30, while the 50-update outcomes show 12/22 negative I contrasts and 10/22 zero contrasts. The new 20/22 lower-accessible fixation tally and the two source-exact exceptions refine *why deterministic prediction from the sign alone is inadequate*; they do **not** uniquely identify whether any allele was lost because of genetic drift, lack of reproductive opportunity, correlations among diploid genotypes, numerical pollen delivery, or interacting fitness components. Those mechanisms can co-occur and need a new controlled, independently specified experiment to separate causally.

These are **numerical allelic values**, not demonstration of identical identity-by-descent lineages. None of these 22 source pairs is an independently sampled island or a new experimental founder; no new significance tests or registered endpoints are introduced. Evidence remains conditional on synthetic Model 3 and on the original, exposed 2026-10-19 pollen-source cohort.

## Reproduce

- Native original-state reader: `scripts/audit_chapter2_r2_original_I_accessibility_20261024.py`
- Source receipt: `docs/audits/CHAPTER2_R2_STANDING_I_ALLELE_ACCESS_20261024.json`
- Dedicated tests and two original-source negative controls: `tests/test_chapter2_r2_original_I_accessibility_20261024.py`
- Original roster of 24 pre-shock states: `docs/audits/CHAPTER2_R2_ORIGINAL_384_STRICT_AM_PREFIXES_20261023.csv`

From repository root, run:

    python -m scripts.audit_chapter2_r2_original_I_accessibility_20261024 --native
    python -m pytest -q tests/test_chapter2_r2_original_I_accessibility_20261024.py

To independently verify all 22 results against **the external original ZIP**, supply it separately:

    python -m scripts.audit_chapter2_r2_original_I_accessibility_20261024 --zip /path/to/baseline-pollen-384-source-20261019.zip
    CHAPTER2_R2_384_ORIGINAL_ZIP=/path/to/baseline-pollen-384-source-20261019.zip python -m pytest -q tests/test_chapter2_r2_original_I_accessibility_20261024.py

This technical native replay only duplicates **2,860 already-existing original source updates** (22×30 original prefixes + 22×2×50 original paired futures) with their archived full-genome hashes. **New biological population updates = 0, independent cohort experiments = 0, newly registered tests = 0.**
