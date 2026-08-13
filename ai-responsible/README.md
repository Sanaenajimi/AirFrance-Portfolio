# AI Responsible — Ground Ops (Customer, Opérations, Ressources)

Ce module illustre le rôle transverse **AI Responsible** du poste : garantir
la bonne application du règlement européen sur l'IA (AI Act), conseiller les
décideurs sur leurs déclarations obligatoires, et tracer l'ensemble des usages
IA du domaine Ground Ops.

## Contenu

| Fichier | Rôle |
|---|---|
| `templates/registre_usages_ia.csv` | Registre des usages IA du domaine, avec classification de risque (AI Act) |
| `templates/template_declaration_ai_act.md` | Trame de déclaration à faire remplir par tout décideur portant un système d'IA |
| `validate_registre_ia.py` | Script de contrôle de conformité (déclaration, documentation, supervision humaine, fraîcheur des audits) |

## Ce que couvre le rôle

1. **Classification du risque** — accompagner chaque décideur métier dans la
   qualification de son usage IA selon les quatre niveaux du règlement
   européen : inacceptable, élevé, limité, minimal.
2. **Conseil sur les obligations** — pour les usages à risque élevé
   (ex. outils influençant l'affectation ou l'évaluation du personnel, cf.
   Annexe III "gestion des travailleurs") : gestion des risques, gouvernance
   des données, documentation technique, supervision humaine effective.
3. **Traçabilité** — maintenir le registre des usages IA à jour et le faire
   auditer périodiquement (`validate_registre_ia.py`).
4. **Point d'alerte** — identifier tout usage relevant d'une pratique
   interdite (risque inacceptable) et le faire remonter immédiatement.

## Utilisation

```bash
python validate_registre_ia.py --registre templates/registre_usages_ia.csv
```

Le script signale : les usages classés risque inacceptable, les usages non
encore classifiés, et — pour les usages à risque élevé — l'absence de
déclaration, de documentation technique, de mesures de supervision humaine, ou
un audit trop ancien (> 12 mois).

## Exemple illustratif

Le registre inclut un cas volontairement classé **risque élevé** (`IA-002` —
outil d'affectation des équipes au sol), représentatif d'un usage IA en
gestion des ressources humaines au sens de l'Annexe III du règlement, et un
cas **non classifié** (`IA-004`) pour illustrer le fonctionnement du contrôle
de conformité.
