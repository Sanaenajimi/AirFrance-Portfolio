"""
Génération d'un jeu de données synthétique de vols Ground Ops
================================================================
Simule des vols court/moyen/long-courrier au départ des hubs Air France
(CDG, ORY) avec des variables explicatives du risque de retard (OTP).

Ce jeu de données est 100% simulé (aucune donnée réelle Air France) :
il sert uniquement de support pédagogique / portfolio pour illustrer
le rôle de Business Analyst du modèle de prédiction du risque OTP.

Usage:
    python generate_synthetic_data.py [--n-flights 20000] [--seed 42]
"""

import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

HUBS = ["CDG", "ORY"]

# (destination, type de courrier, durée de vol moyenne en minutes, poids d'occurrence)
ROUTES = [
    ("JFK", "long-courrier", 480, 3), ("ATL", "long-courrier", 540, 1),
    ("YUL", "long-courrier", 420, 2), ("NRT", "long-courrier", 720, 1),
    ("PVG", "long-courrier", 690, 1), ("DXB", "long-courrier", 420, 2),
    ("FDF", "long-courrier", 500, 2), ("RUN", "long-courrier", 660, 1),
    ("MAD", "moyen-courrier", 120, 4), ("BCN", "moyen-courrier", 105, 4),
    ("FCO", "moyen-courrier", 130, 3), ("LIS", "moyen-courrier", 150, 3),
    ("AMS", "moyen-courrier", 75, 4), ("LHR", "moyen-courrier", 80, 5),
    ("FRA", "moyen-courrier", 85, 4), ("MXP", "moyen-courrier", 95, 3),
    ("NCE", "court-courrier", 75, 6), ("MRS", "court-courrier", 70, 6),
    ("TLS", "court-courrier", 65, 6), ("BOD", "court-courrier", 70, 5),
    ("LYS", "court-courrier", 55, 5), ("NTE", "court-courrier", 65, 5),
]

AIRCRAFT_BY_HAUL = {
    "court-courrier": ["A220", "A319", "A320"],
    "moyen-courrier": ["A320", "A321", "A319"],
    "long-courrier": ["A350", "B777", "B787"],
}

WEATHER_STATES = ["nominal", "vent_fort", "orage", "brouillard", "neige"]
WEATHER_WEIGHTS = [0.72, 0.12, 0.08, 0.05, 0.03]


def generate(n_flights: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    routes = [r for r in ROUTES for _ in range(r[3])]
    start_date = datetime(2025, 1, 1)

    rows = []
    for i in range(n_flights):
        hub = rng.choice(HUBS, p=[0.75, 0.25])
        dest, haul, base_duration, _ = routes[rng.integers(0, len(routes))]
        aircraft = rng.choice(AIRCRAFT_BY_HAUL[haul])

        day_offset = rng.integers(0, 210)
        sched_dep = start_date + timedelta(days=int(day_offset),
                                            hours=int(rng.integers(5, 23)),
                                            minutes=int(rng.integers(0, 60) // 5 * 5))
        dow = sched_dep.weekday()  # 0=lundi
        month = sched_dep.month
        is_holiday_period = month in (7, 8, 12) or (month == 4 and sched_dep.day < 15)

        weather = rng.choice(WEATHER_STATES, p=WEATHER_WEIGHTS)
        weather_severity = {"nominal": 0, "vent_fort": 1, "orage": 3, "brouillard": 2, "neige": 4}[weather]

        connections = rng.poisson(6 if haul != "court-courrier" else 2)
        turnaround_min = max(25, int(rng.normal(45 if haul == "court-courrier" else 75, 12)))
        min_turnaround = {"court-courrier": 30, "moyen-courrier": 40, "long-courrier": 65}[haul]

        crew_ready = rng.random() > 0.04
        ground_handling_delay = max(0, rng.normal(3, 6))
        atc_restriction = rng.random() < (0.10 if hub == "CDG" else 0.06)
        rotation_inherited_delay = max(0, rng.normal(4, 10)) if rng.random() < 0.35 else 0
        strike_day = rng.random() < 0.015
        pax_load_factor = float(np.clip(rng.normal(0.84, 0.09), 0.4, 1.0))

        # --- Modèle génératif du retard (vérité terrain simulée) ---
        # Calibré pour un taux de rupture OTP (>15 min) proche des standards
        # du secteur (~18-22%), à titre illustratif.
        delay = 0.0
        delay += weather_severity * rng.normal(3, 1.5)
        delay += max(0, min_turnaround - turnaround_min) * 0.9
        delay += (0 if crew_ready else rng.normal(20, 7))
        delay += ground_handling_delay * 0.6
        delay += (rng.normal(12, 5) if atc_restriction else 0)
        delay += rotation_inherited_delay * 0.5
        delay += (rng.normal(35, 12) if strike_day else 0)
        delay += max(0, connections - 8) * rng.normal(1.0, 0.4)
        delay += (2 if dow in (4, 6) else 0)  # vendredi / dimanche plus chargés
        delay += (3 if is_holiday_period else 0)
        delay += rng.normal(-4, 4)  # bruit résiduel (centré négatif : la majorité des vols sont à l'heure)
        delay = max(0, delay)

        rows.append({
            "flight_id": f"AF{rng.integers(1000, 9999)}-{i}",
            "scheduled_departure": sched_dep.isoformat(timespec="minutes"),
            "hub": hub,
            "destination": dest,
            "haul_type": haul,
            "aircraft_type": aircraft,
            "day_of_week": dow,
            "month": month,
            "is_holiday_period": is_holiday_period,
            "weather_state": weather,
            "weather_severity": weather_severity,
            "connections_count": int(connections),
            "turnaround_minutes": int(turnaround_min),
            "min_turnaround_required": min_turnaround,
            "crew_ready_on_time": bool(crew_ready),
            "ground_handling_delay_min": round(ground_handling_delay, 1),
            "atc_restriction": bool(atc_restriction),
            "rotation_inherited_delay_min": round(rotation_inherited_delay, 1),
            "strike_day": bool(strike_day),
            "pax_load_factor": round(pax_load_factor, 2),
            "delay_minutes": round(delay, 1),
            "otp_breach_15min": delay > 15,  # définition OTP standard (>15 min)
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Génère un dataset synthétique de vols Ground Ops")
    parser.add_argument("--n-flights", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="flights_synthetic.csv")
    args = parser.parse_args()

    df = generate(args.n_flights, args.seed)
    out_path = args.out
    df.to_csv(out_path, index=False)
    print(f"{len(df)} vols générés -> {out_path}")
    print(f"Taux de rupture OTP (>15 min): {df['otp_breach_15min'].mean():.1%}")
