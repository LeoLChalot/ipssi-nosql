# Partie 3 — CRUD Python

Ce document explique comment utiliser le CRUD du projet : ce qu'il faut avoir en place, comment le lancer, et à quoi doit ressembler un résultat normal.

## Prérequis

- Python 3.12+ et [`uv`](https://astral.sh/uv) installés
- Un fichier `.env` à la racine du projet contenant la chaîne de connexion Atlas :
  ```
  ATLAS_URI="mongodb+srv://<utilisateur>:<mot_de_passe>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
  ```
- L'adresse IP de la machine autorisée dans Atlas (**Network Access** → `0.0.0.0/0` en mode formation)

## Installation

Depuis la racine du projet :

```bash
uv sync
```

Cette commande installe automatiquement les dépendances nécessaires (`pymongo`, `python-dotenv`, `ipykernel`).

## Utilisation

1. Ouvrir `notebookCrud_BackUp.ipynb` (Jupyter, VS Code, ou tout éditeur compatible notebook)
2. Exécuter les cellules **dans l'ordre**, de haut en bas
3. La section **"CRUD Python (livrable 3)"** contient, dans l'ordre :

| Étape | Ce qui se passe | Ce que vous devez voir |
|---|---|---|
| Connexion | Établit `atlas_client` à partir de `.env` | `Connexion cloud établie avec succès` |
| `create_accident(...)` | Insère un accident de test dans `securite_routiere.accidents` | `Inséré avec _id=...` |
| `read_accidents(...)` | Recherche les accidents du département 75 | Une liste de 5 lignes avec numéro d'accident, département, voie |
| `update_accident(...)` | Corrige l'adresse d'un accident existant | `1 document(s) modifié(s)` (ou `0` si déjà modifié lors d'un run précédent) |
| `delete_accident(...)` | Supprime le document de test créé plus haut | `1 document(s) supprimé(s)` |
| Démonstration d'erreurs | Déclenche volontairement 4 erreurs pymongo (une par opération) | 4 messages `Échec de ...` — le notebook ne plante à aucun moment |

## Relancer proprement

Le notebook est conçu pour être **rejouable sans effet de bord** : les documents de test utilisent des numéros d'accident hors plage réelle (`999999999999`, `888888888888`) et sont supprimés dans la foulée de leur création. Vous pouvez faire *Restart Kernel* puis *Run All* autant de fois que nécessaire sans corrompre les vraies données du dataset.

## En cas de problème

| Message | Cause probable | Solution |
|---|---|---|
| `URI manquante dans .env / .env.local` | `.env` absent ou vide | Vérifier que `.env` existe à la racine et contient `ATLAS_URI` |
| `ServerSelectionTimeoutError` | IP non autorisée sur Atlas, ou pas de réseau | Network Access → ajouter `0.0.0.0/0` sur Atlas |
| `Authentication failed` | Mauvais utilisateur/mot de passe dans l'URI | Vérifier l'utilisateur créé dans **Database Access** sur Atlas |
| `ModuleNotFoundError: pymongo` | Dépendances non installées | Relancer `uv sync` |
