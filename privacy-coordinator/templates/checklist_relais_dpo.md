# Checklist — Relais Privacy Coordinator auprès de la communauté data

À utiliser lors du conseil à une équipe métier (Customer, Opérations, Ressources)
qui initie ou fait évoluer un traitement de données, en amont de la validation
par le DPO.

## 1. Qualification du traitement

- [ ] Le traitement implique-t-il des données à caractère personnel (directes ou
      indirectement identifiantes) ?
- [ ] La finalité est-elle clairement formulée et limitée (pas de finalité floue
      ou "au cas où") ?
- [ ] Une base légale est-elle identifiée (contrat, obligation légale, intérêt
      légitime, consentement) et documentée ?
- [ ] Le traitement porte-t-il sur des catégories particulières de données
      (santé, biométrie, origine, etc.) ou des données de mineurs ?

## 2. Minimisation et proportionnalité

- [ ] Les données collectées sont-elles strictement nécessaires à la finalité ?
- [ ] Existe-t-il une alternative anonymisée ou agrégée suffisante ?
- [ ] La durée de conservation est-elle définie et alignée sur un cas d'usage
      métier documenté ?

## 3. Analyse d'impact (DPIA)

- [ ] Le traitement figure-t-il sur la liste des traitements nécessitant une
      DPIA (surveillance systématique, décision automatisée à effet
      significatif, données sensibles à grande échelle) ?
- [ ] Si oui, la DPIA est-elle planifiée avec le DPO avant mise en production ?

## 4. Droits des personnes et transparence

- [ ] Les personnes concernées sont-elles informées (mention d'information,
      politique de confidentialité à jour) ?
- [ ] Les modalités d'exercice des droits (accès, rectification, opposition)
      sont-elles opérationnelles pour ce traitement ?

## 5. Sous-traitance et transferts

- [ ] Un sous-traitant est-il impliqué ? Un contrat de sous-traitance conforme
      est-il en place ?
- [ ] Un transfert hors UE est-il prévu ? Un mécanisme de transfert valide
      (clauses contractuelles types, décision d'adéquation) est-il documenté ?

## 6. Sécurité

- [ ] Les mesures de sécurité (chiffrement, contrôle d'accès, journalisation)
      sont-elles proportionnées au risque ?
- [ ] Un plan de réponse en cas de violation de données est-il identifié ?

## 7. Traçabilité

- [ ] Le traitement est-il consigné dans le registre des traitements
      (`registre_traitements.csv`) ?
- [ ] Une date de réexamen est-elle planifiée ?

---
**Escalade au DPO requise si** : DPIA nécessaire, transfert hors UE sans
mécanisme validé, données sensibles à grande échelle, ou désaccord persistant
avec l'équipe métier sur le niveau de risque.
