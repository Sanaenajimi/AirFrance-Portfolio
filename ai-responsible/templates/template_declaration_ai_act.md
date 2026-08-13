# Template — Déclaration d'usage IA (AI Responsible)

À compléter par le décideur métier porteur d'un système d'IA, avec l'appui de
l'AI Responsible, avant mise en production ou évolution significative.

## 1. Identification

- **Nom de l'usage / système** :
- **Domaine** (Customer / Opérations / Ressources / Transverse) :
- **Décideur métier responsable** :
- **Fournisseur** (interne / éditeur tiers, préciser) :

## 2. Description fonctionnelle

- **Objectif du système** :
- **Utilisateurs finaux** (rôles impactés) :
- **Personnes potentiellement affectées par une décision ou une
  recommandation du système** :
- **Le système prend-il une décision automatisée sans intervention humaine
  significative ?** (Oui / Non — si oui, détailler le mécanisme de recours)

## 3. Classification du risque (Règlement européen sur l'IA)

- [ ] **Risque inacceptable** — pratique interdite (notation sociale,
      manipulation subliminale, etc.) → **le système ne doit pas être déployé**
- [ ] **Risque élevé** — cf. Annexe III (ex. gestion des travailleurs :
      recrutement, affectation de tâches, évaluation, licenciement ;
      infrastructures critiques ; biométrie)
- [ ] **Risque limité** — obligation de transparence (informer l'utilisateur
      qu'il interagit avec une IA ou un contenu généré par IA)
- [ ] **Risque minimal** — aide à la décision sans impact direct sur des
      personnes

**Justification de la classification retenue :**

## 4. Obligations associées (si risque élevé)

- [ ] Système de gestion des risques documenté
- [ ] Gouvernance des données (qualité, biais, représentativité)
- [ ] Documentation technique à jour
- [ ] Journalisation (logs) permettant la traçabilité
- [ ] Information des utilisateurs et transparence
- [ ] Supervision humaine effective et significative
- [ ] Niveau de robustesse, exactitude et cybersécurité approprié
- [ ] Évaluation de conformité réalisée avant mise sur le marché / en service

## 5. Supervision humaine

- **Point(s) de contrôle humain dans le processus** :
- **Mécanisme de contestation / recours pour la personne affectée** :

## 6. Décision et suivi

- **Date de la déclaration** :
- **Statut** : ☐ Approuvé ☐ Approuvé sous conditions ☐ Refusé ☐ En évaluation
- **Date du prochain audit** :
- **Signataire (AI Responsible)** :

---
*Ce document doit être versé au `registre_usages_ia.csv` et réexaminé à
chaque évolution significative du système ou au minimum annuellement pour les
usages à risque élevé.*
