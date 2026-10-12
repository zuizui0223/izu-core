# Chapter 2: cohort identity and the remaining original-source replay gap

**2026-10-11 — source-backed provenance clarification and retrospective analysis boundary.** The confirmed four-setting assurance result from [PR #411](https://github.com/zuizui0223/izu-core/pull/411) remains intact. The completed tempo accounting from [PR #478](https://github.com/zuizui0223/izu-core/pull/478) retains its own cohort and scope. This note corrects the loose label "old #411 full-gradient replay": the existing sequence replay auditor actually targets the earlier sustained-isolation **discovery** population.

This clarification authorizes no new biological campaign, visitor histories, parameter changes, event thresholds, bootstrap or hypothesis test. Any subsequent replay must reproduce a specified original task under verified source identity. Archive availability is a separate retrieval question; a recovered bundle requires cohort-specific admission before scientific use.

The [#478 accounting report](CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_20261011.md) and its [current-evidence addendum](../data/results/chapter2_four_question_current_evidence_addendum_20261011.json) remain byte-identical because the [accounting receipt](../data/results/chapter2_tempo_realization_receipt_20261011.json) records their hashes. Their "old #411" wording is corrected here without rewriting that evidence package. In particular, `old_411_full_gradient_replay_completed_here: false` is a historical label for the discovery-auditor objective not completed by the tempo analysis. It is **not evidence that the actual #411 generality cohort lacks raw data or source-gradient evidence**. Current retrieval/admission findings belong to the [separate identity status](../data/results/chapter2_source_replay_identity_status_20261011.json).

## 1. Four distinct populations

| Frozen cohort | Environmental and demographic seeds | Original tasks and founders | Scientific question |
|---|---|---|---|
| **2026-10-05 sustained-isolation discovery** | Visitor histories **76001–76064**; eight nested repeats **7101–7108** | Two settings × mutation **0/.01** × near/far × 64 × 8 = **4,096 trajectories**. All three traits have standing diploid variation. | Founder-relative A/I sequence and the additional far-minus-near sequence. |
| **2026-10-06 independent sequence/fixed-assurance confirmation** | Histories **26100601–26100664**; repeats **26101601–26101608** | **2,048 evolving far-only sequence cases**, spanning two settings and both mutation rates; **2,048 fixed-A near/far cases** at mutation .01. Sequence founders retain A variation; fixed-A founders have both A homologs reset to .5. | Independent founder-relative sequence confirmation and a separate fixed-assurance necessity test. |
| **Four-setting assurance generality, PR #411** | Histories **26110601–26110664**; repeats **26111601–26111608** | Four settings × fixed/evolving × near/far × 64 × 8 = **8,192 main cases** at mutation .01; **256** zero-mutation structural controls. Both modes start with both A homologs set to .5. | Whether investment decline requires assurance evolution, and whether assurance evolution attenuates near–far investment divergence. |
| **Completed visitor-tempo cohort, PR #476/#478** | Sixteen synthetic profiles **48271001–48271016**; four repeats **49271001–49271004** | Delayed/prior × cost 0/.5 × mutation 0/.01 × abrupt/gradual × 16 × 4 = **1,024 cases**, each with 400 updates. A has standing variation. | Effects of prescribed functional-optimum chronology and accounting of its realized inherited differences. |

All use founder seed **74001** and 48 underlying diploid draws with generating means X=I=A=.5 and SD .15. The assurance resets above are substantive differences: sharing the founder seed does not make all founding populations identical. The discovery's two settings jointly change selfing timing and cost: **delayed/cost .5** versus **prior/cost 0**. The generality design adds delayed control and pollen discount; the tempo design separately crosses timing and direct cost.

Sources: [discovery design](../data/design/model3_persistent_isolation_20261005.json), [confirmation design](../data/design/chapter2_1005_confirmatory_replication_20261006.json), [generality design](../data/design/chapter2_assurance_generality_20261006.json), [generality founder implementation](../scripts/run_chapter2_assurance_generality.py), and [tempo design](../data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json). Repeats remain nested within environmental histories; cases, years and individuals are not extra independent environmental replicates.

## 2. Name the question and required source correctly

The [original genome-replay auditor](../scripts/audit_chapter2_sequence_source_genome_replay_20261011.py) restricts histories to 76001–76064, repeats to 7101–7108, settings to the two discovery settings, and mutation to **.01**. Its domain is therefore **2,048 discovery trajectories**, half the complete original design. The [paired companion](../scripts/audit_chapter2_sequence_paired_original_replay_20261011.py) is narrower: history76001, delayed/costly, both arms and all eight repeats, with a bounded prefix sufficient for that history's already recorded crossings.

The paired discovery question requires its actual evolving near/far populations. The independent confirmatory sequence campaign contains **no evolving-near arm**. Its fixed-A near cases have different assurance founders and expression rules, so they cannot supply that comparator. The confirmation bundle can support retrospective analysis of its own far-arm sequence; it cannot close the discovery's paired gap. Its [runner](../scripts/run_chapter2_1005_confirmatory_replication.py) makes this task distinction explicit.

The [paired-order analysis](CHAPTER2_PAIRED_ORDER_ESTIMANDS_DECISION_20261011.md) distinguishes change relative to each population's founders from emergence of additional far-minus-near divergence. Neither baseline measures the first mutation or automatically identifies selection onset. The [original timing declaration](../data/design/model3_temporal_order_diagnostic_20261005.json) fixes change .05 sustained for 20 updates, five-update near-simultaneous tolerance, sensitivities .025/.10, and explicit unreached-event censoring. These definitions remain unchanged.

## 3. What the original raw files can recover

The [persistent runner](../scripts/run_model3_persistent_isolation.py) and [full-mutation runner](../scripts/run_model3_full_mutation.py) save a **1,001 × 10 trace**: census, three trait means, three variances and three distinct-allele counts. Complete diploid allele arrays are retained only at **t0, t200, t400 and t1000**. JSON case files contain task identities and NPZ SHA256 receipts. The confirmation runner uses the same trace/checkpoint storage; its JSON receipts do not supply annual genomes or parentage.

Verified checkpoint genotypes can support local reproductive calculations at t0, t200 and t400 with the corresponding original visitor state. Census t1000 has no subsequent reproductive exposure in the original 1,000-update record. Annual selection profiles and retained-parent accounting require exact original replay; annual means and variances cannot reconstruct individual genotypes.

By contrast, the [tempo runner](../scripts/run_chapter2_sequence_abrupt_gradual_functional_loss_20261011.py) retained annual adult IDs, diploid genomes and child/parent IDs. Its [completed accounting](CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_20261011.md) covers all **409,600 updates** directly from preserved records. That closes the tempo accounting gate while leaving the original discovery replay question separate. Four visitor types persist in the tempo experiment; its cumulative-pollen match applies to a fixed clonal calibration, not to every evolved population.

## 4. Archive and source admission

The earlier single-case auditor compares task identity, raw-file SHA256, the replayed trace prefix and available genome checkpoints. Full source/runtime identity and complete-cohort admission require additional evidence: authenticate the recovered bundle, verify its complete task set and receipts, match `sources.json` to `sources.zip`, identify the executed biological sources/configuration and numerical runtime, and reproduce the full trace and checkpoints. Runtime agreement alone cannot replace output identity. The [historical summarizer](../scripts/summarize_model3_persistent_order.py) provides the stronger source/task/completeness precedent.

**Filename blocker repaired:** the verifier used `base.with_suffix(".json")` on an extensionless key containing `u0.01`. This truncates `.01_h76001_r7101_far`, producing `persistent_core_assurance_cost_u0.json`; the NPZ path suffers the same error. The two-line repair appends each extension to the complete key. Before the repair, both realistic near/far filename regressions failed; afterward the full reader test file passed **18 tests**. These include rejection of wrong tasks, changed byte hashes, trace differences, changed or missing checkpoints, and a post-200 exposure check using the replay module's selected history provider. The archive fixtures are explicitly synthetic engineering inputs. Passing them repairs the reader; original discovery cases admitted by this task remain **zero**.

**Exposure routing matters after update200.** The full-mutation far experiment switches to near visitors after its first 200 updates. Persistent-far exposure remains isolated for all 1,000 updates. The unchanged full-mutation **near** cases are valid persistent-study references; its far cases are a different experiment. Early prefix tests cannot detect this routing mistake. The [stream registry](../scripts/model3_island/randomness.py) and [history generator](../scripts/model3_island/history.py) also require preserving original stream identities and draw order. Instrumentation must not consume biological RNG streams.

### Retrieval findings on 2026-10-11

The [archive inventory](../data/results/chapter2_source_replay_archive_inventory_20261011.json) records the exact retrieval scope, observation times and source references. All **50 artifact identities** in the preserved public-archive manifest match current GitHub metadata, including sizes and digests. This authenticates the metadata correspondence; the Actions ZIP bytes and their internal case receipts were not inspected in this task.

| Actual archived campaign | Raw shards present and unexpired | Raw artifact bytes | Source run |
|---|---:|---:|---|
| Independent confirmation | 16/16 | 140,185,877 | [37390991122](https://github.com/zuizui0223/izu-core/actions/runs/37390991122) |
| PR #411 assurance generality | 32/32 | 377,932,059 | [37458098483](https://github.com/zuizui0223/izu-core/actions/runs/37458098483) |

The generality run's aggregate conclusion is `cancelled`, while all 32 shard jobs and its summary job completed successfully. Its artifact source is commit `20e8e2d6ad25545b9cb4941305343b5f010a58f4`; use that source identity rather than assuming the final PR head executed the archived tasks. Raw expiry dates are November 4 for confirmation and November 5 for generality, as recorded in the timestamped metadata snapshot.

Two related saved packages were recovered and inspected. The nine-member `chapter2_original_evolved_pollen_service_full_evidence_20261010.zip` matches its preserved SHA256 `57a5008fa216b00d9f446865a8dc491b4ddaaf8b56096d633bdc4fa27369eb2c`; it contains derived #457 audit JSON and scripts, with no raw NPZ case pairs. The two-member `chapter2-old-history-preflight-receipt.zip` contains a design-only plan and an engineering cost receipt using history26110601. Neither supplies the discovery's original 76001-series cases. The separate status record retains their exact sizes, hashes and member lists.

The strongest named discovery lead is `model3_replenishment_evolution_20261005.zip`, **763,914,318 bytes**, SHA256 `37bd0bd312734715392add19f424696121fbe88517dfa784d8e702173ec71b6c`. Its [preserved receipt](../data/results/model3_replenishment_archive_20261005.json) declares 13,312 archived cases, and its [design](../data/design/model3_replenishment_evolution_20261005.json) explicitly reuses the **2,048 original positive-mutation near/far endpoints**. This makes it a candidate for the current reader domain; membership remains an inference until the ZIP directory and bytes are recovered. It cannot by itself establish the mutation-zero half of the discovery design. The [older full-mutation package](MODEL3_FULL_MUTATION_RESULTS_20261004.md), 224,236,731 bytes, is another named lead for the near references. No original discovery archive locator was resolved in the inspected sources; universal absence has not been established.

## 5. Four estimands and the demographic boundary

For maternal outcross return F, paternal return P and viable selfed return S, the native source gives

\[
W_i=\tfrac12F_i+\tfrac12P_i+S_i,\qquad
m_t=\frac{\sum_iW_i g_i}{\sum_iW_i}.
\]

The expected pre-mutation shift `m_t - gbar_t` is a **source transmission covariance**, conditional on positive local recruitment. It incorporates the existing heterogeneous genotype distribution and associations among traits. The local focal assay instead perturbs one adult's two homologs by ±.005 and recalculates `log(W_i)`. Its finite-population response is also distinct from the fixed-resident rare-mutant invasion gradient described in the [four-setting manuscript](CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md).

The [native transition](../scripts/model3_island/population.py) can additionally supply the retained parental-pair mean q. The observed change decomposes into expected response, parental sampling and the combined segregation/mutation remainder. These terms are retrospective accounting along realized states, not separate causal mediation effects. Temporal precedence supplies no intervention on inherited order.

The [original base configuration](../data/design/model3_ch2_bridge_20260927.json) has survival **0** and plant seed supply **0**. Thus no retained-adult or immigrant-genotype mixture is needed: resident candidates are Poisson with mean `sum(W)`, capped at K48. However, the complete discovery design includes a documented extinction in delayed/costly, mutation-zero cases: [paired persistence is 511/512](MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md). Historical curves average available repeats at each census. When that set changes, a pooled change includes both within-repeat genetic change and a **changing-repeat-composition term**. Extinct means remain undefined; occupancy and paired denominators must accompany every pooled comparison.

## 6. Bounded next step

Once the named archives are admitted, a complete annual covariance and retained-parent accounting pass would advance the original mechanism question without new biology. Full discovery-design closure requires all 4,096 trajectories; a .01-only pass must retain its explicit 2,048-case scope. Preserve every history, late crossing and non-crossing outcome. The confirmation cohort can be analyzed under its own identity if that is the admitted source.

Full annual all-adult gradients require a separate computational and recording contract: at N48, two traits and two perturbations require up to **192 additional native reproduction calls per update**. The current eight-adult rank sample and early window cannot establish a population-wide onset date. Continuous profiles, source covariance, availability and the unchanged genomic crossings should be reported separately; the existing ±.02 gradient display band supplies no new biological event threshold. No current replay feasibility finding changes the frozen #411 conclusion or the completed tempo result.
