# Original archived R2 384-path cohort: paired A fixation, not just aggregate bounds

**2026-10-23 — exact readback of ORIGINAL source ZIP, retrospective/descriptive. No new evolutionary updates or independent confirmation.** This is a stronger audit of the *same exposed 384 trajectories*, not a 384-island sample or a new prospective replication. R1–R5 source evidence ranks, the prospectively tested fresh-founder R2 four-setting **overall INCONCLUSIVE**, and registered R4 G/S are unchanged.

## Source recovery and identity

The original [GitHub Actions run 39233450099](https://github.com/zuizui0223/izu-core/actions/runs/39233450099) preserves artifact **12178257738** (named `baseline-pollen-384-39233450099-1`). We downloaded the **original 1,857,529-byte ZIP** rather than reconstructing an equivalent hypothetical population or substituting a saved aggregate. The ZIP byte SHA-256 is `10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e`. All seven internal file hashes listed by `SHA256SUMS` verified.

- Original producer source SHA: `eb785dc6865ca1842ec9d6c7d511778c74e03478`
- Original frozen 384 pilot protocol SHA-256: `87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849`
- Two complete original shards: `strong.json` and `weak.json`, **192 paths each**
- 12 independent founder seeds × four *nested* demographic repeats × A0(.3/.5) × strong/weak prior pollen limitation × decline/control = **384 source paths**, or **192 paired futures**.
- Every matched decline/control pair has identical genotype/allele-support state, census-30 fingerprint and reproductive records across the first 30 updates. The final paired states were compared directly after the remaining 50 updates, not inferred from marginal counts.
- The original source `audit.json`, `summary.json` and independent saved-data review agree with the extracted 48 matched pairs, zero contrast counts, prefix fixation counts and A contrast means in every A0×baseline cell. All 384 populations survive.

## New source-exact joint finding

Define **zero A response** as the *exact numerical* terminal treatment contrast `A80_decline − A80_control = 0` for one paired source, not absence of within-arm evolutionary change or a prespecified biologically meaningful effect size.

| Initial A | Prior pollen limitation | Exact-zero A treatment pairs /48 | A locus already fixed at shock /48 | **Shock-polymorphic → both futures fixed to same A allele** /48 | Exact-zero pairs with **different full terminal state hash** |
|---:|---|---:|---:|---:|---:|
| **0.3** | Strong | **45** | 22 | **23** | 42 |
| 0.3 | Weak | 8 | 1 | **7** | 8 |
| **0.5** | Strong | **42** | 10 | **32** | 38 |
| 0.5 | Weak | 8 | 1 | **7** | 8 |
| **Total** | | **103 / 192** | **34** | **69** | **96 / 103** |

**All 103 zero-contrast source pairs have the same fixed A allele at BOTH future endpoints.** This is a direct pair-level observation, stronger than the earlier conservative inclusion–exclusion lower bounds of 43/48 and 35/48 for strong-limitation final cofixation, and 21/48 and 25/48 for its shock-polymorphic subset. The exact corresponding strong-baseline numbers are **45/48, 42/48**, and **23/48, 32/48**.

Crucially, the **69** pairs with standing A polymorphism at the shock nevertheless reached the same A fixed state after different visitor-activity futures. In these 69 pairs both A means *changed from census 30*: a zero **paired treatment difference** is not a zero evolutionary response in both arms.

Another key qualification: **96 of 103** of these A-converged pairs have **different complete terminal population state fingerprints**, which incorporate genotype, allele origin, individual identity and age. The evidence is therefore **A-locus phenotype/allele convergence**, *not* identical complete genetic-population realization. Seven pairs had matching full state fingerprints.

## Signs of the 69 within-pair changes (descriptive, not selection inference)

In the source pairs that retained A polymorphism at the shock but converged to identical fixed A alleles:

- Strong prior limitation, A0=.3: **23 increased, 0 decreased** in both future arms.
- Strong prior limitation, A0=.5: **31 increased, 1 decreased**.
- Weak prior limitation, A0=.3: **3 increased, 4 decreased**.
- Weak prior limitation, A0=.5: **1 increased, 6 decreased**.

Thus **54/55** of the strong-limitation shock-polymorphic/cofixed paired states moved toward higher expressed A, compared with **4/14** in weak prior limitation. These are **conditional, post-outcome nested-model descriptions**, not 69 independent randomized populations, evidence of a universally attracting evolutionary equilibrium, or a causal selection-versus-drift decomposition. The founder histories, prior q, A distributions and strength of additional q change differ across the two prior regimes.

The 89 paired futures with **nonzero** A treatment contrast are also heterogeneous: under strong history only **3/48 and 6/48** have a nonzero (positive) contrast; under weak history **35 positive / 5 negative** (A0=.3), and **31 positive / 9 negative** (A0=.5). Thus this finding does **not** support a claim that every further decline in visitors increases assurance.

## Interpretation for ecological/evolutionary questions

The original baseline-384 program produced a sparse incremental A response after long-standing severe pollen limitation. **Direct raw-source identity checks now show that the sparseness coincides exactly with identical A-locus fixation at both endpoints, even though the overall population state often differs.** Post-shock cofixation accounted for 55 of the 87 zero contrasts in the strong-baseline group, not merely the 32 pairs already fixed at the shock. Across all strata, 69 of 103 zero pairs were still polymorphic at the shock.

That narrows the *proximate source endpoint explanation*, but does **not** identify the *causal mechanism*: whether A moves through selected reproduction, demography, shared allele support, similar resident returns, stochastic bottlenecks, or interactions with I/M. Nor does it distinguish genetic-history effects from unequal contemporary pollen service. A monomorphic endpoint has no standing A variation in the no-mutation/no-immigration experiment, but this does not establish irreversible evolution in nature.

The separate static R2 assays correctly distinguished maternal viable-seed output from parental-genome contribution. **Their homogeneous reporter calculations are not the actual evolved genotype selection gradients of these 192 pairs**. Any claim that they caused the 69 cofixations requires new source-state-matched analyses or an independently registered donor/pollen factorial.

## Reproduction, exact fail-closed controls

```bash
# First download the original 384 ZIP from GitHub Actions artifact 12178257738
python -m scripts.audit_chapter2_r2_original_384_pair_convergence_20261023 \
  --zip /path/to/baseline-pollen-384-original.zip
pytest -q tests/test_chapter2_r2_original_384_pair_convergence_20261023.py

# Optional full raw source replay by test:
CHAPTER2_R2_384_ORIGINAL_ZIP=/path/to/baseline-pollen-384-original.zip \
  pytest -q tests/test_chapter2_r2_original_384_pair_convergence_20261023.py
```

The runner refuses a mismatched artifact SHA, incomplete file manifest, changed protocol or source commit, missing/mismatched source pairs, unequal first 30 updates, changed original published contrasts, or altered original fixation counts. The repository stores the [compact machine-readable receipt](audits/CHAPTER2_R2_ORIGINAL_384_PAIR_CONVERGENCE_20261023.json) and a testable raw-source reader; it **does not commit a second 1.86 MB copy of the external ZIP**. Default CI checks the independently verified archived receipt against prior independent summaries and exercises paired-classification counterexamples; end-to-end ZIP replay requires explicitly supplying the original source file.

**No new population generation, p-value, prospective registration, natural island validation, causal mediation result, or model parameter retuning is introduced.**
