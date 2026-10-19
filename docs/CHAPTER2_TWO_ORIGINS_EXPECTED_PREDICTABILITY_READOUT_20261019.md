# Expected predictability of individual founding success in the exposed six-source Model 3 fixture

**2026-10-19 | Read-only TECHNICAL result, not a general ecological law, independent held-out forecast or confirmatory biological run.**

## Audited numerical result and source

- [GitHub scientific-gate job log](https://github.com/zuizui0223/izu-core/actions/runs/39273938096), `scientific-gate` job `118133629741`, from source head `8085403037cc115ebc1f4ee19ca27bcad914f012`, completed **success**. The dedicated source tests were run through `tests/test_chapter2_two_origins_predictability_20261019.py`; no original Model3 reproductive kernel or registered Chapter 2 result was changed.
- Reproducible read-only reader: [`scripts/audit_two_origins_predictability_20261019.py`](../scripts/audit_two_origins_predictability_20261019.py). It rebuilds the **identical** six exposed synthetic source genotypes and two exposed island environments from [technical v3](CHAPTER2_TWO_ORIGINS_TECHNICAL_V3_READOUT_20261019.md). It calls original native `reproduce()` and calculates Poisson founding probability but **never draws new arrival/fate outcomes, advances a state, fits a classifier or opens a new scientific cohort**.
- For each of the six candidates `i` in each island `j`, `p_ij = 0.8 × [1 − exp(−Λ_ij)]`. First factor is the independent source-neutral arrival opportunity; second is one-update establishment, conditional on arrival, calculated from all maternal/paternal/selfing returns.
- **Six source lineages equally weighted** within each artificial island. They are all the source genotypes already observed in PR #610, not a distribution of real mainland lineages and not six geological island replicates.

| Artificial island | Source-blind baseline expected Brier | Source-aware oracle expected Brier | Absolute expected improvement | Improvement / baseline |
| --- | ---: | ---: | ---: | ---: |
| No functional visitors, budget B4.5 | **0.23576612** | **0.22576432** | **0.01000180** | **4.242255%** |
| Functional visitors, budget B8 | **0.18068746** | **0.17966137** | **0.00102608** | **0.567877%** |

Values copied from the verified Actions log and rounded to eight decimal places; do not infer extra precision from display. A source-aware “oracle” already knows each genotype's correct establishment probability and is the **mathematical best possible** forecast under the stated Bernoulli model. It is **not trained**, so the table does **not** measure a fitted prediction model's out-of-sample performance or establish generalization to new source populations.

## Mathematical identity / interpretation

Let `Y_i` indicate whether candidate lineage `i` successfully arrives and establishes within the model's first reproduction update, `p_i=P(Y_i=1 | full source genotype, island, fixed arrival protocol)`, and `μ=mean_i p_i`. Under the known Bernoulli event law:

```
Brier_source_oracle = mean_i [p_i(1-p_i)]
Brier_constant      = μ(1-μ)
Brier_constant − Brier_source_oracle = Var_i(p_i).
```

Hence `R2_Brier_oracle = Var_i(p_i)/[μ(1−μ)]` is the fraction of **binary first-establishment fate variance** explainable *in expectation* by complete source-state information under this artificial source distribution and known environmental setting. This is the law of total variance, not newly discovered evolutionary dynamics, a causal A-specific fraction, a p-value, or a proof of precise individual future fate.

The difference illustrates exactly why three statements must be kept separate:

1. **Trait affects fitness/establishment probability:** the Model3 source p increases markedly with A in the no-visitor mode, when I and the rest of the founding genotype are held in a controlled intervention.
2. **Source-informed probability forecast:** there is measurable but **limited potential** improvement in the expected binary establishment prediction within the six exposed genotypes.
3. **Individual lineage fate is deterministic:** **NOT supported**; chance arrival, Poisson recruits and later survival remain stochastic. A sharp probability response does not turn a one-shot 0/1 outcome into a near-certain event.

At the first initial-establishment census, the source-informed classification accuracy ceiling under 0–1 loss differs from proper-score improvement: a perfect oracle can still do little better than predicting the majority class when all `p_i` are on the same side of 0.5. The proper Brier/log loss and calibration should remain primary. These computations do **not** address the distinct question of whether the *across-archipelago mean* trait composition is reproducible upon many complete resets or whether *post-establishment floral evolution* is intrinsically less predictable.

## Research decision

The prior exclusive claim “A is a nearly deterministic imported establishment filter; I is unpredictable in-situ evolution” must **not** be adopted as a conclusion from six technical founders. Existing [technical A- vs I-expression interventions](CHAPTER2_TWO_ORIGINS_TECHNICAL_V3_READOUT_20261019.md) suggest strong **conditional A dependence** of initial expected seed-settlement success in one no-visitor regime, while the present source-conditional oracle comparison shows little expected individual-fate prediction gain with incomplete arrival probability. Neither settles a general difference in the source of natural island floral syndromes.

The next study is specified, but NOT initiated, in the [held-out source×island admission plan](CHAPTER2_TWO_ORIGINS_PREDICTION_ADMISSION_20261019.md): new source-genotype and island namespaces, preselected controls (A-only/I-only/full), explicit arrival probabilities, held-out lineage/island predictive scores, source×island inference, trait-neutral establishment, evolution-clamped conditions, and genuine assembly interactions or a prominently labelled noninteracting null. External Chapter1 empirical data cannot be retroactively interpreted as within-species contrasts.
