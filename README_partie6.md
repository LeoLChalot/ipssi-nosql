# Partie 6 — Sauvegarde et restauration

Ce document explique comment sauvegarder et restaurer la base `securite_routiere` : à la main pour une démonstration, ou automatiquement chaque vendredi.

## Prérequis

- MongoDB Database Tools installés (`mongodump`, `mongorestore`) :
  ```bash
  mongodump --version
  mongorestore --version
  ```
  Si ces commandes échouent, installer le paquet (`brew install mongodb-database-tools` sous macOS)
- Un fichier `.env` à la racine avec `ATLAS_URI` (source des sauvegardes)
- Un fichier `.env.local` avec `LOCAL_URI` (cible de la démonstration de restauration), et un serveur MongoDB qui tourne en local (Docker ou installation native) — voir `setup/README.md` pour l'installer

## Sauvegarder manuellement

1. Ouvrir `notebookCrud_BackUp.ipynb`
2. Aller à la section **"Administration — sauvegarde et restauration (livrable 6)"**
3. Exécuter la cellule de démonstration **sauvegarde**

Résultat attendu :
```
Sauvegarde créée : backups/securite_routiere_2026-08-28_11h06
```

Un nouveau dossier apparaît dans `backups/`, contenant un fichier `.bson` + `.metadata.json` par collection. Chaque sauvegarde a un nom unique (horodaté) : rien n'est jamais écrasé.

## Restaurer manuellement

1. Juste après la sauvegarde, exécuter la cellule de démonstration **restauration**

Résultat attendu :
```
Restauration terminée depuis : backups/securite_routiere_2026-08-28_11h06
```

La restauration cible volontairement la base **locale** (`LOCAL_URI`), jamais Atlas — ça vérifie que le dump est valide sans jamais risquer d'altérer les vraies données de production. Pour vérifier que les documents sont bien revenus :

```bash
mongosh --quiet --eval "db.getSiblingDB('securite_routiere').accidents.countDocuments()" mongodb://localhost:27017
```

## Automatiser la sauvegarde chaque vendredi

Le script `scripts/weekly_backup.py` existe déjà dans le dépôt (il a été généré depuis le notebook). Il ne dépend d'aucun notebook ouvert : il se lance seul, en ligne de commande.

### 1. Tester le script manuellement une fois

```bash
uv run python scripts/weekly_backup.py
```

Doit afficher `Sauvegarde créée : backups/...` et créer le dossier correspondant, exactement comme la démonstration dans le notebook.

### 2. Programmer la tâche cron (une seule fois)

```bash
crontab -e
```

Ajouter la ligne (en adaptant le chemin du projet et de `uv` à votre machine — trouvable avec `which uv`) :

```cron
0 20 * * 5 cd /chemin/vers/ipssi-nosql && /opt/homebrew/bin/uv run python scripts/weekly_backup.py >> backups/backup.log 2>&1
```

Cette ligne signifie : *tous les vendredis à 20h00*, lancer le script de sauvegarde et enregistrer sa sortie dans `backups/backup.log`.

### 3. Vérifier que la tâche est bien enregistrée

```bash
crontab -l
```

### 4. Vérifier qu'une sauvegarde automatique a bien tourné

```bash
cat backups/backup.log
ls backups/
```

Si le vendredi soir arrive et qu'aucun nouveau dossier n'apparaît dans `backups/`, consulter `backups/backup.log` en premier : le script y écrit son message d'erreur exact.

## En cas de problème

| Message | Cause probable | Solution |
|---|---|---|
| `mongodump: command not found` | MongoDB Database Tools non installés | Installer le paquet (section Prérequis) |
| `URI manquante dans .env / .env.local` | Fichier `.env` absent ou vide | Vérifier la présence de `ATLAS_URI` |
| `Aucun dump trouvé dans ...` | Restauration lancée sans sauvegarde préalable, ou mauvais chemin | Relancer d'abord la sauvegarde, réutiliser le `dump_path` qu'elle retourne |
| La tâche cron ne se déclenche jamais | Chemin `uv` incorrect dans la ligne cron, ou machine éteinte le vendredi soir | Vérifier le chemin avec `which uv`, vérifier `crontab -l` |
