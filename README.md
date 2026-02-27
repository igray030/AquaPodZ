# AquaPodZ - NIST CSF Quarterly Maturity App

FastAPI + Streamlit web application to ingest quarterly NIST CSF maturity data, apply configurable Protiviti-style rollup math, store quarterly snapshots in SQLite, and export reports.

## What this includes
- Quarterly CSV/XLSX uploads.
- SQLite/Postgres row-level snapshot persistence (`snapshots`, `records`).
- SQLite rollup snapshot persistence per quarter (`rollup_snapshots`) for quarterly runs.
- Configurable maturity scoring (`config/protiviti_scoring.json`).
- Configurable weight formula (`config/formula_config.json`).
- Quarterly reports (function/category/subcategory/overall).
- Quarter-over-quarter delta reports.
- Excel + PDF exports.
- Streamlit dashboard with interactive charts.
- Unit/API tests and GitHub Actions workflow.

## Local run
1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```
2. Generate sample data:
```bash
python scripts/generate_sample_data.py
```
3. Start API:
```bash
uvicorn app.main:app --reload
```
4. Start UI (new terminal):
```bash
streamlit run streamlit_app/app.py
```

## Environment variables
- `DATABASE_URL` (default: `sqlite:///./aquadodz.db`)
- `SCORING_CONFIG` (default: `config/protiviti_scoring.json`)
- `FORMULA_CONFIG` (default: `config/formula_config.json`)
- `API_BASE_URL` for Streamlit backend URL (default: `http://localhost:8000`)

## Weight formula behavior
Weights are applied before scoring:

`effective_weight = uploaded_weight * function_weight * category_weight * subcategory_weight`

Where:
- `uploaded_weight` comes from the upload file (`weight` column; defaults from formula config if missing).
- `function_weight` is looked up by function key (e.g. `ID`).
- `category_weight` is looked up by `function.category` key (e.g. `ID.AM`).
- `subcategory_weight` is looked up by full subcategory key (e.g. `ID.AM-1`).

Any missing lookup defaults to `1.0`.

## Main endpoints
- `POST /upload?quarter=2025Q1`
- `GET /quarters`
- `GET /reports/{quarter}`
- `GET /reports/delta?from_quarter=2025Q1&to_quarter=2025Q2`
- `GET /snapshots/{quarter}` (SQLite-stored rollup snapshot rows)
- `GET /export/excel/{quarter}`
- `GET /export/pdf/{quarter}`
- `GET /export/excel/delta?from_quarter=...&to_quarter=...`
- `GET /export/pdf/delta?from_quarter=...&to_quarter=...`

## CI
GitHub Actions workflow is in `.github/workflows/tests.yml` and runs sample-data generation + `pytest` on PRs.
