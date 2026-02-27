from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def load_scoring_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def apply_maturity_scores(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    maturity_scale = config["maturity_scale"]
    default_weight = float(config.get("default_weight", 1.0))

    out = df.copy()
    if "weight" not in out.columns:
        out["weight"] = default_weight
    out["weight"] = out["weight"].fillna(default_weight).astype(float)
    out["maturity_score"] = out["maturity"].map(maturity_scale)
    if out["maturity_score"].isna().any():
        unknown = out.loc[out["maturity_score"].isna(), "maturity"].unique().tolist()
        raise ValueError(f"Unknown maturity levels: {unknown}")
    out["maturity_score"] = out["maturity_score"].astype(float)
    return out


def weighted_group(df: pd.DataFrame, by: list[str], rounding: int = 2) -> pd.DataFrame:
    grouped = (
        df.groupby(by, as_index=False)
        .apply(lambda g: (g["maturity_score"] * g["weight"]).sum() / g["weight"].sum(), include_groups=False)
        .rename(columns={None: "score"})
    )
    grouped["score"] = grouped["score"].round(rounding)
    return grouped


def build_quarter_report(df: pd.DataFrame, config: dict) -> dict[str, pd.DataFrame]:
    rounding = int(config.get("rounding", 2))
    subcategory = df[["function", "category", "subcategory", "maturity_score", "weight"]].copy()
    subcategory = subcategory.rename(columns={"maturity_score": "score"})
    subcategory["score"] = subcategory["score"].round(rounding)

    category = weighted_group(df, ["function", "category"], rounding=rounding)
    function = weighted_group(df, ["function"], rounding=rounding)
    overall = weighted_group(df, ["quarter"], rounding=rounding)

    return {
        "subcategory": subcategory.sort_values(["function", "category", "subcategory"]),
        "category": category.sort_values(["function", "category"]),
        "function": function.sort_values(["function"]),
        "overall": overall,
    }


def build_delta_report(from_report: dict[str, pd.DataFrame], to_report: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    result: dict[str, pd.DataFrame] = {}
    for level in ["subcategory", "category", "function", "overall"]:
        left = from_report[level].copy()
        right = to_report[level].copy()
        if level == "subcategory":
            keys = ["function", "category", "subcategory"]
        elif level == "category":
            keys = ["function", "category"]
        elif level == "function":
            keys = ["function"]
        else:
            keys = []

        left = left.rename(columns={"score": "from_score"})
        right = right.rename(columns={"score": "to_score"})
        if keys:
            merged = left[keys + ["from_score"]].merge(right[keys + ["to_score"]], on=keys, how="outer")
        else:
            merged = pd.DataFrame(
                {
                    "from_score": [left["from_score"].iloc[0] if not left.empty else None],
                    "to_score": [right["to_score"].iloc[0] if not right.empty else None],
                }
            )

        merged["delta"] = (merged["to_score"] - merged["from_score"]).round(2)
        result[level] = merged.sort_values(keys) if keys else merged

    return result
