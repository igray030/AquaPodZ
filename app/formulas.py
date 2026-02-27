from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def load_formula_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def apply_weight_formula(df: pd.DataFrame, formula_config: dict) -> pd.DataFrame:
    out = df.copy()
    default_weight = float(formula_config.get("default_weight", 1.0))

    if "weight" not in out.columns:
        out["weight"] = default_weight
    out["weight"] = out["weight"].fillna(default_weight).astype(float)

    function_weights = formula_config.get("function_weights", {})
    category_weights = formula_config.get("category_weights", {})
    subcategory_weights = formula_config.get("subcategory_weights", {})

    out["function_weight"] = out["function"].map(function_weights).fillna(1.0).astype(float)
    out["category_key"] = out["function"].astype(str) + "." + out["category"].astype(str)
    out["category_weight"] = out["category_key"].map(category_weights).fillna(1.0).astype(float)
    out["subcategory_weight"] = out["subcategory"].map(subcategory_weights).fillna(1.0).astype(float)
    out["weight"] = out["weight"] * out["function_weight"] * out["category_weight"] * out["subcategory_weight"]

    return out.drop(columns=["function_weight", "category_key", "category_weight", "subcategory_weight"])
