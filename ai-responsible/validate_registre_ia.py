"""
Contrôle de conformité du registre des usages IA (rôle AI Responsible).

Vérifie notamment que :
- tout usage classé "Risque élevé" a une déclaration effectuée, une
  documentation technique disponible et des mesures de supervision humaine
  documentées,
- tout usage "Risque élevé" a été audité au cours des 12 derniers mois,
- aucun usage n'est classé "Risque inacceptable" (pratique interdite),
- aucun usage n'est laissé sans classification ("A évaluer") au-delà d'un
  délai raisonnable n'est pas calculable ici sans date de création, donc
  simplement signalé.

Usage:
    python validate_registre_ia.py [--registre templates/registre_usages_ia.csv]
"""

import argparse
import csv
from datetime import date, datetime

AUDIT_MAX_MOIS_RISQUE_ELEVE = 12


def months_since(d: date) -> float:
    today = date.today()
    return (today.year - d.year) * 12 + (today.month - d.month)


def validate(rows):
    issues = []
    for row in rows:
        rid = row.get("id", "?")
        risque = row.get("classification_risque_ai_act", "").strip()

        if risque.lower() == "risque inacceptable":
            issues.append(f"[{rid}] CRITIQUE : classé risque inacceptable — usage à interrompre immédiatement")

        if risque.lower() == "a evaluer" or risque == "":
            issues.append(f"[{rid}] classification de risque non finalisée — à traiter en priorité")
            continue

        if risque.lower() == "risque eleve":
            if row.get("declaration_effectuee", "").strip().lower() != "oui":
                issues.append(f"[{rid}] risque élevé sans déclaration effectuée")
            if row.get("documentation_technique_dispo", "").strip().lower() != "oui":
                issues.append(f"[{rid}] risque élevé sans documentation technique disponible")
            if not row.get("mesures_surveillance_humaine", "").strip():
                issues.append(f"[{rid}] risque élevé sans mesure de supervision humaine documentée")

            audit_raw = row.get("dernier_audit", "").strip()
            if not audit_raw:
                issues.append(f"[{rid}] risque élevé sans date d'audit renseignée")
            else:
                try:
                    d = datetime.strptime(audit_raw, "%Y-%m-%d").date()
                    if months_since(d) > AUDIT_MAX_MOIS_RISQUE_ELEVE:
                        issues.append(f"[{rid}] dernier audit du {audit_raw} (> {AUDIT_MAX_MOIS_RISQUE_ELEVE} mois pour un risque élevé)")
                except ValueError:
                    issues.append(f"[{rid}] date d'audit invalide : '{audit_raw}'")

    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registre", default="templates/registre_usages_ia.csv")
    args = parser.parse_args()

    with open(args.registre, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    issues = validate(rows)

    print(f"{len(rows)} usages IA contrôlés dans {args.registre}")
    if not issues:
        print("Aucune anomalie détectée.")
    else:
        print(f"{len(issues)} anomalie(s) détectée(s) :")
        for issue in issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
