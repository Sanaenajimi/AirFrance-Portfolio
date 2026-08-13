"""Fonctions partagées de feature engineering pour le modèle de risque OTP."""

import pandas as pd

FEATURE_COLUMNS = [
    "hub", "destination", "haul_type", "aircraft_type",
    "day_of_week", "month", "is_holiday_period",
    "weather_severity", "connections_count",
    "turnaround_minutes", "min_turnaround_required",
    "crew_ready_on_time", "ground_handling_delay_min",
    "atc_restriction", "rotation_inherited_delay_min",
    "strike_day", "pax_load_factor",
]

CATEGORICAL_COLUMNS = ["hub", "destination", "haul_type", "aircraft_type"]
TARGET_COLUMN = "otp_breach_15min"


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["scheduled_departure"])
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute des features dérivées utiles au modèle."""
    out = df.copy()
    out["turnaround_slack_min"] = out["turnaround_minutes"] - out["min_turnaround_required"]
    out["is_weekend"] = out["day_of_week"].isin([5, 6])
    return out
