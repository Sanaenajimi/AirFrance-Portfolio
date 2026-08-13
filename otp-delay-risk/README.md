# Modèle de prédiction du risque de retard OTP — rôle Business Analyst

Ce module illustre le rôle de **Business Analyst du modèle de prédiction du
risque de retard ('OTP')** décrit dans le poste : gestion de la backlog du
modèle avec les business owners et la Data Science, maintien en conditions
opérationnelles, support aux services utilisateurs via un dashboard de
monitoring, et référent du risque retard au sein de la compagnie.

> ⚠️ **Données 100 % synthétiques.** Aucune donnée réelle Air France n'est
> utilisée. Ce module a une vocation de démonstration (portfolio).

## Structure

```
otp-delay-risk/
├── data/
│   └── generate_synthetic_data.py   # génère un dataset de vols simulé
├── model/
│   ├── model_utils.py               # feature engineering partagé
│   └── train_model.py               # entraînement + export des métriques de monitoring
├── backlog/
│   ├── backlog_modele_otp.csv       # backlog produit du modèle
│   └── README.md                    # process de gestion de la backlog
└── dashboard/
    ├── dashboard_template.html      # template du dashboard (charts en SVG/JS natif)
    ├── build_dashboard.py           # assemble le dashboard final à partir des données
    └── otp_monitoring_dashboard.html  # dashboard généré, ouvrable directement dans un navigateur
```

## Pipeline de bout en bout

```bash
cd otp-delay-risk

# 1. Génère le dataset synthétique de vols
python data/generate_synthetic_data.py --n-flights 20000 --seed 42 \
    --out data/flights_synthetic.csv

# 2. Entraîne le modèle et exporte les données de monitoring
cd model
python train_model.py --data ../data/flights_synthetic.csv
cd ..

# 3. Génère le dashboard de monitoring (HTML autonome)
cd dashboard
python build_dashboard.py
# -> ouvrir otp_monitoring_dashboard.html dans un navigateur
```

## Choix de modélisation

- **Cible** : `otp_breach_15min` — le vol dépasse-t-il 15 minutes de retard au
  départ (définition standard de l'indicateur OTP15) ?
- **Split temporel** (et non aléatoire) : le modèle est entraîné sur les
  premiers mois et évalué sur les 6 dernières semaines, pour simuler une
  fenêtre de monitoring en production plutôt qu'une validation croisée
  classique — cohérent avec le rôle de suivi en conditions opérationnelles.
- **Modèle** : Gradient Boosting Classifier (scikit-learn), avec encodage
  one-hot des variables catégorielles (hub, destination, type de courrier,
  type d'appareil).
- **Suivi hebdomadaire** : le script recalcule les métriques par semaine sur
  l'ensemble du dataset pour donner une vue de dérive potentielle dans le
  temps, restituée dans le dashboard.

## Dashboard de monitoring

Le dashboard (`dashboard/otp_monitoring_dashboard.html`) est un fichier HTML
autonome (pas de serveur ni de dépendance externe) qui présente :

- les indicateurs clés du modèle sur la dernière fenêtre de test (AUC,
  précision, rappel, F1),
- le suivi hebdomadaire du taux de rupture OTP réel vs prédit,
- le suivi hebdomadaire de l'AUC (proxy de dérive du modèle),
- la matrice de confusion,
- le risque moyen par hub et par type de courrier, et le top 10 des
  destinations à risque,
- les facteurs contributeurs au risque (importance des variables),
- un aperçu de la backlog du modèle.

Il peut être ouvert directement dans n'importe quel navigateur, y compris sans
connexion réseau.
