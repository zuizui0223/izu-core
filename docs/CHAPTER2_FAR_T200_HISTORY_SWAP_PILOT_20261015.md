# Technical pilot: original t200 genotypes × future assurance policy (2026-10-15)

**Status: source-authenticated, single-original-visitor-history NEW conditional futures. These are exploratory feasibility/technical results, not independent ecological confirmation, main-treatment effect replication, evidence of historical mediation or a Q3 causal mechanism.**

## Frozen design and source

- See [prospective-to-the-new-futures post-outcome exploratory protocol](protocols/chapter2_far_t200_history_swap_20261015.json) and [pilot script](../scripts/chapter2_far_t200_history_swap_20261015.py).
- Original 2026-10-06 four-setting, 64-history × 8 demographic repeat study is unchanged. Four original ZIP shard IDs: 11411031490, 11410452132, 11411051762, 11411155493; authentication rejects mismatching outer ZIP SHA-256 and every inner source manifest/case receipt.
- [GitHub Actions pilot run 38708130106](https://github.com/zuizui0223/izu-core/actions/runs/38708130106) **success**; [full result artifact 11959363204](https://github.com/zuizui0223/izu-core/actions/runs/38708130106/artifacts/11959363204). One predeclared original visitor seed **26110601**, original demographic repeat **26111601**, four original mating settings × two **t200 origin genotypes** (fixed/evolved assurance) × two **new future policies** (A fixed/evolvable) = **16** new conditional futures; update 200→1000 = **12,800 new model updates**. These are **not 16 independent visitor histories**.
- Exactly **625/800** future annual visitor states were visitor-free in this **one far history**. All 16 conditional descendants had terminal **N=48** at update1000. Genomes and all future parentage were saved in the artifact, with fixed future policy A expression at 0.5; stored prior t200 source parent IDs/birth ages were unavailable and reconstructed.
- Independent artifact readback checked all **16** SHA-256 case receipts against ZIP payloads and recomputed **801** annual diploid-genotype investment means against all stored annual I summaries per case, with **maximum absolute disagreement 0** (native float arithmetic). The four per-setting 2×2 contrasts below are checkable in the exact source output, but are **not inferential estimates**.

## Single-history pilot contrasts (raw I, update 200→1000)

For each original t200 origin, future policy effect is:
`[I(t1000)-I(t200)] future A evolving − future A fixed`, with identical t200 genetic alleles and the same future visitor sequence.

| Reproductive rule | Future-policy E−F from originally fixed-A t200 genome | Future-policy E−F from originally evolved-A t200 genome | Origin × future-policy interaction |
| --- | ---: | ---: | ---: |
| delayed control | −0.003425 | −0.254955 | −0.251530 |
| prior selfing | −0.047915 | −0.065445 | −0.017529 |
| pollen discount | +0.245009 | −0.201391 | −0.446400 |
| assurance cost | −0.029133 | −0.208310 | −0.179177 |

**Reading and intervention limit:** the future-fixed intervention **simultaneously resets the expressed A phenotype to 0.5 and turns off new A mutation**; the future-evolving branch retains existing A expression and mutation. Thus **future-policy E−F is not a mutation-only, evolvability-only or historical genetic mediation effect**. At the one selected visitor history, this combined-policy effect differs by which t200 diploid population is used. The positive future effect in one fixed-origin pollen-discount cell, and the negative effects in most others, must not be promoted to any model-general or signed biological mechanism: a matched future RNG still produces stochastic parentage differences and origin populations had distinct initial I distributions; 64 independent source histories were not run. This pilot does not reproduce the 8-repeat original far E−F+ contrast, nor prove any time-lag, gene support, selection covariance or demographic mediator.

## Gate for the next, unexecuted step

- The design specifies **64 visitor-history clusters**, all four reproductive rules, two original diploid t200 origins × two future A policies = **1024** conditional new futures, 819,200 model updates if fully completed. **Not run by this pilot**. The original main 8 repeats remain separate; their primary frozen confidence intervals must never be replaced by this one-repeat new-future cohort.
- Pre-specified primary conditional estimand is future A-policy effect **within the identical original diploid genotype source**, then origin×future interaction; report complete history distributions and visitor-history clustered intervals, not per-year pseudo-replication.
- Annual Price expectations describe next-generation parent-genome selection *conditional on state*; compare with realized next-census change and genotype support to diagnose discrepancies. Partition cannot uniquely identify natural mediation.
- Run source genotypes from both arms through both possible future policies; preserve extinction as undefined trait effect (not missing-at-random), and keep all source histories including zero visitor cohorts.
- Repo workflow policy requires manual **`workflow_dispatch`** only for experiment workflows. The branch's technical pilot workflow was accordingly corrected after the successfully run initial push-pilot so the repository scientific CI guard is not weakened.

**Conclusion:** original-source intake + conditional continuation mechanics are operational; the ecological/genetic explanation for positive far-side E−F remains **unidentified**.
