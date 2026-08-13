# Privacy Coordinator — Ground Ops (Customer, Opérations, Ressources)

Ce module illustre le rôle de **Privacy Coordinator** du poste : s'assurer de
la bonne application des règlements relatifs aux données personnelles au sein
du domaine Ground Ops, en lien avec le DPO (Data Protection Officer), et servir
de relais auprès de la communauté data (conseil, application des principes).

## Contenu

| Fichier | Rôle |
|---|---|
| `templates/registre_traitements.csv` | Registre des traitements du domaine Ground Ops (Customer, Opérations, Ressources) — trame type article 30 RGPD |
| `templates/checklist_relais_dpo.md` | Checklist de conseil utilisée lors de l'accompagnement d'une équipe métier sur un nouveau traitement |
| `validate_registre.py` | Script de contrôle de cohérence du registre (champs obligatoires, suivi DPIA, fraîcheur du réexamen) |

## Positionnement du rôle

Le Privacy Coordinator n'est **pas** le DPO : il agit comme **relais
opérationnel** entre le DPO et les équipes métier / data du domaine Ground
Ops. Concrètement :

1. **Conseil de premier niveau** — accompagne les équipes métier via la
   checklist avant remontée au DPO.
2. **Tenue du registre** — maintient à jour le registre des traitements
   spécifique au domaine, contrôlé régulièrement via `validate_registre.py`.
3. **Escalade** — identifie les traitements nécessitant une DPIA ou une
   validation formelle du DPO, et prépare les éléments de dossier.
4. **Diffusion des principes** — relaie les règles et évolutions
   réglementaires auprès de la communauté data (Business Analysts, Data
   Scientists, Data Engineers du domaine).

## Utilisation

```bash
python validate_registre.py --registre templates/registre_traitements.csv
```

Le script signale les traitements avec des champs manquants, une DPIA requise
mais non suivie, un transfert hors UE non sécurisé, ou une date de réexamen
trop ancienne (> 18 mois).
