# Domain

## 1. Compréhension du domaine

- Qu'est-ce qu'un **ticket** dans un système de support ?
Un ticket est une manière pour un utilisateur d'obtenir de l'aide dans l'utilisation d'un logiciel.

- Quelles informations minimales doit-il contenir ?
Des informations détaillées sur le problème, la date et l'heure ou il s'est produit, la version du logiciel utilisée, les étapes de reproduction du problème éventuelles

- Quels **statuts** peut-il prendre au cours de sa vie ?
    - OPEN → ouvert, en attente de traitement
    - IN_PROGRESS → en cours de résolution
    - RESOLVED → résolu, en attente de validation
    - CLOSED → fermé définitivement

- Quels rôles un utilisateur peut-il prendre ?

Demandeur, Gestionnaire et Administrateur

- Quelles règles métier sont présentes ?

    - Un ticket doit avoir un titre non vide
    - Un utilisateur doit avoir un username non vide
    - Un ticket fermé ne peut plus être assigné
    - Un ticket déjà fermé ne peut pas être re-fermé
    - Un ticket ouvert ne peut que passer en status "en cours"
    - Un ticket en cours ne peut pas repasser en mode "ouvert"
    - Un ticket 

