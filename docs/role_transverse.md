# Note de cadrage — Data Officer Operations, domaine Ground Ops

## Rattachement et périmètre

Le poste est rattaché au **Data Officer des Opérations** et couvre l'ensemble
du domaine de données **Ground Ops**, structuré en trois sous-domaines
métier :

- **Customer** — relation client, réclamations, correspondances bagages,
  programmes de fidélité liés à l'expérience passager en escale.
- **Opérations** — ponctualité (OTP), rotations, ressources aéroportuaires,
  surveillance opérationnelle.
- **Ressources** — planification des effectifs au sol, qualifications,
  affectations.

Le poste combine **trois rôles complémentaires** sur ce périmètre, ainsi
qu'un **rôle transverse de gouvernance** :

| Rôle | Nature | Dossier du projet |
|---|---|---|
| Business Analyst — modèle OTP | Opérationnel / produit data | [`otp-delay-risk/`](../otp-delay-risk/) |
| Privacy Coordinator | Conformité RGPD | [`privacy-coordinator/`](../privacy-coordinator/) |
| AI Responsible | Conformité règlement IA | [`ai-responsible/`](../ai-responsible/) |

## Pourquoi ces trois rôles sont complémentaires

Le point commun des trois rôles est la **gouvernance de la donnée et des
modèles au service des opérations aéroportuaires** :

- Le Business Analyst OTP porte un cas d'usage IA concret (prédiction du
  risque de retard) et en assure la valeur métier.
- Le Privacy Coordinator s'assure que la donnée utilisée par ce type de
  modèle — et par tous les traitements du domaine — respecte les principes de
  protection des données personnelles.
- L'AI Responsible s'assure que les systèmes d'IA du domaine (dont le modèle
  OTP lui-même, mais aussi d'autres usages comme l'affectation des équipes ou
  l'assistance client) respectent le règlement européen sur l'IA.

Ce triptyque permet à un seul poste de couvrir à la fois **la production de
valeur data** (BA OTP) et **la maîtrise des risques réglementaires** associés
(Privacy + AI Act), sur un périmètre opérationnel cohérent (Ground Ops).

## Indicateurs de succès transverses (illustratifs)

- Couverture du registre des traitements et du registre des usages IA :
  100 % des traitements/usages actifs du domaine recensés.
- Délai de traitement des demandes de conseil privacy/IA par les équipes
  métier.
- Taux de disponibilité et de performance du modèle OTP (cf. dashboard de
  monitoring).
- Nombre d'anomalies de conformité détectées et corrigées (scripts de
  validation des registres).

## Cadence de gouvernance proposée

- **Hebdomadaire** — suivi de la performance du modèle OTP et des incidents
  opérationnels associés.
- **Mensuelle** — revue de la backlog du modèle OTP avec les business owners ;
  point de conseil privacy/IA avec les équipes en cours d'instruction.
- **Trimestrielle** — revue des registres (traitements, usages IA) avec le
  DPO et le comité de gouvernance data.
- **Annuelle** — audit complet des usages à risque élevé (AI Act) et des
  traitements nécessitant une DPIA.
