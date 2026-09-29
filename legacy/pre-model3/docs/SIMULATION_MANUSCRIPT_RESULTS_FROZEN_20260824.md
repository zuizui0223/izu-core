# Simulation manuscript Results — frozen 2026-08-24

## Scope

This Results layer is restricted to the **simulation study with qualitative external island-system challenges**. It uses only already-frozen model outputs and the predeclared 13-system state challenge. No field bundle, empirical `V_k × E_k` mapping, external-system parameter fitting, seed selection from observed island outcomes, or post-hoc mechanism addition is used in the primary result.

## 1. One frozen architecture generates several island-response state classes

The frozen ABM generated three qualitatively distinct recurrent response classes without system-specific retuning: within-run branching, same-direction responses, and strong buffering in a subset of lineages. In the original v12 residual block, mixed-sign responses occurred in **5 of 12 matched runs (0.4167)**. Consequently, **7 of 12 runs (0.5833)** were non-mixed even while initial lineage trait-position heterogeneity remained present. Same-direction response is therefore a genuine output class of the heterogeneous model, but it is not evidence that lineages began from uniform states.

Strong sign-level buffering was produced by the frozen network-context route. In an independently seeded matched block, local support converted a support-OFF reproductive decline to a non-negative response in **16 of 96 eligible contrasts (0.1667)**. The same intervention worsened **11 of 96 contrasts (0.1146)**. Thus network context has genuine buffering capacity, but its stable role is a **bidirectional branch allocator**, not a universally protective buffer.

Autonomous assurance occupied a different synthetic region. In its independent block, assurance attenuated decline magnitude in **207 of 216 service-decline lineages (0.9583)** but produced **0 of 216** sign rescues. A broadened support envelope likewise produced **0 of 525** strong assurance sign rescues. The robust property of the implemented assurance route is therefore attenuation of reproductive decline, not reliable reversal of response sign.

## 2. Pre-existing lineage functional position is the minimal identified branch generator

The v12 residual-factor ablation isolated the source of two-sided within-run branching after the four tested v11 downstream modifiers were fixed OFF. In the original frozen block, the full residual model had a mixed-sign run fraction of **0.4167** and a mean within-run branching balance of **0.2569**. Removing initial trait-position heterogeneity reduced both quantities to **0**, whereas individually removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity did not collapse branching.

The result replicated in the prespecified independent block with seed `90260825`. The independently seeded full residual model again produced mixed-sign responses in **0.4167** of matched runs, with mean within-run branching balance **0.2917**. Removing initial trait-position heterogeneity again reduced mixed-sign runs and within-run branching balance to **0**, with **44 paired lineage sign changes**. By contrast, removing trait-adjustment heterogeneity retained a mixed-sign fraction of **0.4167** and mean within-run balance **0.2847**, while removing assurance-ceiling heterogeneity retained **0.4167** and **0.2917**, respectively.

Across the two independently seeded frozen blocks, pre-existing lineage position in the standardized functional trait space is therefore the only tested residual factor whose removal eliminates within-run response-sign branching. This identifies a **minimal synthetic generator inside the declared ABM**; it does not identify any particular measured floral trait as the corresponding real-world axis.

## 3. Downstream mechanisms modify branch identity differently

The v11 factorial showed that local support changed **105 of 288 paired branch signs (0.3646)** when ablated, whereas partner effectiveness changed **13 of 288 (0.0451)**. Dependency heterogeneity changed none, and assurance responsiveness changed one paired sign. These results separate branch **generation** from branch **allocation**: two-sided branching persists without the tested downstream modifiers, but local support can substantially redistribute which lineages occupy which response branch.

The independent network-context robustness block sharpened that interpretation. Among lineages with declining global opportunity and a support-OFF reproductive decline, support ON improved decline magnitude in **85 of 96 cases (0.8854)**, crossed the zero boundary in **16 of 96**, and worsened **11 of 96**. Network context is therefore capable of strong sign rescue, but the same route can also make an already-negative response more negative.

Autonomous assurance differs qualitatively. Across saturation values 1, 2 and 3, sign rescue remained **0** while magnitude attenuation occurred in **71/75 (0.9467)**, **73/76 (0.9605)** and **63/65 (0.9692)** service-decline lineages, respectively. No transition to a robust sign-buffering regime was detected in the declared saturation envelope.

## 4. Observed state is only asymmetrically informative about mechanism

The forward model can generate several response states, but the inverse problem is not one-to-one. Using mixed-sign branching as a diagnostic of initial trait-position heterogeneity gives **specificity 1.0** but **sensitivity 0.4167**. Thus observing mixed-sign branching is highly informative among the tested residual mechanisms, whereas not observing it does not exclude heterogeneous initial lineage states.

The reverse inference from same-direction response is weak. A non-mixed response is guaranteed when initial trait heterogeneity is removed, but it also occurs in **0.5833** of heterogeneity-ON runs. Treating same-direction response as evidence for trait uniformity therefore gives a false-positive rate of **0.5833** and specificity of only **0.4167**.

Strong sign rescue is similarly asymmetric. Against the tested assurance route, network-context sign rescue has **specificity 1.0** but sensitivity only **0.1667**. Magnitude attenuation has the opposite problem: assurance attenuation sensitivity is **0.9583**, but network context also attenuates **0.8854** of eligible declines, leaving specificity against network context at only **0.1146**. A smaller decline is therefore a poor discriminator between these two implemented routes.

The key inference is not that each observed state reveals its mechanism. Rather, **different state observations carry very different diagnostic information**.

## 5. The external island challenge broadens state-space validity without becoming a fit

The global screening layer contains **54 geographic/system units**, from which **13 strict external systems** were admitted to the frozen state challenge. Of these, **11 are generative state challenges**: three branching systems, six same-direction propagation systems and two buffering/alternative systems. All 11 are qualitatively covered or sign-compatible with an already-frozen synthetic state class. No ABM rerun, parameter retuning, mechanism addition or state-vocabulary change was performed for these new systems.

The remaining two strict systems are deliberately not counted as successful generative targets. Puerto Rico–Mona *Guaiacum* is retained as a **reproductive-axis-decoupling constraint**, because its observed reproductive axes should not be collapsed into a single buffering label. Dominica *Heliconia* remains a **retained falsification**: the frozen signed-position projection did not predict the observed direction, and the mapping was not retuned after failure.

The external challenge therefore supports a limited but useful statement: **one frozen minimal architecture spans several recurrent island-response state classes**. It does not support the stronger claim that one mechanism has been empirically identified across 13 island systems.

## 6. Protected falsifications define the claim boundary

Four negative results are part of the primary evidence rather than defects to be tuned away. First, removing initial trait-position heterogeneity must not leave mixed-sign within-run branching in the declared residual gate; it did not in either frozen block. Second, network context cannot be described as a universal buffer because matched worsenings are present. Third, the implemented assurance route cannot be described as a robust strong sign buffer because sign rescue was absent in the independent and broadened blocks. Fourth, the failed Dominica signed-position projection remains a protected external falsification.

A future predeclared external state outside every frozen state class is likewise defined in advance as a **state-space miss**. Such a miss would motivate a new separately frozen question, not retroactive extension of the current model.

## Result-level conclusion

The frozen ABM supports a state-dependent view of island pollination response. A common upstream functional perturbation can yield different downstream signs because lineages enter the perturbation from different positions in functional trait space. Local network context then reallocates branches and can sometimes rescue or worsen a decline, whereas autonomous assurance robustly changes magnitude without robustly reversing sign. The external island series shows that these response-state classes recur across independent systems, while the identifiability analysis shows why state compatibility alone cannot establish real-world causal mechanism.

The primary simulation result is therefore complete without new field data. Additional simulation is justified only by a new prespecified question, not by a desire to increase favorable frequencies or rescue a known external failure.
