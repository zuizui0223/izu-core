# Chapter 2 interaction-kernel derivation

Updated: 2026-08-28
Status: exact analytic reading of the frozen model; no new simulation or empirical fit

## Decision

The current matching/service model does admit a community-interaction-kernel representation, but only with one important qualification.

For a fixed plant state, the sign of the island-minus-mainland service contrast is exactly the sign of a community-kernel difference. In the implemented endpoint model, however, weak trait adjustment can produce different final plant states under the two pollinator trajectories. The exact response coordinate is therefore a **trajectory-conditioned composite kernel**, not the shortcut `K_island(x0) - K_mainland(x0)` evaluated at the unchanged starting state.

This derivation exposes existing model structure. It does not add a fitted mechanism, a new simulation result or evidence about natural frequencies.

## 1. Fixed-state community kernel

For environment `E`, plant functional state `x`, and extant pollinator `j`, define

```text
k_Ej(x) = a_Ej exp[-((x - p_Ej) / b_Ej)^2],
```

where `p_Ej` is pollinator position, `b_Ej` is its breadth and `a_Ej` is `0.82` for a replacement partner and `1` otherwise. The implemented bounds do not alter this expression because the product already lies in `[0,1]` for the declared parameter domain.

Under the fixed visit budget, the community kernel is

```text
K_E(x) = 0                                      if N_E = 0,
K_E(x) = (1 / N_E) sum_j k_Ej(x)               otherwise.
```

The service map is

```text
S_E(x) = f_sigma[K_E(x)]
f_sigma(z) = 1 - exp(-sigma z).
```

For `sigma > 0`, `f_sigma` is strictly increasing because

```text
f'_sigma(z) = sigma exp(-sigma z) > 0.
```

Consequently, if plant state and saturation are fixed,

```text
sign{S_I(x) - S_M(x)} = sign{K_I(x) - K_M(x)}.
```

This makes `G(x) = K_I(x) - K_M(x)` an exact fixed-state sign coordinate. Partner turnover changes the number, positions, breadths and replacement penalties of the component kernels and therefore deforms `G` rather than merely shifting one average effect.

## 2. Exact endpoint coordinate with trait adjustment

The active geometry model updates plant state when current service is below `0.45`. Let

```text
Phi_E,T(x0; omega_E)
```

denote the final state produced from starting position `x0` by environment-specific pollinator trajectory `omega_E`. Define the composite endpoint kernel

```text
calK_E(x0; omega_E)
    = K_E,T[Phi_E,T(x0; omega_E)].
```

The exact per-realization response coordinate is then

```text
G_omega(x0)
    = calK_I(x0; omega_I) - calK_M(x0; omega_M),

sign DeltaS_omega(x0) = sign G_omega(x0).
```

Thus the starting position is the input coordinate, while the realized mainland and island community trajectories jointly determine both the final kernel shape and the state at which each endpoint kernel is evaluated.

### Rejected shortcut

`K_I(x0) - K_M(x0)` is not the exact endpoint response when trait adjustment moves the two trajectories to different final plant states. It becomes exact if trait adjustment is zero, if both final states equal `x0`, or if `K_E` is explicitly redefined as the trajectory-conditioned composite `calK_E` above.

### Aggregation boundary

The exact sign identity is per realization. The published mean geometry is

```text
mean_omega { f_sigma[calK_I] - f_sigma[calK_M] }.
```

Because `f_sigma` is nonlinear, its sign cannot generally be replaced by the sign of a difference between mean kernels. The frozen `21 × 96` analysis remains the evidence for the mean response geometry; the analytic identity explains its coordinate system but does not replace that analysis.

## 3. Interpretation of the five mechanistic coordinates

| Coordinate | Exact model role | Allowed interpretation |
|---|---|---|
| Turnover regime | Changes kernel components through partner loss, arrival, breadth, position and replacement status | Deforms the available response surface within the declared synthetic design |
| Starting state | Supplies `x0` to both matched environment trajectories | Locates a lineage on the response coordinate; does not determine its branch alone |
| Realized community | Determines `omega_E`, final community components and `Phi_E,T` | Changes the response geometry and explains much of realization-level variation |
| Local filtering | Applies stochastic support restriction and within-support weight reallocation | Can change branch identity; is not a scalar reduction of global service |
| Assurance | Maps upstream effective service into reproduction through a separate downstream route | Can attenuate magnitude; sign preservation is conditional, not a universal theorem |

## 4. Local filtering as an operator

For a plant opportunity row with weights `w_j = k_j / N`, let `L_(s,h)` denote the implemented local-context operation. It:

1. independently filters plant rows, pollinators and feasible pairs at stress `s`;
2. intersects those support masks without repairing empty or partnerless outcomes;
3. rescales every retained positive row to its original global opportunity total; and
4. at context strength `h`, redistributes that retained row total through positive affinity multipliers.

With partner-quality multipliers `q_j`, the local effective kernel is

```text
K_E^L = sum_j [L_(s,h)(w)]_j q_j,
S_E^L = 1 - exp(-sigma K_E^L).
```

`L_(s,h)` is therefore a stochastic support-and-reallocation operator. It can remove an entire row or particular partners, but for a retained row it conserves the pre-context row budget while redistributing mass among retained partners. Calling it a uniform scalar shrinkage would be incorrect. The frozen directionality analysis, not the operator definition alone, establishes that positive branches were lost more readily than negative branches were rescued in the tested envelope.

## 5. Assurance is downstream of the kernel

For fixed pollinator dependency `d` and fixed autonomous-route contribution `U`, reproduction is

```text
R(S) = 1 - (1 - dS)(1 - U)
     = U + d(1 - U)S.
```

If `d > 0` and `U < 1`, this map is strictly increasing, so a fixed downstream route preserves the sign of a service contrast while attenuating or amplifying its magnitude.

The implemented assurance state is dynamic and can differ between environments. Sign preservation is therefore not an unconditional theorem for the full model. The valid evidence is the frozen sensitivity result: across the declared `0.5×–4×` envelope, there were zero sign rescues among 580 eligible service declines. Assurance should consequently remain a downstream magnitude modifier **within the tested envelope**, not a general mathematical prohibition on sign rescue.

## 6. HOW, proximal WHY and ultimate-WHY ceiling

The kernel representation unifies the mechanistic HOW:

```text
turnover -> community-kernel deformation
         -> state- and trajectory-conditioned service
         -> local support/reallocation
         -> downstream reproduction.
```

It supplies a model-conditional proximal WHY: the same broad interaction reorganization can produce different response signs because lineages occupy different starting positions relative to different realized community kernels, with non-additive and local-context effects.

It does not supply the ultimate WHY for why a particular island assembled its species pool, why a lineage arrived with a particular state, or why a historical turnover process occurred. Those causes remain outside Chapter 2.

## 7. Reproducible identity audit

`scripts/audit_chapter2_interaction_kernel.py` checks the implemented identities using deterministic hand-built fixtures. It uses no random draws, parameter search or additional scientific simulation. The frozen output is `data/results/chapter2_interaction_kernel_audit_frozen_20260828.json`.

The audit verifies:

- exact equality of implemented service and the monotone saturation of the mean-match kernel;
- exact equality at trajectory-conditioned endpoints;
- per-realization sign equivalence between service contrast and composite-kernel difference; and
- sign preservation for a fixed downstream assurance route.

The audit deliberately records the rejected same-`x0` shortcut, nonlinear aggregation boundary, non-scalar local-filtering boundary and dynamic-assurance boundary.
