# Reporting + formula details

## Rollup levels
Quarterly reporting computes these levels:
- `subcategory`: direct mapped maturity score
- `category`: weighted mean of subcategories in category
- `function`: weighted mean of categories in function
- `overall`: weighted mean for the quarter

## Delta report
For each level, delta report outputs:
- `from_score`
- `to_score`
- `delta = to_score - from_score`

## Formula config (`config/formula_config.json`)
Formula weights are applied before rollup:

`effective_weight = uploaded_weight * function_weight * category_weight * subcategory_weight`

Lookup keys:
- `function_weights`: by `function` (example `ID`)
- `category_weights`: by `function.category` (example `ID.AM`)
- `subcategory_weights`: by `subcategory` (example `ID.AM-1`)

If a key is absent, multiplier defaults to `1.0`.

## Snapshot storage
Two kinds of SQLite persistence are used:
1. Raw quarterly ingestion (`snapshots`, `records`).
2. Quarterly rollup snapshots (`rollup_snapshots`) generated at upload time and queryable via `/snapshots/{quarter}`.
