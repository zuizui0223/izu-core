# R2 pathwise Model 3: expected parental genetic sorting versus finite realization

**2026-10-24 — strictly original-source technical replay, source-selected and retrospective. Not a new experimental cohort, preregistered selection/drift experiment, or empirical island generalization.**

## Current scientific question

Original 384-path R2 source data show that flower investment **I** can respond to visitor activity decline even when both autonomous reproductive assurance **A** and matching trait **M** have already become monomorphic. After strong prior pollen limitation, 22 original matched pairs were A/M-fixed, I-polymorphic at the shock and 22/22 visitor-decline futures ultimately fixed I. Maintained visitors yielded 13/22 I-fixed endpoints; 12 paired I contrasts were negative and 10 exactly zero. 

The authenticated full census30 diploid genotype replay in PR #633 identified an **immediate one-generation expected I sorting difference** (decline minus maintained) of **−0.002857521** I trait units, negative in all **22** source cells. This static expectation is not the same as the observed 50-update endpoint contrast (**−0.089133523** on average). The key next question is *how to describe the gap without falsely calling all residual changes "drift"*.

## Identity on the exact original visited genotype sequence

At each original update t, native Model 3 gives the expected offspring genotype-weighted investment trait under its **full ordered paternal × maternal** expected viable outcross parentage and viable autonomous selfing. With parent I_i and no mutation or immigrants:

    E_t[I_child] =
       [sum_{father,mother} outcross[father,mother] * (I_father+I_mother)/2
          + sum_i self_viable[i]*I_i] /
       [sum_{father,mother} outcross[father,mother] + sum_i self_viable[i]].

Define **current conditional expectation** and **one-generation realization residual**:

    S_t = E_t[I_child] - I_t
    epsilon_t = I_{t+1} - E_t[I_child]
    I_{t+1} - I_t = S_t + epsilon_t.

Because these terms are defined for **every visited state of the original source trajectory**, their sums telescope over updates 30–79:

    I_80 - I_30 = sum_{t=30}^{79} S_t + sum_{t=30}^{79} epsilon_t.

In each original 50-update **paired** comparison, subtract corresponding totals from maintained-visitor versus decline-visitor futures:

    I_80(decline) - I_80(control)
      = [sum S_t(decline) - sum S_t(control)]
      + [sum epsilon_t(decline) - sum epsilon_t(control)].

These are **exact descriptive accounting identities conditional on an actual stochastic realized history**, not a causal intervention that removes selection or forces drift. The expected term **depends on the current genetic state**, which itself changes through prior parent sampling, inheritance, resource allocation and visitor feedback. Residuals include the finite draws of recruits/parents and segregation; they are **not a standalone independently manipulated "drift effect"**. Neither the ratio of summed expected to realized contrasts nor the ratio of squared components should be called a universally identifiable "share caused by selection".

## Source of truth and acceptance criteria

The new script uses the exact original Model 3 producer from the 2026-10-19 **frozen experimental protocol** and exact authenticated 24-source census30 roster from PR #633 (Git blob SHA `6b04ee9a5cd6c2342e397c6c69539688474b391f`).

It reexecutes **only existing** source histories, never samples new founders, visitor histories, or RNG streams:
- **24 × 30 = 720** original source prefix updates, required to reproduce all 24 census30 full-genome fingerprints;
- **24 × 2 × 50 = 2,400** original recorded source future updates, paired by the original copied source RNG streams, required to reproduce **each of the 48 original terminal full-genome fingerprints** recorded in the source ZIP;
- for each original year and realized genome, evaluate the original `reproduce` ledger and perform the expected parental-mean arithmetic above;
- fail closed if any state hash, original source settings, ordered-parent algebra, one-update accounting, or accumulated 50-update identity fails.

In the original source model, adult survival, mutation and incoming seeds are zero. The number of occupied adults can **temporarily drop below K=48** in some future paths. The script handles N=1..48 rather than silently assuming all paths remain full at every census, and rejects extinction when contrary to the original archived all-surviving source.

It retains full **50-update trajectories and conditioning information** in the source artifact and compact summary-level readout for strong and weak prior pollen-limitation groups. No raw ZIP is recommitted: authenticated original [Actions artifact 12178257738](https://github.com/zuizui0223/izu-core/actions/runs/39233450099) remains the source of truth.

## Source-executed original-genome pathwise results (2026-10-24)

**Actual verification, not a proposed future simulation:** GitHub Actions [run 40057254260](https://github.com/zuizui0223/izu-core/actions/runs/40057254260) generated the full 50-update source readback (artifact **12546400082**, original output **1,381,522 bytes**, SHA256 `794a23aca8e56f8e74f4d5497fa221cbba9432a20170917163fe117dd7fddccc`). Source replay matched **all 24 census30 and 48 terminal full-genome fingerprints** from the original October 19 experimental ZIP. All 2,400 original future updates were source-replayed; **0 new seeded futures** were allocated. The permanent [compact receipt](audits/CHAPTER2_R2_ORIGINAL_PATHWISE_RECEIPT_20261024.json) preserves the result, artifact provenance and limits. Cross-run last-bit floating differences are allowed only under explicit numeric tolerance: do not promote the first output's raw SHA to an invariant of other platforms.

For the same archived 24 source cells, the pairwise observed **terminal** I contrast is the sum of the *two realized-path conditional expectation differences* and the *two realized-path stochastic residual differences*:

| Original historical pollen limitation | Paired source cells (independent founders) | Mean accumulated expected-I contrast | Mean accumulated realization-residual contrast | Mean original final I contrast |
| --- | ---: | ---: | ---: | ---: |
| **Strong** | **22 (11)** | **−0.056857** | **−0.032277** | **−0.089134** |
| Weak | 2 (2) | +0.044878 | +0.050174 | +0.095052 |

These three columns add up **by construction and by independent source-state replay**, not as separate experimental causal effects. Under strong historical pollen limitation, accumulated conditional expected sorting differences were **negative in 19/22**, positive in **3/22**; the realization residual differences were **negative in 11/22** and positive in **11/22**; final I treatment differences were **negative in 12/22** and exactly zero in **10/22**.

Among the **10 original strong-history pairs with identical final I**, the mean cumulative expected component was **−0.026543** and the mean realized residual component **+0.026543**, exactly cancelling at the endpoint. For the **12 original strong-history pairs with lower final I under decline**, the respective means were **−0.082118** and **−0.081293**, both contributing negatively to the observed difference. Thus the 10 zero contrasts are not evidence that the entire dynamic conditional expected sorting contrast was numerically zero.

**Contrast with the census30 static result:** at the initial same-genotype shock state, the instantaneous first-generation expected-I treatment differential was negative in **22/22** strong-history source cells. Over the full finite 50-step *realized genotype paths* only **19/22** have a negative accumulated expected-I contrast. This is an important state-dependence result: the initially evaluated local expectation does not uniquely determine the full moving-genotype expected contribution or final genetic endpoint. Three positive accumulated conditional sums are model-bound and post-outcome; they are not a claim of reversals in all contexts or an independent test.

A source step can occasionally drop below the 48-adult capacity without extinction (**1 future step across the 22 strong-history pairs**). The source replay includes that state exactly. These 22 histories belong to **11 unique founders** with nested demographic repeats and were selected after examining archived outcomes. No independent significance level or natural-island inference is attached.

## Source-bound interpretive ceilings

- No **new biological population futures**: recomputing the original stored genotypes is a technical replay, not a new experimental allocation.
- Only **11 founder seeds** contribute the 24 posthoc selected shock-time source states, with nested repeat/initial-A contrasts. Do not treat 24 × 2 trajectories or their 2,400 updates as independent ecosystems.
- A positive selection-looking conditional expectation does **not** force a positive finite realized response; the realised residual is not automatically pure random neutral drift.
- The decomposition is path-dependent, and changing the visitor regime also changes *future population states*. It **cannot by itself identify the counterfactual causal contribution of selection** or prove A/I locus independence in real organisms.
- The original prospective independently founded R2 four-setting overall judgment remains **INCONCLUSIVE**; the original R1, R3–R5 rankings and R4 G/S are unchanged.
- Natural-island inferences would require observed genetic/pollen/genotype turnover data and appropriately independent island systems.

## Reproduction and result provenance

- Frozen original pilot: `scripts/chapter2_pollen_baseline_factorial_20261019.py`
- Original R2 lineage fingerprints: `docs/audits/CHAPTER2_R2_ORIGINAL_384_STRICT_AM_PREFIXES_20261023.csv`
- Accepted original full genome replay and static parental expectation: `scripts/audit_chapter2_r2_shock_genome_expected_I_20261023.py`
- **New original pathwise technical replay**: `scripts/audit_chapter2_r2_original_pathwise_I_accounting_20261024.py`
- Negative controls and SHA/type tests: `tests/test_chapter2_r2_original_pathwise_I_accounting_20261024.py`

From repo root:

    python -m scripts.audit_chapter2_r2_original_pathwise_I_accounting_20261024 > /tmp/R2_ORIGINAL_PATHWISE_ACCOUNTING.json
    python -m pytest -q tests/test_chapter2_r2_original_pathwise_I_accounting_20261024.py

The full generated JSON will be captured as an Actions artifact only after CI success and will be identified by its actual original-source head commit and digest. Do not write fixed biological effect estimates into this note before a verified original source run.
