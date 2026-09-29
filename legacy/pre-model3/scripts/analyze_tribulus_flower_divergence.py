#!/usr/bin/env python3
"""Reanalyse source-native Tribulus petal-length divergence conservatively.

Two layers are kept separate:

1. **author-model reproduction**: approximate the released lme4 models with
   statsmodels MixedLM using the exact source fields and filtering rules encoded
   in ``data/design/tribulus_flower_source_mapping.json``;
2. **ID-level independence sensitivity**: average repeated flower rows within
   the source-defined ``ID`` grouping unit, then fit HC3 OLS models.  This is
   intentionally conservative because the README states that ``ID`` can denote
   a herbarium voucher or a field site, not necessarily one biological plant.

The script reports mainland/island divergence, climate adjustment, continent
fixed-effect sensitivity, Galapagos leverage, and Galapagos-versus-other-island
contrasts.  Flower size is never recoded as pollinator dependency.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


REQUIRED_COLUMNS = (
    "ID",
    "year_collected",
    "continent",
    "mainland_island",
    "galapagos_other",
    "island_group",
    "flower_num",
    "petal_length",
    "Bio_1",
    "Bio_4",
    "Bio_12",
    "Bio_15",
)
CLIMATE_COLUMNS = ("Bio_1", "Bio_4", "Bio_12", "Bio_15")


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def normalize_group(value: object) -> str:
    text = normalize_text(value).casefold()
    if text in {"continent", "mainland"}:
        return "continent"
    if text == "island":
        return "island"
    return text


def galapagos_binary(value: object) -> str | None:
    text = normalize_text(value).casefold()
    if not text or text in {"na", "nan", "none"}:
        return None
    return "galapagos" if "galapagos" in text else "other_islands"


def load_mapping(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_source_file(input_dir: Path, filename: str) -> Path:
    candidates = sorted(input_dir.rglob(filename))
    if len(candidates) != 1:
        raise ValueError(
            f"expected exactly one {filename!r} under {input_dir}, found {len(candidates)}"
        )
    return candidates[0]


def import_analysis_stack():
    try:
        import pandas as pd
        import statsmodels.formula.api as smf
    except ImportError as error:  # pragma: no cover - dedicated workflow installs deps
        raise RuntimeError(
            "Tribulus analysis requires pandas and statsmodels; install them in the analysis environment"
        ) from error
    return pd, smf


def source_dataframe(path: Path):
    pd, _ = import_analysis_stack()
    frame = pd.read_csv(path)
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"Tribulus source is missing required columns: {missing}")
    frame = frame.copy()
    frame["mainland_island_clean"] = frame["mainland_island"].map(normalize_group)
    invalid = sorted(
        set(frame["mainland_island_clean"].dropna().astype(str)) - {"continent", "island"}
    )
    if invalid:
        raise ValueError(f"unexpected mainland_island source values: {invalid}")
    frame["is_island"] = (frame["mainland_island_clean"] == "island").astype(int)
    frame["continent_clean"] = frame["continent"].map(normalize_text)
    frame["galapagos_binary"] = frame["galapagos_other"].map(galapagos_binary)
    for column in ("year_collected", "petal_length", *CLIMATE_COLUMNS):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def composition(frame) -> dict[str, Any]:
    pd, _ = import_analysis_stack()
    def counts(series):
        values = series.fillna("<NA>").astype(str).value_counts(dropna=False)
        return {str(key): int(value) for key, value in values.items()}

    id_status = (
        frame.groupby("ID", dropna=False)["mainland_island_clean"]
        .agg(lambda values: ";".join(sorted(set(map(str, values)))))
    )
    return {
        "n_rows": int(len(frame)),
        "n_unique_ID": int(frame["ID"].nunique(dropna=True)),
        "rows_by_mainland_island": counts(frame["mainland_island_clean"]),
        "IDs_by_mainland_island": counts(id_status),
        "rows_by_continent": counts(frame["continent_clean"]),
        "rows_by_galapagos_other": counts(frame["galapagos_binary"]),
        "rows_by_island_group": counts(frame["island_group"]),
        "n_missing_petal_length": int(frame["petal_length"].isna().sum()),
        "n_missing_Bio_4": int(frame["Bio_4"].isna().sum()),
    }


def fit_mixedlm(formula: str, data, group_column: str = "ID"):
    _, smf = import_analysis_stack()
    model = smf.mixedlm(formula, data=data, groups=data[group_column])
    errors = []
    for method in ("lbfgs", "powell", "cg"):
        try:
            result = model.fit(reml=False, method=method, disp=False)
            if getattr(result, "converged", True):
                return result, method, errors
            errors.append(f"{method}: did not converge")
        except Exception as error:  # pragma: no cover - source dependent
            errors.append(f"{method}: {error!r}")
    raise RuntimeError("MixedLM did not converge: " + "; ".join(errors))


def fixed_effect_record(result, *, coefficient: str, label: str) -> dict[str, Any]:
    estimate = float(result.fe_params[coefficient])
    se = float(result.bse_fe[coefficient])
    return {
        "label": label,
        "coefficient": coefficient,
        "estimate_mm": estimate,
        "se_mm": se,
        "ci_95_mm": [estimate - 1.959963984540054 * se, estimate + 1.959963984540054 * se],
        "n_rows": int(result.nobs),
        "converged": bool(getattr(result, "converged", True)),
    }


def mixedlm_author_reproduction(frame) -> dict[str, Any]:
    pd, _ = import_analysis_stack()
    prep = frame.dropna(subset=["petal_length", "Bio_4", "year_collected", "ID"]).copy()
    formula_unadjusted = "petal_length ~ is_island + year_collected"
    initial, initial_method, initial_errors = fit_mixedlm(formula_unadjusted, prep)
    residuals = pd.Series(initial.resid, index=prep.index)
    keep = residuals.abs() < 5
    filtered = prep.loc[keep].copy()
    filtered_result, filtered_method, filtered_errors = fit_mixedlm(
        formula_unadjusted, filtered
    )

    climate_complete = prep.dropna(subset=list(CLIMATE_COLUMNS)).copy()
    formula_climate = (
        "petal_length ~ is_island + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15"
    )
    climate_result, climate_method, climate_errors = fit_mixedlm(
        formula_climate, climate_complete
    )

    island_only = climate_complete[
        climate_complete["mainland_island_clean"] == "island"
    ].dropna(subset=["galapagos_binary"]).copy()
    island_only["is_galapagos"] = (
        island_only["galapagos_binary"] == "galapagos"
    ).astype(int)
    gal_result = None
    gal_method = None
    gal_errors: list[str] = []
    if island_only["is_galapagos"].nunique() == 2:
        gal_result, gal_method, gal_errors = fit_mixedlm(
            "petal_length ~ is_galapagos + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15",
            island_only,
        )

    removed_indices = list(prep.index[~keep])
    removed = prep.loc[~keep, ["ID", "flower_num", "petal_length"]].copy()
    return {
        "model_family": "approximate_cross_software_reproduction_of_released_lme4_models",
        "unadjusted_initial": {
            **fixed_effect_record(initial, coefficient="is_island", label="island_minus_continent"),
            "fit_method": initial_method,
            "fit_attempt_notes": initial_errors,
        },
        "unadjusted_residual_filter": {
            "rule": "absolute initial-model residual strictly below 5 mm",
            "n_rows_before": int(len(prep)),
            "n_rows_after": int(len(filtered)),
            "n_rows_removed": int((~keep).sum()),
            "n_unique_ID_removed": int(removed["ID"].nunique()),
            "removed_IDs": sorted(map(str, removed["ID"].unique())),
            "removed_source_indices": [int(index) for index in removed_indices],
        },
        "unadjusted_filtered": {
            **fixed_effect_record(
                filtered_result, coefficient="is_island", label="island_minus_continent"
            ),
            "fit_method": filtered_method,
            "fit_attempt_notes": filtered_errors,
        },
        "bioclimate_adjusted": {
            **fixed_effect_record(
                climate_result, coefficient="is_island", label="island_minus_continent"
            ),
            "fit_method": climate_method,
            "fit_attempt_notes": climate_errors,
        },
        "galapagos_vs_other_islands_bioclimate": (
            {
                **fixed_effect_record(
                    gal_result,
                    coefficient="is_galapagos",
                    label="galapagos_minus_other_islands",
                ),
                "fit_method": gal_method,
                "fit_attempt_notes": gal_errors,
            }
            if gal_result is not None
            else {"status": "not_estimable_from_source_levels"}
        ),
    }


def id_level_frame(frame):
    pd, _ = import_analysis_stack()
    usable = frame.dropna(subset=["ID", "petal_length"]).copy()
    first_columns = [
        "mainland_island_clean",
        "is_island",
        "continent_clean",
        "galapagos_binary",
        "island_group",
        "year_collected",
        *CLIMATE_COLUMNS,
    ]
    conflicts = {}
    for column in first_columns:
        n_unique = usable.groupby("ID")[column].nunique(dropna=True)
        bad = n_unique[n_unique > 1]
        if not bad.empty:
            conflicts[column] = sorted(map(str, bad.index))
    if conflicts:
        raise ValueError(f"source-defined ID has conflicting grouping/covariate values: {conflicts}")
    grouped = usable.groupby("ID", as_index=False).agg(
        petal_length=("petal_length", "mean"),
        n_flower_rows=("petal_length", "size"),
        **{column: (column, "first") for column in first_columns},
    )
    return grouped


def ols_record(formula: str, data, *, coefficient: str, label: str) -> dict[str, Any]:
    _, smf = import_analysis_stack()
    result = smf.ols(formula, data=data).fit(cov_type="HC3")
    if coefficient not in result.params:
        return {
            "status": "not_estimable",
            "label": label,
            "formula": formula,
            "n_ID": int(result.nobs),
            "design_rank": int(result.model.rank),
            "design_columns": list(result.params.index),
        }
    estimate = float(result.params[coefficient])
    se = float(result.bse[coefficient])
    ci = [float(value) for value in result.conf_int().loc[coefficient].tolist()]
    return {
        "status": "estimated",
        "label": label,
        "formula": formula,
        "coefficient": coefficient,
        "estimate_mm": estimate,
        "hc3_se_mm": se,
        "hc3_ci_95_mm": ci,
        "n_ID": int(result.nobs),
        "design_rank": int(result.model.rank),
        "design_columns": list(result.params.index),
        "r_squared": float(result.rsquared),
    }


def id_level_sensitivities(frame) -> dict[str, Any]:
    IDs = id_level_frame(frame)
    base = IDs.dropna(subset=["petal_length", "year_collected"]).copy()
    climate = base.dropna(subset=list(CLIMATE_COLUMNS)).copy()
    output = {
        "independent_unit": (
            "source-defined ID grouping unit; README says herbarium voucher when applicable or field site for field-collected samples"
        ),
        "n_ID_total": int(len(IDs)),
        "n_ID_continent": int((IDs["is_island"] == 0).sum()),
        "n_ID_island": int((IDs["is_island"] == 1).sum()),
        "flower_rows_per_ID": {
            "median": float(IDs["n_flower_rows"].median()),
            "maximum": int(IDs["n_flower_rows"].max()),
        },
        "year_adjusted": ols_record(
            "petal_length ~ is_island + year_collected",
            base,
            coefficient="is_island",
            label="ID_mean_island_minus_continent",
        ),
        "bioclimate_adjusted": ols_record(
            "petal_length ~ is_island + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15",
            climate,
            coefficient="is_island",
            label="ID_mean_island_minus_continent",
        ),
    }

    climate_continent = climate[climate["continent_clean"].astype(str).str.len() > 0].copy()
    output["bioclimate_plus_continent_fixed_effects"] = ols_record(
        "petal_length ~ is_island + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15 + C(continent_clean)",
        climate_continent,
        coefficient="is_island",
        label="ID_mean_island_minus_continent_with_continent_FE",
    )

    without_gal = climate[climate["galapagos_binary"] != "galapagos"].copy()
    output["bioclimate_excluding_galapagos"] = ols_record(
        "petal_length ~ is_island + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15",
        without_gal,
        coefficient="is_island",
        label="ID_mean_island_minus_continent_excluding_Galapagos",
    )

    island_only = climate[climate["is_island"] == 1].dropna(
        subset=["galapagos_binary"]
    ).copy()
    island_only["is_galapagos"] = (
        island_only["galapagos_binary"] == "galapagos"
    ).astype(int)
    output["galapagos_vs_other_islands_bioclimate"] = ols_record(
        "petal_length ~ is_galapagos + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15",
        island_only,
        coefficient="is_galapagos",
        label="ID_mean_Galapagos_minus_other_islands",
    )

    continent_groups = {}
    for continent, group in climate.groupby("continent_clean"):
        if group["is_island"].nunique() != 2 or len(group) < 6:
            continue
        continent_groups[str(continent)] = ols_record(
            "petal_length ~ is_island + year_collected + Bio_1 + Bio_4 + Bio_12 + Bio_15",
            group,
            coefficient="is_island",
            label=f"ID_mean_island_minus_continent_within_{continent}",
        )
    output["within_continent_bioclimate"] = continent_groups
    return output


def author_anchor_comparison(
    mapping: Mapping[str, Any], reproduction: Mapping[str, Any]
) -> dict[str, Any]:
    anchors = mapping["author_model_anchors"]
    return {
        "unadjusted": {
            "author_mainland_mm": anchors["unadjusted_filtered_mixed_model"][
                "reported_emmean_mainland_mm"
            ],
            "author_island_mm": anchors["unadjusted_filtered_mixed_model"][
                "reported_emmean_island_mm"
            ],
            "author_difference_mm": anchors["unadjusted_filtered_mixed_model"][
                "reported_emmean_island_mm"
            ]
            - anchors["unadjusted_filtered_mixed_model"]["reported_emmean_mainland_mm"],
            "python_mixedlm_island_coefficient_mm": reproduction["unadjusted_filtered"][
                "estimate_mm"
            ],
        },
        "bioclimate": {
            "author_mainland_mm": anchors["bioclimate_mixed_model"][
                "reported_emmean_mainland_mm"
            ],
            "author_island_mm": anchors["bioclimate_mixed_model"][
                "reported_emmean_island_mm"
            ],
            "author_difference_mm": anchors["bioclimate_mixed_model"][
                "reported_emmean_island_mm"
            ]
            - anchors["bioclimate_mixed_model"]["reported_emmean_mainland_mm"],
            "python_mixedlm_island_coefficient_mm": reproduction["bioclimate_adjusted"][
                "estimate_mm"
            ],
        },
        "galapagos_vs_other": {
            "author_galapagos_mm": anchors["galapagos_vs_other_islands_bioclimate"][
                "reported_emmean_galapagos_mm"
            ],
            "author_other_islands_mm": anchors[
                "galapagos_vs_other_islands_bioclimate"
            ]["reported_emmean_other_islands_mm"],
            "author_difference_mm": anchors[
                "galapagos_vs_other_islands_bioclimate"
            ]["reported_emmean_galapagos_mm"]
            - anchors["galapagos_vs_other_islands_bioclimate"][
                "reported_emmean_other_islands_mm"
            ],
            "python_mixedlm_galapagos_coefficient_mm": (
                reproduction["galapagos_vs_other_islands_bioclimate"].get(
                    "estimate_mm"
                )
            ),
        },
    }


def analyse(source: Path, mapping_path: Path) -> dict[str, Any]:
    mapping = load_mapping(mapping_path)
    frame = source_dataframe(source)
    reproduction = mixedlm_author_reproduction(frame)
    ID_sensitivity = id_level_sensitivities(frame)
    return {
        "schema_version": "1.0",
        "status": "tribulus_source_native_flower_divergence_reanalysis_complete",
        "source_id": mapping["source_id"],
        "dataset_doi": mapping["dataset_doi"],
        "article_doi": mapping["article_doi"],
        "source_file": source.name,
        "source_file_git_blob_sha": mapping["source_file_git_blob_sha"],
        "composition": composition(frame),
        "author_model_reproduction": reproduction,
        "author_anchor_comparison": author_anchor_comparison(mapping, reproduction),
        "ID_level_independence_sensitivity": ID_sensitivity,
        "effect_registry_eligible": False,
        "reading": (
            "The same Tribulus source supports a weak unadjusted island-continent flower-size contrast, a larger "
            "environment-adjusted contrast in the released author model, and a strong Galapagos-versus-other-island "
            "contrast. ID-level, continent-adjusted, and Galapagos-exclusion sensitivities are reported separately "
            "to show how much the headline island effect depends on repeated flower rows, source-pool composition, "
            "and Galapagos leverage."
        ),
        "claim_boundary": mapping["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir", type=Path, default=Path("artifacts/tribulus_dryad")
    )
    parser.add_argument(
        "--filename", default="Tribulus_flower_data_clean.csv"
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=Path("data/design/tribulus_flower_source_mapping.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/tribulus_analysis/analysis.json"),
    )
    args = parser.parse_args()
    source = find_source_file(args.input_dir, args.filename)
    result = analyse(source, args.mapping)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    print(result["composition"])
    print(args.output)


if __name__ == "__main__":
    main()
