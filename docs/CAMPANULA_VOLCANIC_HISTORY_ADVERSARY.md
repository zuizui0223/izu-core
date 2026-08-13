# Campanula pre-1986 volcanic-history adversary

## Question

Can the three adopted island-side *Campanula* channels be approximated by recent volcanic disturbance or time since the latest source-supported eruptive event, rather than by the staged response profile?

This is a deliberately narrow history adversary. It does not treat latitude or island order as a history variable.

## No future-information leakage

The history snapshot is frozen at **1986-01-01**, before the first publication in the retained Izu *Campanula* evidence programme.

Consequently:

- the 1986 Izu-Oshima eruption is not allowed to explain the retained biological observations;
- the 2000 Miyakejima eruption is not allowed to explain them;
- only eruptions strictly before the cutoff enter the history table.

The source lock is `data/design/izu_volcanic_history_pre1986.csv`.

## Source-locked pre-cutoff events

| island | latest retained event | elapsed years at 1986 cutoff |
|---|---|---:|
| Oshima | 1974 magmatic eruption | 12 |
| Toshima | latest eruption reported as 9100–4000 yr BP | 4036–9136 |
| Niijima | 886–887 Mukaiyama eruption | 1099 |
| Kozushima | 838 Tenjozan eruption | 1148 |
| Miyake | 1983 fissure eruption | 3 |
| Hachijo | 1605 Nishiyama land eruption | 381 |

JMA is used for Oshima, Niijima, Kozushima, Miyake and Hachijo; GSJ is used for Toshima. Hachijo's 1606 event is not used because the source describes it as an offshore eruption of uncertain position, whereas the 1605 event is a documented land eruption.

Toshima is not assigned an invented midpoint. The workflow runs two sensitivity cases using the young and old endpoints of the reported interval.

## Candidate history responses

Each retained channel compares:

- `null`;
- `island_order_cline`;
- `volcanic_recency_cline` using `log1p(years since latest pre-cutoff event)`;
- `recent_100y_disturbance`, for which only Oshima and Miyake are positive;
- the predeclared `oshima_to_toshima_step`.

Composite diagnostics compare the same continuous/history axis for flower size and outcrossing while retaining the predeclared autonomous-reproduction step.

## Frozen result

Workflow run `31250136732` completed successfully and uploaded artifact `9019734850`.

### Toshima young endpoint: 4036 years

| composite | AICc |
|---|---:|
| **two-stage order hybrid** | **5.12** |
| two-stage recent-100-y hybrid | 27.48 |
| two-stage volcanic-recency hybrid | 29.51 |
| single island-order cline | 30.25 |
| null | 36.28 |
| single recent-100-y disturbance | 51.29 |
| single volcanic-recency cline | 54.93 |

### Toshima old endpoint: 9136 years

| composite | AICc |
|---|---:|
| **two-stage order hybrid** | **5.12** |
| two-stage recent-100-y hybrid | 27.48 |
| two-stage volcanic-recency hybrid | 29.74 |
| single island-order cline | 30.25 |
| null | 36.28 |
| single recent-100-y disturbance | 51.29 |
| single volcanic-recency cline | 55.26 |

The ranking is therefore insensitive to the unresolved Toshima eruption-age interval.

### Channel-level reading

For the young-endpoint case:

| channel | order AICc | volcanic-recency AICc | recent-100-y AICc | Oshima→Toshima step AICc |
|---|---:|---:|---:|---:|
| flower length | 31.78 | 41.28 | 39.01 | 39.01 |
| outcrossing midpoint | **-10.20** | 4.70 | 4.93 | 1.42 |
| autonomous capsule set | 8.67 | 8.95 | 7.35 | **-16.46** |

Flower length remains underpowered (`n=4`; null AICc 29.94), so no single-channel shape is declared resolved from AICc alone.

The source-locked volcanic-recency axes do not reproduce the smooth outcrossing erosion or the sharp autonomous-reproduction transition. Retaining the autonomous step but replacing the two continuous channels with volcanic recency worsens the composite by roughly 24.4–24.6 AICc units.

## What this does not establish

This result weakens one explicit volcanic-history alternative; it does not reject history in general. Time since the latest eruption is not the same as:

- spatial eruption footprint or severity;
- vegetation reset and successional state;
- founder number or effective population size;
- source-population identity;
- inter-island gene flow;
- colonisation sequence;
- habitat availability;
- pollinator causation.

The next history layer must therefore use lineage-specific population-genetic evidence where it is source-supported, and must not turn qualitative phylogeographic statements into invented numeric covariates.
