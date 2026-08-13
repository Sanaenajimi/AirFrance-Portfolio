# Gestion de la backlog — Modèle de risque OTP

Ce dossier illustre le rôle de **Business Analyst du modèle de prédiction du
risque de retard OTP** : la gestion de la backlog en collaboration avec les
business owners du modèle (Direction Ops des hubs, Direction Bagages, Data
Officer Operations) et l'équipe Data Science.

## Contenu

- `backlog_modele_otp.csv` — backlog produit du modèle : évolutions
  fonctionnelles, dette technique, monitoring / MCO, documentation et process.

## Colonnes

| Colonne | Description |
|---|---|
| `type` | Évolution modèle, nouvelle fonctionnalité, dette technique, monitoring/MCO, documentation, process |
| `priorite_moscow` | Priorisation MoSCoW (Must / Should / Could / Won't) |
| `business_owner` | Porteur métier de l'item (Ops, Bagages, Data Officer...) |
| `data_science_owner` | Porteur Data Science / IT |
| `statut` | À faire, En cours, En revue, Fait |
| `release_cible` | Fenêtre de livraison visée |
| `effort_pts` | Estimation d'effort (points, type planning poker) |
| `impact_attendu` | Impact business ou technique attendu, chiffré quand possible |

## Rituel de gestion de backlog

1. **Recueil des besoins** — remontées des services utilisateurs (dispatch,
   hubs, bagages), des incidents de production, et des opportunités
   identifiées par la Data Science.
2. **Priorisation mensuelle** — revue avec les business owners (item
   `OTP-008`) : arbitrage MoSCoW en fonction de l'impact OTP et de la
   capacité de l'équipe Data Science.
3. **Suivi hebdomadaire** — statut des items en cours, blocages IT
   (alimentation, infrastructure), remontés au Data Officer Operations.
4. **Clôture et mesure d'impact** — chaque item livré est confronté à
   l'impact attendu (ex. gain d'AUC, réduction de latence) via le
   [dashboard de monitoring](../dashboard/).
