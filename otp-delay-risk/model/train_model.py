"""
Entraînement et monitoring du modèle de prédiction du risque de retard OTP
============================================================================
Ce script illustre le rôle de Business Analyst du modèle OTP :
- entraînement d'un modèle de classification (risque de rupture OTP >15 min)
- évaluation / MCO (suivi de performance dans le temps, proxy de dérive)
- export des artefacts consommés par le dashboard de monitoring (JSON)

Usage:
    python train_model.py --data ../data/flights_synthetic.csv
"""

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    roc_auc_score, precision_score, recall_score, f1_score,
    confusion_matrix, brier_score_loss,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from model_utils import (
    FEATURE_COLUMNS, CATEGORICAL_COLUMNS, TARGET_COLUMN,
    load_dataset, build_features,
)


def build_pipeline() -> Pipeline:
    numeric_cols = [c for c in FEATURE_COLUMNS if c not in CATEGORICAL_COLUMNS]
    preproc = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
        ],
        remainder="passthrough",
    )
    model = GradientBoostingClassifier(
        n_estimators=200, max_depth=3, learning_rate=0.08, random_state=42,
    )
    return Pipeline([("preproc", preproc), ("model", model)]), numeric_cols


def weekly_monitoring(df: pd.DataFrame, y_true_col: str, y_pred_proba: np.ndarray) -> list:
    """Simule le suivi hebdomadaire de performance du modèle (proxy MCO)."""
    tmp = df[["scheduled_departure"]].copy()
    tmp["y_true"] = df[y_true_col].values
    tmp["y_proba"] = y_pred_proba
    tmp["week"] = tmp["scheduled_departure"].dt.to_period("W").apply(lambda p: p.start_time.date().isoformat())

    records = []
    for week, g in tmp.groupby("week"):
        if g["y_true"].nunique() < 2:
            auc = None
        else:
            auc = round(float(roc_auc_score(g["y_true"], g["y_proba"])), 3)
        records.append({
            "week": week,
            "n_flights": int(len(g)),
            "otp_breach_rate_actual": round(float(g["y_true"].mean()), 3),
            "otp_breach_rate_predicted": round(float((g["y_proba"] > 0.5).mean()), 3),
            "model_auc": auc,
        })
    return sorted(records, key=lambda r: r["week"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="../data/flights_synthetic.csv")
    parser.add_argument("--model-out", type=str, default="otp_model.joblib")
    parser.add_argument("--dashboard-out", type=str, default="../dashboard/otp_dashboard_data.json")
    args = parser.parse_args()

    df = load_dataset(args.data)
    df = build_features(df)
    df = df.sort_values("scheduled_departure").reset_index(drop=True)

    # Split temporel : les 6 dernières semaines simulent une fenêtre de
    # monitoring "en production" plutôt qu'un split aléatoire.
    cutoff = df["scheduled_departure"].max() - pd.Timedelta(weeks=6)
    train_df = df[df["scheduled_departure"] < cutoff]
    test_df = df[df["scheduled_departure"] >= cutoff]

    pipeline, _ = build_pipeline()
    pipeline.fit(train_df[FEATURE_COLUMNS], train_df[TARGET_COLUMN])

    proba_test = pipeline.predict_proba(test_df[FEATURE_COLUMNS])[:, 1]
    pred_test = (proba_test > 0.5).astype(int)
    y_test = test_df[TARGET_COLUMN].values

    metrics = {
        "auc": round(float(roc_auc_score(y_test, proba_test)), 3),
        "precision": round(float(precision_score(y_test, pred_test)), 3),
        "recall": round(float(recall_score(y_test, pred_test)), 3),
        "f1": round(float(f1_score(y_test, pred_test)), 3),
        "brier_score": round(float(brier_score_loss(y_test, proba_test)), 3),
        "n_train": int(len(train_df)),
        "n_test": int(len(test_df)),
        "test_period_start": test_df["scheduled_departure"].min().date().isoformat(),
        "test_period_end": test_df["scheduled_departure"].max().date().isoformat(),
    }

    cm = confusion_matrix(y_test, pred_test).tolist()

    # Feature importance (agrégée par variable d'origine, en repliant le one-hot)
    ohe_cols = pipeline.named_steps["preproc"].named_transformers_["cat"].get_feature_names_out(CATEGORICAL_COLUMNS)
    numeric_cols = [c for c in FEATURE_COLUMNS if c not in CATEGORICAL_COLUMNS]
    all_cols = list(ohe_cols) + numeric_cols
    importances = pipeline.named_steps["model"].feature_importances_
    imp_df = pd.DataFrame({"feature": all_cols, "importance": importances})

    def base_feature(f):
        for c in CATEGORICAL_COLUMNS:
            if f.startswith(c + "_"):
                return c
        return f

    imp_df["base_feature"] = imp_df["feature"].apply(base_feature)
    top_features = (
        imp_df.groupby("base_feature")["importance"].sum()
        .sort_values(ascending=False).head(10)
    )

    # Risque de retard par hub / haul type (sur l'ensemble du dataset test)
    test_df = test_df.copy()
    test_df["risk_score"] = proba_test
    risk_by_hub = (
        test_df.groupby("hub")["risk_score"].mean().round(3).to_dict()
    )
    risk_by_haul = (
        test_df.groupby("haul_type")["risk_score"].mean().round(3).to_dict()
    )
    risk_by_destination = (
        test_df.groupby("destination")["risk_score"].mean()
        .sort_values(ascending=False).head(10).round(3).to_dict()
    )

    weekly = weekly_monitoring(df.assign(**{TARGET_COLUMN: df[TARGET_COLUMN]}), TARGET_COLUMN,
                                pipeline.predict_proba(df[FEATURE_COLUMNS])[:, 1])

    dashboard_payload = {
        "generated_at": pd.Timestamp.now(tz="UTC").isoformat(),
        "metrics": metrics,
        "confusion_matrix": {
            "labels": ["OTP respecté (<=15min)", "Rupture OTP (>15min)"],
            "matrix": cm,
        },
        "top_features": [{"feature": k, "importance": round(float(v), 3)} for k, v in top_features.items()],
        "risk_by_hub": risk_by_hub,
        "risk_by_haul_type": risk_by_haul,
        "risk_by_destination_top10": risk_by_destination,
        "weekly_monitoring": weekly,
        "overall_otp_breach_rate": round(float(df[TARGET_COLUMN].mean()), 3),
        "n_flights_total": int(len(df)),
    }

    Path(args.dashboard_out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.dashboard_out, "w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, ensure_ascii=False, indent=2)

    joblib.dump(pipeline, args.model_out)

    print("Modèle entraîné.")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"Modèle sauvegardé -> {args.model_out}")
    print(f"Données dashboard exportées -> {args.dashboard_out}")


if __name__ == "__main__":
    main()
