# Far-side assurance paradox: native original-genome Price audit (2026-10-15)

**Status: SOURCE-VERIFIED, RETROSPECTIVE, NOT independent ecological replication or causal mediation.** Original prospectively frozen four-setting experiment and manuscript claims are not modified.

## Identifiable question

Does the small positive evolved-assurance-minus-fixed-assurance floral-investment endpoint in the far/low-visitor arm appear only after update 1000, and can the contemporaneous one-step genetic selection response or A–I factor association explain its sign?

**Source:** original 2026-10-06 [four-setting campaign](../data/design/chapter2_assurance_generality_20261006.json), authentic ZIPs 0–3 (artifact IDs 11411031490, 11410452132, 11411051762, 11411155493) from [Actions run 37458098483](https://github.com/zuizui0223/izu-core/actions/runs/37458098483); SHA-256 outer ZIPs, embedded source manifests, original 0/200/400/1000 NPZ alleles and case receipts all authenticated by the unmodified source verifier. Visitor RNG stream replay parity also checked. Experimental unit: 64 original visitor histories per setting, **only one original nested demographic repeat** (26111601), not the eight repeats that support the main confirmation.

**New work:** [source auditor](../scripts/audit_chapter2_far_assurance_price_checkpoints_20261015.py) + [frozen source-only protocol](protocols/chapter2_far_assurance_price_checkpoint_20261015.json) + [focused tests](../tests/test_chapter2_far_assurance_price_checkpoints_20261015.py). Four original reproductive settings × 64 histories × near/far × fixed/evolving A × 4 genome checkpoints = **4,096 audited original genetic checkpoints**. Of these, the 200 and 400 checkpoints yielded **2,048 one-step Price-assay source cells**. Zero newly simulated years, offspring, histories, founder draws or independent real islands.

### 1. When does the endpoint contrast arise?

Mean E−F investment (E = A evolvable; F = A fixed at 0.5), in the **first** demographic repeat, from original saved diploid genotypes. Initial E−F trait difference was exactly zero across all settings/arms. These values are raw trait units, **not a change from founder**, and no biological independence is conferred by treating updates as repeated samples.

| Mating setting | E−F near t200 | near t400 | near t1000 | E−F far t200 | far t400 | far t1000 |
|---|---:|---:|---:|---:|---:|---:|
| delayed_control | -0.003963 | -0.018291 | -0.083673 | +0.055359 | +0.025934 | +0.034509 |
| prior_selfing | +0.012244 | -0.016520 | -0.176145 | +0.059925 | +0.062769 | +0.028542 |
| pollen_discount | -0.014594 | -0.044012 | -0.147894 | +0.030349 | +0.023092 | +0.017706 |
| assurance_cost | -0.020320 | -0.036718 | -0.088828 | +0.027222 | +0.030797 | +0.005075 |

**Source finding:** far E−F is already positive by update 200 across all four reproductive rules; it remains positive at the audited 400/1000 checkpoints in this first repeat. Meanwhile near E−F becomes negative in all four settings by 400. Hence the far-positive sign is not a t1000 subtraction or terminal-survivor artifact. However the first-repeat t1000 values differ from the main eight-repeat effect, especially for direct A cost, showing why these observations cannot replace the original 64-history×8-repeat confidence intervals.

### 2. Do the actual parents' inherited genetic returns align with the far-positive endpoint?

For every original state at update 200 and 400, use the unchanged native reproduction operator and

`W_i = 0.5*F_i + 0.5*P_i + S_i`

with father rows, mother columns and viable selfing on the diagonal. Without drawing offspring, verify to 1e−12 that the expected conditional next-generation I shift equals both the explicit father–mother pair lottery mean and `Cov_N(I_i,W_i)/mean_N(W_i)`. This is an exact within-state expectation only when no new mutations, seed immigration or surviving adults are applied during the diagnostic step; extinct-state mean would be undefined.

| Mating setting | Far t200 ΔPrice(E−F) | Far t400 ΔPrice(E−F) | Far zero-visitor count t400 | Far A-alignment at zero visitors, t400 |
|---|---:|---:|---:|---:|
| delayed_control | +0.00001478 | -0.00003439 | 50/64 | -0.00001916 |
| prior_selfing | +0.00021432 | -0.00001711 | 50/64 | +0.00005077 |
| pollen_discount | +0.00013883 | -0.00003391 | 50/64 | +0.00009670 |
| assurance_cost | -0.00001375 | -0.00012697 | 50/64 | +0.00007354 |

**Source finding:** at the t400 original checkpoint, the mean one-generation expected Price shift in evolving A **minus** fixed A is negative in all four far settings. This has the opposite sign from the contemporaneous far E−F *trait-level difference*. It does not mean E trajectories must decline relative to F for the next 600 steps; the source snapshots do not include all intervening genotypes, visitors and realized births. It does rule out the inference that the positive far endpoint is immediately implied by the t400 local selection response.

### 3. Native zero-visitor factorization and A–I association

At t400, **50/64** far visitor histories have exactly zero visitor types (only **1/64** near history). All such original source states were retained, not excluded as missing. Then for positive viable selfing, the original source fitness factorizes as

`W_i ∝ exp(-c_I*I_i**2) * [A_i*exp(-c_A*A_i**2)]`.

The audit independently verifies this exactly against the original full F/P/S ledger for each zero-visitor native genome. The A-alignment diagnostic compares expected next I under the complete native original weights versus the same source population with the square-bracket A factor held constant among individuals (I genotypes and their I-specific cost weights unchanged).

These effects are **tiny and not sign-consistent**: delayed control is slightly negative at t400, and the other three settings slightly positive. This particular contemporaneous between-individual A–I alignment is therefore *not by itself an established explanation* of the shared positive 1000-update E−F endpoint. Its effect is not zero in every population, and repeated small/variable selection effects cannot be excluded without a full longitudinal replay.

### 4. What has actually been settled?

1. A pure terminal-readout or wrong-subtraction explanation is disfavoured by direct original checkpoint I comparisons at four times.
2. The original source mating/parentage conservation and numerical Price identities pass; **this is not a new full 1000-year independent biological replay**, nor a proof every code path is bug-free.
3. The mechanism is **history-dependent realized inherited population composition**, not identifiable solely by the cross-sectional A–I alignment or fixed-state local gradient. No unique shares for drift, A-driven realized selfing, genetic covariance, Mendelian transmission, or remaining inherited feedback can be reported.
4. The original 8-repeat, 4-setting insurance compression claim stays at its previously registered evidence rank, while this after-outcome 1-repeat audit is mechanistic source support only. The original near arm remains pollen limited, not a pollen-saturated mainland.

## Reproducibility and source archive

- Source-only readout: [GitHub Actions 38685186752](https://github.com/zuizui0223/izu-core/actions/runs/38685186752), job `116258372904`, **success**, on head `5aa89890c424cf5a408930f8351bda96134f46ce`.
- Full 4,096-checkpoint/2,048-Price-cell JSON: [artifact 11949773757](https://github.com/zuizui0223/izu-core/actions/runs/38685186752/artifacts/11949773757) (`chapter2-original-far-price-audit-20261015`, archived ZIP SHA-256 `55dc0a08b9d01a386eee9396f341cc9f26d9c623e449238e28d36c505c713db3`). This is the original-source **derived audit**, not a DOI deposit.
- All original frozen SHA-256 admissions are checked by existing source code [original-evolved-pollen-service auditor](../scripts/audit_chapter2_original_evolved_pollen_service.py).
- This PR initially failed the repository tracked-data budget only (new protocol data JSON would exceed budget by ~3.5 KB); the protocol bytes were moved unchanged to `docs/protocols/` and the original `data/design/` duplicate deleted before rerunning ordinary CI. This storage fix changes no scientific model, audit design or biological result.

**Decision:** Do not promote a novel ecological mechanism or a full Q1→Q4 causal mediation from this result. A future discriminating test must follow actual annual full genomes and F/P/S parentage with matched treatment pairs, and compare controlled A expression/distribution under a frozen, independent history design; merely accumulating more retrospective source snapshots cannot uniquely allocate drift versus selection.
