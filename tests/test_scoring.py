from app.scoring import apply_maturity_scores, build_delta_report, build_quarter_report
import pandas as pd


CONFIG = {
    "maturity_scale": {
        "Initial": 1,
        "Developing": 2,
        "Defined": 3,
        "Managed": 4,
        "Optimized": 5,
    },
    "default_weight": 1.0,
    "rounding": 2,
}


def test_apply_and_aggregate():
    df = pd.DataFrame(
        [
            {"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-1", "maturity": "Defined", "weight": 1},
            {"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-2", "maturity": "Managed", "weight": 1},
        ]
    )
    scored = apply_maturity_scores(df, CONFIG)
    report = build_quarter_report(scored, CONFIG)
    assert report["category"]["score"].iloc[0] == 3.5


def test_delta():
    base = pd.DataFrame(
        [{"quarter": "2025Q1", "function": "ID", "category": "AM", "subcategory": "ID.AM-1", "maturity": "Defined", "weight": 1}]
    )
    nextq = pd.DataFrame(
        [{"quarter": "2025Q2", "function": "ID", "category": "AM", "subcategory": "ID.AM-1", "maturity": "Optimized", "weight": 1}]
    )
    r1 = build_quarter_report(apply_maturity_scores(base, CONFIG), CONFIG)
    r2 = build_quarter_report(apply_maturity_scores(nextq, CONFIG), CONFIG)
    delta = build_delta_report(r1, r2)
    assert delta["subcategory"]["delta"].iloc[0] == 2
