from __future__ import annotations

import io
import os
from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .exporters import to_excel_bytes, to_pdf_bytes
from .formulas import apply_weight_formula, load_formula_config
from .models import Record, RollupSnapshot, Snapshot
from .scoring import apply_maturity_scores, build_delta_report, build_quarter_report, load_scoring_config

app = FastAPI(title="NIST CSF Quarterly Maturity API")
CONFIG_PATH = Path(os.getenv("SCORING_CONFIG", "config/protiviti_scoring.json"))
FORMULA_CONFIG_PATH = Path(os.getenv("FORMULA_CONFIG", "config/formula_config.json"))


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


def _read_upload(file: UploadFile) -> pd.DataFrame:
    content = file.file.read()
    if file.filename and file.filename.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(content))
    else:
        df = pd.read_csv(io.BytesIO(content))
    required = {"function", "category", "subcategory", "maturity"}
    missing = required - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {sorted(missing)}")
    return df


def _snapshot_to_df(snapshot: Snapshot) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "quarter": snapshot.quarter,
                "function": r.function,
                "category": r.category,
                "subcategory": r.subcategory,
                "maturity": r.maturity_label,
                "maturity_score": r.maturity_score,
                "weight": r.weight,
            }
            for r in snapshot.records
        ]
    )


def _get_snapshot_or_404(db: Session, quarter: str) -> Snapshot:
    snap = db.scalar(select(Snapshot).where(Snapshot.quarter == quarter))
    if not snap:
        raise HTTPException(status_code=404, detail=f"Quarter {quarter} not found")
    return snap


def _store_rollup_snapshots(db: Session, quarter: str, report: dict[str, pd.DataFrame]) -> None:
    db.execute(delete(RollupSnapshot).where(RollupSnapshot.quarter == quarter))
    for level, frame in report.items():
        for _, row in frame.iterrows():
            db.add(
                RollupSnapshot(
                    quarter=quarter,
                    level=level,
                    function=row.get("function"),
                    category=row.get("category"),
                    subcategory=row.get("subcategory"),
                    score=float(row["score"]),
                )
            )


@app.post("/upload")
def upload_quarter(
    quarter: str = Query(..., description="Quarter label e.g. 2025Q1"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    config = load_scoring_config(CONFIG_PATH)
    formula_config = load_formula_config(FORMULA_CONFIG_PATH)
    df = _read_upload(file)
    df["quarter"] = quarter
    weighted = apply_weight_formula(df, formula_config)
    scored = apply_maturity_scores(weighted, config)

    existing = db.scalar(select(Snapshot).where(Snapshot.quarter == quarter))
    if existing:
        db.delete(existing)
        db.flush()

    snapshot = Snapshot(quarter=quarter, source_file=file.filename or "upload")
    db.add(snapshot)
    db.flush()

    for _, row in scored.iterrows():
        db.add(
            Record(
                snapshot_id=snapshot.id,
                function=str(row["function"]),
                category=str(row["category"]),
                subcategory=str(row["subcategory"]),
                maturity_label=str(row["maturity"]),
                maturity_score=float(row["maturity_score"]),
                weight=float(row.get("weight", 1.0)),
            )
        )

    report = build_quarter_report(scored, config)
    _store_rollup_snapshots(db, quarter, report)

    db.commit()
    return {"message": "snapshot stored", "quarter": quarter, "rows": len(scored)}


@app.get("/quarters")
def list_quarters(db: Session = Depends(get_db)):
    quarters = db.scalars(select(Snapshot.quarter).order_by(Snapshot.quarter)).all()
    return {"quarters": quarters}


@app.get("/snapshots/{quarter}")
def get_rollup_snapshot(quarter: str, db: Session = Depends(get_db)):
    rows = db.scalars(select(RollupSnapshot).where(RollupSnapshot.quarter == quarter).order_by(RollupSnapshot.level)).all()
    if not rows:
        raise HTTPException(status_code=404, detail=f"No rollup snapshots found for {quarter}")
    payload = [
        {
            "quarter": r.quarter,
            "level": r.level,
            "function": r.function,
            "category": r.category,
            "subcategory": r.subcategory,
            "score": r.score,
        }
        for r in rows
    ]
    return {"items": payload}


@app.get("/reports/{quarter}")
def quarter_report(quarter: str, db: Session = Depends(get_db)):
    config = load_scoring_config(CONFIG_PATH)
    snap = _get_snapshot_or_404(db, quarter)
    report = build_quarter_report(_snapshot_to_df(snap), config)
    return {k: v.to_dict(orient="records") for k, v in report.items()}


@app.get("/reports/delta")
def delta_report(from_quarter: str, to_quarter: str, db: Session = Depends(get_db)):
    config = load_scoring_config(CONFIG_PATH)
    from_snap = _get_snapshot_or_404(db, from_quarter)
    to_snap = _get_snapshot_or_404(db, to_quarter)
    from_report = build_quarter_report(_snapshot_to_df(from_snap), config)
    to_report = build_quarter_report(_snapshot_to_df(to_snap), config)
    deltas = build_delta_report(from_report, to_report)
    return {k: v.to_dict(orient="records") for k, v in deltas.items()}


@app.get("/export/excel/{quarter}")
def export_excel(quarter: str, db: Session = Depends(get_db)):
    config = load_scoring_config(CONFIG_PATH)
    snap = _get_snapshot_or_404(db, quarter)
    report = build_quarter_report(_snapshot_to_df(snap), config)
    payload = to_excel_bytes(report, title=f"Quarterly maturity report - {quarter}")
    return Response(
        payload,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=report_{quarter}.xlsx"},
    )


@app.get("/export/pdf/{quarter}")
def export_pdf(quarter: str, db: Session = Depends(get_db)):
    config = load_scoring_config(CONFIG_PATH)
    snap = _get_snapshot_or_404(db, quarter)
    report = build_quarter_report(_snapshot_to_df(snap), config)
    payload = to_pdf_bytes(report, title=f"Quarterly maturity report - {quarter}")
    return Response(payload, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=report_{quarter}.pdf"})


@app.get("/export/excel/delta")
def export_delta_excel(from_quarter: str, to_quarter: str, db: Session = Depends(get_db)):
    config = load_scoring_config(CONFIG_PATH)
    from_report = build_quarter_report(_snapshot_to_df(_get_snapshot_or_404(db, from_quarter)), config)
    to_report = build_quarter_report(_snapshot_to_df(_get_snapshot_or_404(db, to_quarter)), config)
    payload = to_excel_bytes(build_delta_report(from_report, to_report), title=f"Delta report {from_quarter} -> {to_quarter}")
    return Response(
        payload,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=delta_{from_quarter}_{to_quarter}.xlsx"},
    )


@app.get("/export/pdf/delta")
def export_delta_pdf(from_quarter: str, to_quarter: str, db: Session = Depends(get_db)):
    config = load_scoring_config(CONFIG_PATH)
    from_report = build_quarter_report(_snapshot_to_df(_get_snapshot_or_404(db, from_quarter)), config)
    to_report = build_quarter_report(_snapshot_to_df(_get_snapshot_or_404(db, to_quarter)), config)
    payload = to_pdf_bytes(build_delta_report(from_report, to_report), title=f"Delta report {from_quarter} -> {to_quarter}")
    return Response(payload, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=delta_{from_quarter}_{to_quarter}.pdf"})
