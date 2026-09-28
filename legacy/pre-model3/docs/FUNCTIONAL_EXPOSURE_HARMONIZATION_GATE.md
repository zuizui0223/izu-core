# Functional-exposure harmonization gate

## Decision

The next cross-system blocker is **construct harmonization**, not lack of candidate rows.

The Izu reference exposure is not generic visitor diversity. Hiraiwa & Ushimaru (2024) define pollinator `FDQ` as abundance-weighted Rao's quadratic entropy over pollinator proboscis length:

```text
FDQ = sum_i sum_j p_i p_j |L_i - L_j|
```

where `p` is pollinator relative abundance and `L` is proboscis length.

Therefore species richness, Shannon diversity, Gini-Simpson diversity, visitor identity, binary Bombus/Apis presence, or a coarse guild count are not valid drop-in replacements.

## Current panels

| panel | abundance | quantitative pollination trait | Rao-Q exposure | direct dependency same unit | exact joint |
|---|---|---|---|---|---|
| Izu Hiraiwa 2024 | yes | yes: proboscis length | yes | no | no |
| Seychelles Thespesia | yes | no | no | yes | no |
| Puerto Rico–Mona Guaiacum | yes | no | no | no exact tree linkage | no |
| Balearic Malva | yes | no | no repeated gradient | yes | no |
| Canary Lotus | yes | no | no | yes | no |

Only the Izu source currently passes the Izu-compatible FDQ gate, and it lacks the direct dependency treatment.

## Minimum admission contract

An external panel can be called Izu-compatible functional exposure only if all are available prospectively:

1. visitor relative abundance inside a declared exposure unit;
2. a quantitative pollination-relevant trait for every admitted visitor taxon/group;
3. a source-native or prospectively frozen trait map chosen independently of reproductive outcomes;
4. Rao-Q calculated under the same formula and direction;
5. repeated exposure units rather than one pooled population total.

Direct reproductive dependency is a separate gate. Having bagging or breeding treatments does not repair a missing functional-exposure trait.

## Consequence for Issue #91

The Campanula pilot already requires visitor identity/contact and observation effort. To make the future joint cell genuinely comparable to the 2024 Izu exposure axis, visitor identity must also link to a frozen proboscis-length/functional-trait table. Known taxa may reuse source-locked measurements when the identity is exact; new/unresolved taxa remain outside FDQ until a defensible trait value is available.

This does not add a new biological response treatment. It adds the trait metadata needed to calculate the exposure variable that the programme is already using.

## External-system consequence

Seychelles and Guaiacum remain useful joint architectures, but neither may be turned into FDQ by renaming richness or Shannon diversity. Reopen them for harmonized analysis only if quantitative visitor traits can be recovered without outcome-guided selection.

For vertebrate-dominated systems, proboscis length is not assumed to be a universal homologous trait. Those systems stay outside the Izu-compatible FDQ analysis unless a separate, prospectively justified common construct is developed and validated.

## Source lock

- Hiraiwa & Ushimaru 2024, Functional Ecology, DOI `10.1111/1365-2435.14527`
- source data/code DOI `10.6084/m9.figshare.25025000.v1`
- frozen GitHub artifact digest `sha256:dce1cf210e3674722b39d4b01ff47709c78e642eefd207228a6c5ac5bc6b4037`
