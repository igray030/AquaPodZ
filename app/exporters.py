from __future__ import annotations

from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def to_excel_bytes(report: dict[str, pd.DataFrame], title: str) -> bytes:
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        for level, df in report.items():
            df.to_excel(writer, sheet_name=level[:31], index=False)
        meta = pd.DataFrame({"title": [title]})
        meta.to_excel(writer, sheet_name="meta", index=False)
    return bio.getvalue()


def _table_for_df(df: pd.DataFrame):
    data = [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f77b4")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def to_pdf_bytes(report: dict[str, pd.DataFrame], title: str) -> bytes:
    bio = BytesIO()
    doc = SimpleDocTemplate(bio, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    for level, df in report.items():
        elements.append(Paragraph(level.capitalize(), styles["Heading2"]))
        elements.append(_table_for_df(df.head(100)))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    return bio.getvalue()
