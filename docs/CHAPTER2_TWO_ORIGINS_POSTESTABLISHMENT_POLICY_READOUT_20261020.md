# Third source namespace: native versus fixed-expressed A/I after establishment

**2026-10-20 | TECHNICAL ENGINEERING COHORT — NOT AN INDEPENDENT BIOLOGICAL CONFIRMATION.** This records only numerical evidence already printed by the completed original [Chapter 2 scientific gate](https://github.com/zuizui0223/izu-core/actions/runs/39277643082) (job `118146523676`) at source commit `d6161057cf0b1e8272049efbf981cbc67be3eff0`. The scientific gate concluded **success**. The general cross-Python CI associated with this commit was still in progress at subsequent checks; these are different tests. No new publication p-value, posterior or confidence interval is introduced. The editable study source is [`scripts/chapter2_two_origins_postestablishment_probe_20261019.py`](../scripts/chapter2_two_origins_postestablishment_probe_20261019.py), checked by [source tests](../tests/test_chapter2_two_origins_postestablishment_probe_20261019.py).

## Source registry and comparison

- **THIRD** technical source namespace 21030000–21030023, 24 independently generated **artificial source genotypes** (three A-hints × two I-hints × four genotype seeds per stratum), disjoint from the prior six exposed source genotypes and from the previous 24 train +24 heldout genotypes.
- Four synthetic environments: budget B4.5 or B8 × functional visitors 0 or 4. Each of 24 source genotypes is repeated with **8 nested demographic/arrival seeds**, giving 192 **candidate attempts per environment** and 768 total candidate attempts; the 4 downstream policies make 3,072 **paired arm trajectories, not 3,072 independently arriving taxa or islands**.
- One common original source genotype, Bernoulli arrival event, native founding reproduction update and first genotype precede the policy fork: **native** allele-expressed A and I; **clamp_A** expressed source *population mean* A for every descendant; **clamp_I** expressed source population mean I; **clamp_A_I** both means fixed. All arms have the same random-stream master but RNG event draws can diverge after their histories differ. Native diploid alleles **still segregate** in the clamp policies, and selfing is **not** disabled when A expression is fixed.
- Horizon **6 reproductive updates** (one early establishment update, five subsequent native updates), source founding population 2 adults, capacity12, mutation/immigration=0, no interacting-lineage community.

## What was observed in the original gate

All denominators below are **192 original candidate attempts per environment**, including arrivals that failed to establish.

| Budget | Visitors | Arrived | Established at first update | Native survived at update 6 | clamp_A survived | clamp_I survived | clamp_A_I survived |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B4.5 | 0 | 156 | 117 | **50** | **50** | 51 | 51 |
| B4.5 | 4 | 157 | 127 | **67** | **67** | 67 | 66 |
| B8 | 0 | 158 | 141 | **91** | **91** | 91 | 91 |
| B8 | 4 | 154 | 148 | **118** | **118** | 117 | 118 |
| **Total, descriptive** | — | 625/768 | 533/768 | **326/768** | **326/768** | 326/768 | 326/768 |

In all four synthetic environmental contexts the *marginal* occupancy count of native and source-mean-clamped A policies is equal (native minus clamp A **0/192 = 0 percentage points**). The sum across these four contexts also equals zero. **This does not imply identical paired individual fates, identical final genotypes, an effective equivalence test or zero causal contribution of A evolution.** The previously registered Chapter 2 long-horizon 160×160 survival result involved different source configurations, 80 updates and a different policy intervention, so the results must not be directly compared as a single temporal crossover experiment.

### Pre-specified A-hint strata from original job

| Budget / visitors | Source A-hint class | Native survivors / 64 | clamp-A survivors / 64 | clamp-I survivors / 64 |
| --- | --- | ---: | ---: | ---: |
| B4.5 / 0 | low | 0 | 0 | 0 |
| B4.5 / 0 | middle | 17 | 17 | 17 |
| B4.5 / 0 | high | 33 | 33 | 34 |
| B4.5 / 4 | low | 3 | 3 | 3 |
| B4.5 / 4 | middle | 31 | 31 | 31 |
| B4.5 / 4 | high | 33 | 33 | 33 |
| B8 / 0 | low | 6 | **7** | 6 |
| B8 / 0 | middle | 38 | **37** | 38 |
| B8 / 0 | high | 47 | 47 | 47 |
| B8 / 4 | low | 22 | 22 | 21 |
| B8 / 4 | middle | 53 | 53 | 53 |
| B8 / 4 | high | 43 | 43 | 43 |

The low/middle/high source strata are from design hint values .2/.5/.8; actual source genotype means vary around those hints. These counts still contain nested eight repeat streams per source and **must not be scored as 64 independent lineages per class**. In B8/0 the native vs clamp-A marginal totals cancel across the low and middle A source strata, so aggregation alone can conceal heterogeneity.

## What this says about the two-origin hypothesis

**Supported in this one exposed synthetic cohort:**
- A source-state stratum is a strong *descriptive predictor* of six-update occupancy across contexts (even when the policy clamp is applied after the founding update).
- The specific intervention that suppresses A's **subsequent expression change** by clamping every descendant to source-population mean A had **zero aggregate survival-count difference** from native A in all four artificial contexts over this short horizon.
- Different first-establishment outcomes under A/I expression interventions and nonzero source-selection terms were separately measured by earlier technical experiments. None of these equal a naturally observed taxon-level colonization filter.

**Not identified:**
- **Causal effect of post-establishment genetic A evolution alone:** clamping source-population-mean A immediately suppresses **standing within-population phenotypic heterogeneity**, not just inherited mean evolution; genotypes still transmit and founder selection occurs at establishment before the clamp.
- **No effect of evolutionary response in general:** six reproductive updates may be too short, founder genotypes insufficiently variable, and resource/pollinator conditions selected as technical fixtures rather than independently registered biological regimes.
- **A becomes fixed on mainland or is exclusively imported:** no model event is a continental stage, and the source genotype hints are artificial.
- **I evolves exclusively on islands:** I has a direct initial establishment fitness effect and its short-horizon descendant changes were small. Existing six-update results **do not support** an exclusive I-after-settlement pattern.
- **Individual paired fate equivalence:** marginal equal counts can conceal discordance between policy arms. [A later source-locked paired-discordance test](../tests/test_chapter2_two_origins_postestablishment_probe_20261019.py) was added to inspect the actual `both/native-only/clamp-only/neither` cells; its latest CI has to pass before those values are admitted as verified evidence.

## Next action / admission

1. Independently admit all policy-paired discordance counts (not just equal marginal totals), strictly preserving the original source×island×reset denominator. If differences cancel, report them without cherry-picking.
2. Design an explicit **founding trait-profile-preserving** alternative expression intervention before calling any native-vs-A-clamp contrast an evolutionary-genetic effect; distinguish mean-A change and within-individual A expression variance. Make clear which source genome and random events each intervention holds constant.
3. For ecological generality, a future independently registered source×island confirmation needs new genotype and island-factorial namespaces, source- and island-heldout proper forecast scores, meaningful biological effect threshold, power/resources and a source-compatible interacting-lineage model or acknowledged noninteracting null. It cannot be inferred from this 24-genotype technical demonstration.

**Scientific publication route:** the registered source-supported Model3 Q1–Q4 Article remains separate [PR #609](https://github.com/zuizui0223/izu-core/pull/609); Draft [PR #610](https://github.com/zuizui0223/izu-core/pull/610) is a prospective island assembly research prototype.
