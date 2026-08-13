"""
Génère le dashboard HTML autonome de monitoring OTP à partir de :
- otp_dashboard_data.json (produit par model/train_model.py)
- backlog/backlog_modele_otp.csv (backlog produit géré par le BA)

Usage:
    python build_dashboard.py
"""

import csv
import json
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
DATA_PATH = HERE / "otp_dashboard_data.json"
BACKLOG_PATH = HERE.parent / "backlog" / "backlog_modele_otp.csv"
TEMPLATE_PATH = HERE / "dashboard_template.html"
OUT_PATH = HERE / "otp_monitoring_dashboard.html"


def load_backlog_summary():
    with open(BACKLOG_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    status_counts = Counter(r["statut"] for r in rows)
    priority_counts = Counter(r["priorite_moscow"] for r in rows)
    return {
        "total_items": len(rows),
        "by_status": dict(status_counts),
        "by_priority": dict(priority_counts),
        "items": [
            {"id": r["id"], "titre": r["titre"], "statut": r["statut"],
             "priorite": r["priorite_moscow"], "release": r["release_cible"]}
            for r in rows
        ],
    }


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        dashboard_data = json.load(f)

    backlog_summary = load_backlog_summary()

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = template.replace(
        "/*__DASHBOARD_DATA__*/", json.dumps(dashboard_data, ensure_ascii=False)
    ).replace(
        "/*__BACKLOG_SUMMARY__*/", json.dumps(backlog_summary, ensure_ascii=False)
    )

    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard généré -> {OUT_PATH}")


if __name__ == "__main__":
    main()
