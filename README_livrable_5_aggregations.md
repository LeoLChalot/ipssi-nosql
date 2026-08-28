# Livrable 5 — Rapport analytique par agrégations

Ce notebook correspond à la partie **rapport analytique par agrégations** du projet final.

Le but est de répondre à des questions compréhensibles même sans connaître le BAAC ou MongoDB.

Notebook concerné : `notebook_livrable_5_aggregations.ipynb`

Les calculs métier sont faits directement dans MongoDB avec des pipelines d'agrégation. Pandas et Matplotlib servent seulement à afficher les résultats.

---

## 1. Prérequis

Le notebook travaille directement sur la collection finale Atlas :

```text
Base       : securite_routiere
Collection : accidents
```

Il faut avoir :

- Python 3.12 ou plus récent ;
- `uv` ;
- accès au cluster MongoDB Atlas du projet ;
- les dépendances du projet ;
- un fichier `.env` ou `.env.local` avec `ATLAS_URI`.

Installation de l'environnement :

```powershell
uv sync
```

Les principales librairies utilisées ici sont :

```text
pymongo
python-dotenv
pandas
matplotlib
```

Si `securite_routiere.accidents` n'est pas encore chargée, exécuter d'abord le notebook principal d'ingestion du projet.

---

## 2. Lancer le notebook

Dans VS Code :

1. ouvrir `notebook_livrable_5_aggregations.ipynb` ;
2. sélectionner le kernel du `.venv` ;
3. vérifier la présence de `ATLAS_URI` dans `.env` ou `.env.local` ;
4. lancer **Run All** ;
5. enregistrer le notebook avec ses tableaux et graphiques.

Le notebook ne recharge pas les CSV et ne fait aucun `drop()` de collection. Il travaille uniquement en lecture sur la base finale.

---

## 3. Contrôle avant analyse

Quelques doublons ont été ajoutés dans la base partagée pendant les tests.

Chaque analyse commence donc par :

```text
$group par Num_Acc
$replaceRoot
```

Le but est de garder un seul document par accident avant de calculer les statistiques.

Cela évite qu'un doublon de test fasse monter artificiellement un résultat.

---

## 4. Analyse 1 — Heure et semaine / week-end

Question :

> La part d'usagers tués varie-t-elle selon l'heure et entre semaine et week-end ?

Les usagers sont stockés dans :

```text
vehicules[].usagers[]
```

On utilise donc deux `$unwind` pour pouvoir analyser chaque usager séparément.

Le pipeline utilise ensuite :

```text
$hour
$dayOfWeek
$group
$project
$sort
```

Résultats observés :

```text
Semaine
Pic à 3 h
8,03 % d'usagers tués
585 usagers impliqués

Week-end
Pic à 2 h
5,83 % d'usagers tués
1 046 usagers impliqués
```

Ce résultat décrit la part d'usagers tués **parmi les personnes déjà impliquées dans un accident**.

Il ne dit pas qu'on a plus de risque d'avoir un accident à 3 h.

---

## 5. Analyse 2 — Gravité selon le mode de déplacement

Question :

> Quels modes de déplacement présentent la plus forte proportion d'usagers tués ou hospitalisés ?

On considère ici comme conséquence grave :

```text
grav = 2 : Tué
grav = 3 : Blessé hospitalisé
```

Les groupes retenus sont :

```text
Piéton
Vélo
Deux-roues motorisé
Voiture légère
```

Résultats :

```text
Deux-roues motorisés : 35,75 %
Piétons              : 32,86 %
Vélos                 : 27,56 %
Voitures légères     : 12,54 %
```

Les catégories sont construites à partir de `catu` et `catv`.

Pour les deux-roues motorisés, on retient notamment le code `2` ainsi que les codes `30` à `34` du BAAC.

### Limite importante

Ces pourcentages ne mesurent pas le risque d'avoir un accident.

Pour faire ça correctement, il faudrait aussi connaître l'exposition de chaque mode de déplacement : kilomètres parcourus, nombre d'usagers en circulation, temps passé sur la route, etc.

Ici on compare seulement la gravité des conséquences une fois que l'usager est déjà impliqué dans un accident.

---

## 6. Analyse 3 — Type de route et mortalité

Question :

> Quels types de routes ont le plus d'accidents corporels et quelle part de ces accidents est mortelle ?

Types de routes comparés :

```text
Autoroute
Route nationale
Route départementale
Voie communale
```

Le point important du pipeline est le retour à l'unité **accident** après les `$unwind`.

On regroupe par `Num_Acc`, puis :

```python
"$max": {
    "$cond": [
        {"$eq": ["$vehicules.usagers.grav", 2]},
        1,
        0
    ]
}
```

Si au moins un usager est tué, l'accident vaut `1`.

Même si plusieurs personnes sont tuées dans le même accident, cet accident reste compté une seule fois.

Résultats :

```text
Part d'accidents mortels

Route départementale : 9,27 %
Route nationale      : 7,96 %
Autoroute             : 4,44 %
Voie communale        : 2,92 %
```

En volume :

```text
Voie communale : 22 910 accidents
```

C'est le résultat principal de cette analyse : la catégorie avec le plus d'accidents n'est pas forcément celle où les accidents sont proportionnellement les plus mortels.

Les quatre catégories utilisées couvrent environ **95,94 %** des accidents distincts de la collection utilisée pendant le test.

---

## 7. Pourquoi ces trois analyses

On a volontairement gardé trois questions simples à expliquer :

```text
Quand ?
Pour qui ?
Sur quel type de route ?
```

Elles utilisent aussi plusieurs mécanismes MongoDB différents :

```text
$unwind
$project
$group
$cond
$switch
$max
$sort
```

Le but n'était pas de faire les pipelines les plus longs possibles mais d'avoir des calculs qu'on peut expliquer et vérifier.

---

## 8. Limites du rapport

Les résultats sont descriptifs.

On ne cherche pas à prouver qu'une heure, un type de route ou un mode de déplacement cause directement la gravité d'un accident.

Le BAAC est une base administrative brute. Certaines valeurs peuvent être manquantes, inconnues ou mal renseignées.

Autre point : la base décrit les accidents corporels relevés par les forces de l'ordre. Elle ne représente donc pas tous les petits incidents de circulation.

Ces limites sont gardées dans le notebook car elles changent la manière d'interpréter les graphiques.

---

## 9. Résultats attendus au lancement

Le notebook doit afficher :

```text
Connexion Atlas : OK
```

puis :

- le contrôle des doublons ;
- le tableau et le graphique heure / semaine-week-end ;
- le tableau et le graphique par mode de déplacement ;
- le tableau et le graphique par type de route ;
- les conclusions associées ;
- `Connexion fermée`.

Les sorties sont conservées dans le notebook pour le rendu.

---

## 10. Sécurité

La connexion Atlas est lue depuis :

```text
.env
ou
.env.local
```

Aucune chaîne de connexion complète ne doit être écrite dans le notebook ou dans le dépôt.

Avant de commit :

```powershell
git status
```

et vérifier qu'aucun fichier d'environnement n'est suivi.
