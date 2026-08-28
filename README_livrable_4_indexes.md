# Livrable 4 — Indexation MongoDB

Ce notebook correspond à la partie index justifiés et mesurés du projet final.

Le but ici n'est pas juste de créer des index. Pour chaque index, on part d'une requête réelle, on mesure son comportement sans index, puis on refait exactement la même requête avec l'index.

Notebook concerné : `notebook_livrable_4_indexes.ipynb`

---

## 1. Prérequis

Le projet doit déjà être installé et la collection finale doit être chargée sur MongoDB Atlas.

Le notebook travaille sur :

```text
Base       : securite_routiere
Collection : accidents
```

Il faut avoir :

- Python 3.12 ou plus récent ;
- `uv` ;
- accès au cluster MongoDB Atlas du projet ;
- les dépendances du projet installées ;
- un fichier `.env` ou `.env.local` contenant `ATLAS_URI`.

Les identifiants Atlas ne doivent jamais être écrits directement dans le notebook ou dans ce README.

Pour installer l'environnement :

```powershell
uv sync
```

Si la collection `securite_routiere.accidents` n'existe pas encore, il faut d'abord exécuter le notebook principal d'ingestion du projet.

---

## 2. Structure attendue

Le notebook utilise surtout les champs suivants :

```text
Num_Acc
dep
atm
localisation
vehicules[].usagers[].grav
```

`localisation` est stocké au format GeoJSON :

```json
{
  "type": "Point",
  "coordinates": [2.3522, 48.8566]
}
```

L'ordre est bien :

```text
[longitude, latitude]
```

---

## 3. Lancer le notebook

Depuis VS Code :

1. ouvrir `notebook_livrable_4_indexes.ipynb` ;
2. sélectionner le kernel Python du `.venv` du projet ;
3. vérifier que `.env` ou `.env.local` contient bien `ATLAS_URI` ;
4. lancer **Run All**.

Le notebook doit rester enregistré avec ses sorties pour le rendu.

---

## 4. Méthode utilisée

Pour ne pas supprimer les index de la base partagée pendant les tests, la mesure "avant" est faite avec :

```python
hint={"$natural": 1}
```

Cela force MongoDB à parcourir la collection.

La mesure "après" force ensuite l'index testé.

On regarde surtout :

- le nombre de documents retournés ;
- le nombre de documents examinés ;
- le nombre de clés examinées ;
- le temps d'exécution ;
- le passage de `COLLSCAN` à `IXSCAN`.

Le temps seul n'est pas suffisant pour juger un index, surtout sur une collection d'environ 54 000 documents. La baisse du nombre de documents examinés est plus parlante.

---

## 5. Index testés

### `idx_num_acc`

```python
[("Num_Acc", 1)]
```

Requête servie :

```python
{"Num_Acc": 202400034184}
```

Résultat observé :

```text
Avant : 54 407 documents examinés
Après : 1 document examiné
Réduction : 99,998 %
```

`Num_Acc` sert à retrouver directement un accident.

L'index n'est pas déclaré `unique` dans le notebook de test car des doublons ont été ajoutés temporairement dans la collection pendant les tests du groupe.

---

### `idx_dep_atm`

```python
[("dep", 1), ("atm", 1)]
```

Requête servie :

```python
{"dep": "75", "atm": 2}
```

Résultat observé :

```text
Avant : 54 407 documents examinés
Après : 641 documents examinés
Réduction : 98,822 %
```

`dep` est placé en premier pour que l'index reste aussi utilisable sur une recherche filtrée uniquement par département.

Le département est stocké comme une chaîne et pas comme un entier, notamment parce que les codes BAAC peuvent contenir des valeurs comme `2A` ou `2B`.

---

### `idx_usagers_gravite`

```python
[("vehicules.usagers.grav", 1)]
```

Requête servie :

```python
{"vehicules.usagers.grav": 2}
```

Résultat observé :

```text
Avant : 54 407 documents examinés
Après : 3 226 documents examinés
Réduction : 94,071 %
```

Les usagers sont stockés dans des tableaux imbriqués dans les véhicules. MongoDB crée donc un index **multikey** sur ce champ.

Dans le BAAC, `grav = 2` correspond à un usager tué.

---

### `idx_localisation_2dsphere`

```python
[("localisation", "2dsphere")]
```

Requête servie : recherche des accidents dans un rayon de 5 km autour du centre de Paris.

```python
{
    "localisation": {
        "$geoWithin": {
            "$centerSphere": [
                [2.3522, 48.8566],
                5 / 6378.1
            ]
        }
    }
}
```

Résultat observé :

```text
Avant : 54 407 documents examinés
Après : 4 421 documents examinés
Réduction : 91,874 %
```

Le rayon est divisé par le rayon moyen de la Terre car `$centerSphere` attend une valeur en radians.

---

## 6. Pourquoi seulement ces index

On n'a pas indexé tous les champs.

Un index améliore les lectures, mais il prend de la place et doit aussi être mis à jour lors des écritures. Le choix a donc été limité à des requêtes qu'on utilise réellement dans le projet :

- recherche d'un accident ;
- filtre territorial + météo ;
- recherche sur la gravité des usagers ;
- recherche géographique.

---

## 7. Point connu

La base utilisée pendant les tests contenait quelques doublons ajoutés par l'équipe.

Les tests ont permis de repérer notamment plusieurs documents avec le même `Num_Acc`. Rien n'a été supprimé depuis ce notebook : il ne sert pas à nettoyer les données, seulement à mesurer les index.

Une fois les données finales figées, `Num_Acc` pourra de nouveau être contrôlé comme identifiant unique si la collection respecte bien la règle **un document = un accident**.

---

## 8. Fichiers liés

```text
notebook_livrable_4_indexes.ipynb
docs/indexes.md
docs/images/
```

`docs/indexes.md` contient le détail des mesures et les captures Compass utilisées pendant les premiers tests.

---

## 9. Sécurité

Aucune URI Atlas complète, aucun mot de passe et aucun fichier `.env` ne doivent être commités.

Avant un push :

```powershell
git status
```

et vérifier que `.env` / `.env.local` ne sont pas suivis par Git.
