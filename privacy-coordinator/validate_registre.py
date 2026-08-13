"""
Contrôle de cohérence du registre des traitements (rôle Privacy Coordinator).

Vérifie, pour chaque traitement du registre :
- que les champs obligatoires sont renseignés,
- que les traitements marqués DPIA requise ont un statut de DPIA suivi,
- que les traitements avec transfert hors UE documentent une mesure de sécurité,
- que la date de dernier réexamen n'est pas trop ancienne (> 18 mois).

Usage:
    python validate_registre.py [--registre templates/registre_traitements.csv]
"""

import argparse
import csv
from datetime import date, datetime

REQUIRED_FIELDS = [
    "nom_traitement", "finalite", "base_legale", "categories_donnees",
    "duree_conservation", "proprietaire_metier",
]
REEXAMEN_MAX_MOIS = 18


def months_since(d: date) -> float:
    today = date.today()
    return (today.year - d.year) * 12 + (today.month - d.month)


def validate(rows):
    issues = []
    for row in rows:
        rid = row.get("id", "?")

        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                issues.append(f"[{rid}] champ obligatoire manquant : {field}")

        if row.get("dpia_requise", "").strip().lower() == "oui":
            statut = row.get("dpia_statut", "").strip().lower()
            if statut in ("", "non applicable"):
                issues.append(f"[{rid}] DPIA requise mais statut de DPIA non renseigné")
            elif statut not in ("realisee", "en cours", "a confirmer"):
                issues.append(f"[{rid}] statut DPIA inattendu : '{row.get('dpia_statut')}'")

        if row.get("transfert_hors_ue", "").strip().lower().startswith("oui"):
            if not row.get("mesures_securite", "").strip():
                issues.append(f"[{rid}] transfert hors UE sans mesure de sécurité documentée")

        reexamen_raw = row.get("dernier_reexamen", "").strip()
        if reexamen_raw:
            try:
                d = datetime.strptime(reexamen_raw, "%Y-%m-%d").date()
                if months_since(d) > REEXAMEN_MAX_MOIS:
                    issues.append(f"[{rid}] dernier réexamen daté du {reexamen_raw} (> {REEXAMEN_MAX_MOIS} mois)")
            except ValueError:
                issues.append(f"[{rid}] date de réexamen invalide : '{reexamen_raw}'")
        else:
            issues.append(f"[{rid}] date de dernier réexamen manquante")

    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registre", default="templates/registre_traitements.csv")
    args = parser.parse_args()

    with open(args.registre, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    issues = validate(rows)

    print(f"{len(rows)} traitements contrôlés dans {args.registre}")
    if not issues:
        print("Aucune anomalie détectée.")
    else:
        print(f"{len(issues)} anomalie(s) détectée(s) :")
        for issue in issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
