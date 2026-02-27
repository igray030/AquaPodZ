import pandas as pd

from app.formulas import apply_weight_formula
from app.scoring import apply_maturity_scores, build_quarter_report


SCORING_CONFIG = {
    "maturity_scale": {"Initial": 1, "Developing": 2, "Defined": 3, "Managed": 4, "Optimized": 5},
    "default_weight": 1.0,
    "rounding": 2,
}

FORMULA_CONFIG = {
    "default_weight": 1.0,
    "function_weights": {"ID": 2.0},
    "category_weights": {"ID.AM": 1.5},
    "subcategory_weights": {"ID.AM-1": 2.0},
}


def test_effective_weight_formula_application():
    raw = pd.DataFrame(
        [
            {"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-1", "maturity": "Defined", "weight": 1.0},
            {"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-2", "maturity": "Managed", "weight": 1.0},
        ]
    )
    weighted = apply_weight_formula(raw, FORMULA_CONFIG)

    assert weighted.loc[0, "weight"] == 6.0  # 1 * 2 * 1.5 * 2
    assert weighted.loc[1, "weight"] == 3.0  # 1 * 2 * 1.5 * 1


def test_rollup_weighted_mean_math():
    raw = pd.DataFrame(
        [
            {"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-1", "maturity": "Defined", "weight": 1.0},
            {"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-2", "maturity": "Managed", "weight": 1.0},
        ]
    )
    weighted = apply_weight_formula(raw, FORMULA_CONFIG)
    scored = apply_maturity_scores(weighted, SCORING_CONFIG)
    report = build_quarter_report(scored, SCORING_CONFIG)

    # ((3*6) + (4*3)) / (6+3) = 30 / 9 = 3.33
    assert report["category"].iloc[0]["score"] == 3.33
    assert report["function"].iloc[0]["score"] == 3.33
    assert report["overall"].iloc[0]["score"] == 3.33
