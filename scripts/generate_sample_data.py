from __future__ import annotations

import csv
from pathlib import Path

MAPPING = {
    "ID": ["ID.AM-1", "ID.GV-1", "ID.RA-1"],
    "PR": ["PR.AC-1", "PR.DS-1", "PR.IP-1"],
    "DE": ["DE.CM-1", "DE.DP-1", "DE.AE-1"],
    "RS": ["RS.RP-1", "RS.CO-1", "RS.AN-1"],
    "RC": ["RC.RP-1", "RC.IM-1", "RC.CO-1"],
}

MATURITY = ["Initial", "Developing", "Defined", "Managed", "Optimized"]


def build_rows(shift: int) -> list[dict]:
    rows = []
    for i, (function, subs) in enumerate(MAPPING.items()):
        for j, sub in enumerate(subs):
            rows.append(
                {
                    "function": function,
                    "category": sub.split(".")[1].split("-")[0],
                    "subcategory": sub,
                    "maturity": MATURITY[min(4, (i + j + shift) % 5)],
                    "weight": 1 + ((i + j) % 2) * 0.5,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["function", "category", "subcategory", "maturity", "weight"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    out = Path("sample_data")
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "2025Q1.csv", build_rows(0))
    write_csv(out / "2025Q2.csv", build_rows(1))
    print("Generated sample_data/2025Q1.csv and sample_data/2025Q2.csv")
