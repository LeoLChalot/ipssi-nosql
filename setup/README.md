# Guide de setup — Module NoSQL & MongoDB
**NEEKOCODE x IPSSI / MIA4 27.2**

> **Module :** Conception et intégration d'une base NoSQL  
> **Dates :** Du lundi 24 au vendredi 28 août 2026 (en distanciel)  
> **Objectif :** Ce guide installe tout ce dont vous aurez besoin pendant les cinq jours. Suivez-le une fois, tranquillement, et vous n'y reviendrez plus.  
> **Échéance :** À terminer avant lundi 9h00 (comptez 30 à 45 minutes). **Preuve de setup à déposer sur Teams avant dimanche 22h00.**

---

## Sommaire
- [00. Le contrat](#00-le-contrat)
- [01. Ce que vous installez, et pourquoi](#01-ce-que-vous-installez-et-pourquoi)
- [02. Votre serveur MongoDB](#02-votre-serveur-mongodb)
  - [Voie A · Atlas (Recommandée)](#voie-a--atlas-recommandée)
  - [Voie B · Docker](#voie-b--docker)
  - [Voie C · Locale](#voie-c--locale)
- [03. Les outils, quelle que soit votre voie](#03-les-outils-quelle-que-soit-votre-voie)
- [04. L'environnement Python](#04-lenvironnement-python)
- [05. Le test de validation](#05-le-test-de-validation)
- [06. Votre preuve de setup](#06-votre-preuve-de-setup)
- [07. Les erreurs qui vont vous arriver](#07-les-erreurs-qui-vont-vous-arriver)
- [08. Checklist finale](#08-checklist-finale)

---

## 00. Le contrat

**Lundi à 9h00, on écrit des requêtes. On n'installe pas.**

Une installation ratée coûte dix minutes à celui qui la subit et une heure à toute la promo, parce que le formateur ne peut pas être à trente-deux endroits à la fois. C'est la seule raison d'être de ce guide.

Si vous bloquez ce week-end, postez votre message d'erreur dans le canal Teams. Vous aurez une réponse. Si vous bloquez lundi matin sans avoir rien tenté avant, vous perdrez la matinée.

---

## 01. Ce que vous installez, et pourquoi

Cinq briques. Aucune n'est décorative, vous vous servirez des cinq dès lundi après-midi.

| Brique | Rôle | Vous en aurez besoin |
| :--- | :--- | :--- |
| **Un serveur MongoDB** | La base elle-même. Dans le cloud avec Atlas, ou sur votre machine avec Docker. | Dès lundi 14h00 |
| **mongosh** | Le shell. C'est là que vous taperez vos premières requêtes. | Dès lundi 14h00 |
| **MongoDB Database Tools** | Les commandes `mongoimport`, `mongodump`, `mongorestore`. Elles ne sont *pas* incluses dans mongosh. | Lundi 14h00, puis mercredi |
| **Compass** | L'interface graphique. Pour voir vos documents, et pour lire un plan d'exécution sans plisser les yeux. | Dès lundi, indispensable mardi |
| **Python + uv + pymongo** | Piloter MongoDB depuis du code, ce que vous ferez dans le projet. | Lundi 16h00 |

> ⚠️ **Le piège numéro un**  
> Installer `mongosh` ne vous donne pas `mongoimport`. Ce sont deux téléchargements différents. Chaque année, la moitié d'une promo se retrouve bloquée sur ce point précis au moment de charger les données. La section 03 le traite, ne la sautez pas.

---

## 02. Votre serveur MongoDB

Trois voies possibles. Choisissez-en une, faites-la jusqu'au bout. Vous pourrez ajouter la deuxième plus tard si le cœur vous en dit.

### Voie A · Atlas (Recommandée)
*Recommandée · 15 minutes · aucune installation de serveur*

Atlas est le service cloud de MongoDB. Le palier gratuit suffit largement pour ce module, et il est **obligatoire** si vous visez le bonus recherche vectorielle du projet, parce que cette fonctionnalité n'existe que sur Atlas.

#### 1. Créer le compte
Rendez-vous sur `mongodb.com/cloud/atlas/register`. Inscrivez-vous avec votre adresse IPSSI. Confirmez l'e-mail.

#### 2. Créer le cluster
Atlas vous propose plusieurs paliers et pousse discrètement vers les payants. Choisissez explicitement le palier **Free**, aussi appelé **M0**.
- **Fournisseur :** AWS
- **Région :** une région européenne, **Frankfurt** ou **Paris** (une région asiatique ou américaine fonctionnera aussi, mais chaque requête sera lente et vous le sentirez pendant cinq jours).
- **Nom du cluster :** laissez `Cluster0`.

*La création prend deux à trois minutes.*

#### 3. Créer l'utilisateur de la base
Menu **Database Access**, puis **Add New Database User**.  
*Attention : cet utilisateur n'a rien à voir avec votre compte Atlas (ce sont deux identités distinctes, et les confondre est la deuxième cause d'échec de connexion).*
- **Méthode :** mot de passe
- **Nom d'utilisateur :** simple, en minuscules, par exemple `mia4`
- **Mot de passe :** **lettres et chiffres uniquement**. Pas de `@`, `:`, `/`, `#`, `%` (ces caractères ont une signification dans une URL de connexion et casseront votre chaîne).
- **Rôle :** `Read and write to any database`

#### 4. Autoriser votre adresse IP
Menu **Network Access**, puis **Add IP Address**. Choisissez **Allow access from anywhere**, ce qui inscrit `0.0.0.0/0`.

> 💡 **Ce que vous venez de faire**  
> Vous venez d'ouvrir votre base à l'internet entier. C'est acceptable pour une semaine de formation sur des données publiques, depuis des connexions domestiques dont l'adresse change. Ce serait une faute grave en production. On en reparle mercredi, dans le bloc sécurité, et cette décision sera un des exemples.

#### 5. Récupérer la chaîne de connexion
Menu **Database**, bouton **Connect**, puis **Drivers**. Copiez la chaîne. Elle ressemble à ceci :
```text
mongodb+srv://mia4:VOTRE_MOT_DE_PASSE@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```
Remplacez `VOTRE_MOT_DE_PASSE` par le mot de passe de l'étape 3. Atlas ne le réaffiche jamais.

> 🛑 **Règle absolue du module**  
> Cette chaîne contient un mot de passe. Elle ne va **jamais** dans votre code, **jamais** dans un notebook, **jamais** sur GitHub. Elle va dans un fichier `.env.local`, lui-même listé dans `.gitignore`. La section 04 vous montre comment. Un identifiant en clair dans un dépôt rendu coûte des points sur le projet, et vous verrez mercredi que ce n'est pas une règle d'école.

---

### Voie B · Docker
*Pour ceux qui ont déjà Docker · 5 minutes*

Vous avez fait le module Docker, autant s'en servir. Cette voie est parfaitement valable pour tout le socle du module. Elle a même un avantage : votre base survit à une coupure de connexion.  
Sa seule limite est le bonus du projet. La recherche vectorielle n'existe pas dans MongoDB Community, elle est propre à Atlas. Si vous visez ce bonus, faites aussi la voie A, les deux cohabitent sans problème.

#### 1. Lancer le conteneur
```bash
# Le volume nommé garantit que vos données survivent à un docker rm
docker run -d \
  --name mongo8 \
  -p 27017:27017 \
  -v mongo8_data:/data/db \
  mongo:8
```

#### 2. Vérifier
```bash
docker ps
# Vous devez voir mongo8 avec le statut Up et le port 27017
```

#### 3. Votre chaîne de connexion
```text
mongodb://localhost:27017
```
*Pas d'authentification, pas de mot de passe. C'est le confort du local, et c'est aussi pourquoi cette base ne doit jamais être exposée sur un réseau.*

> 💡 **Deux commandes à retenir**  
> `docker stop mongo8` pour l'éteindre le soir, `docker start mongo8` pour le rallumer. Vos données restent en place grâce au volume.

---

### Voie C · Locale
*Dernier recours · 20 minutes · si Atlas et Docker sont hors de portée*

Installation native de MongoDB Community Server sur votre machine. À réserver aux situations où le cloud est bloqué par votre réseau et où Docker n'est pas installable.

#### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community@8.0
brew services start mongodb-community@8.0
```

#### Windows
Téléchargez l'installeur `.msi` depuis `mongodb.com/try/download/community`. Pendant l'installation, cochez **Install MongoDB as a Service** et laissez le port par défaut.

#### Linux (Ubuntu / Debian)
Suivez la procédure officielle du dépôt APT sur `mongodb.com/docs/manual/administration/install-on-linux/`. N'installez pas le paquet `mongodb` des dépôts de votre distribution, il est obsolète depuis des années.

#### Votre chaîne de connexion
```text
mongodb://localhost:27017
```

---

## 03. Les outils, quelle que soit votre voie

Ces trois installations sont communes aux trois voies. Personne n'y coupe.

### mongosh, le shell
```bash
# macOS
brew install mongosh

# Windows (PowerShell)
winget install MongoDB.Shell

# Sinon, téléchargement direct : [mongodb.com/try/download/shell](https://mongodb.com/try/download/shell)
```
*Vérification :* `mongosh --version` doit afficher un numéro de version.

### MongoDB Database Tools
C'est le paquet qui contient `mongoimport`, `mongoexport`, `mongodump` et `mongorestore`. Il se télécharge séparément de `mongosh`.

```bash
# macOS
brew install mongodb/brew/mongodb-database-tools

# Windows : télécharger le .msi sur [mongodb.com/try/download/database-tools](https://mongodb.com/try/download/database-tools)
# puis relancer votre terminal pour que le PATH soit pris en compte
```
*Vérification :* `mongoimport --version` doit afficher un numéro de version. Si vous obtenez « command not found », l'installation n'est pas faite ou le terminal n'a pas été relancé.

### Compass, l'interface graphique
Téléchargez depuis `mongodb.com/try/download/compass`, installez, ouvrez, collez votre chaîne de connexion, cliquez **Connect**.

Compass n'est pas un gadget de confort. Mardi, vous y lirez des plans d'exécution, et personne n'a envie de déchiffrer un `explain()` brut dans un terminal la première fois.

---

## 04. L'environnement Python

On utilise **uv**, le gestionnaire de paquets Python de référence en 2026. Beaucoup plus rapide que pip, et il gère l'environnement virtuel pour vous.

### 1. Installer uv
```bash
# macOS / Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```
Relancez votre terminal, puis vérifiez avec `uv --version`.

### 2. Créer le projet du module
```bash
uv init mia4-nosql
cd mia4-nosql
uv add "pymongo[srv]" python-dotenv
```

> ⚠️ **Les crochets ne sont pas décoratifs**  
> `"pymongo[srv]"` installe en plus la résolution DNS dont les chaînes `mongodb+srv://` d'Atlas ont besoin. Sans les crochets, votre connexion Atlas échouera avec un message parlant de `dnspython`. Les guillemets sont là parce que certains terminaux interprètent les crochets.

### 3. Ranger vos identifiants
Créez un fichier `.env.local` à la racine du projet :
```env
ATLAS_URI=mongodb+srv://mia4:motdepasse@cluster0.xxxxx.mongodb.net/
LOCAL_URI=mongodb://localhost:27017
```

Puis ajoutez cette ligne à votre `.gitignore` :
```gitignore
.env.local
```
*Ce réflexe vaut pour tout le reste de votre carrière, pas seulement pour ce module.*

---

## 05. Le test de validation

Un seul script qui vérifie tout et vous dit oui ou non. C'est lui qui sert de preuve.

Créez un fichier `check_setup.py` à la racine de votre projet, avec exactement ce contenu :

```python
# check_setup.py
# Vérifie que l'environnement du module NoSQL est opérationnel.

import os
import shutil
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv(dotenv_path=".env.local", override=True)

print("=" * 52)
print("  MIA4 NoSQL - vérification de l'environnement")
print("=" * 52)

# --- 1. Versions Python et pymongo ---
import pymongo

print(f"Python  : {sys.version.split()[0]}")
print(f"pymongo : {pymongo.__version__}")

# --- 2. Présence des outils en ligne de commande ---
tools_ok = True
for tool in ("mongosh", "mongoimport", "mongodump"):
    path = shutil.which(tool)
    if path:
        print(f"OK      : {tool} trouvé")
    else:
        print(f"MANQUE  : {tool} introuvable dans le PATH")
        tools_ok = False

# --- 3. Connexion aux serveurs déclarés ---
# On teste toutes les URI présentes dans .env.local.
# Une seule connexion réussie suffit pour valider le setup.
targets = {
    "Atlas": os.environ.get("ATLAS_URI"),
    "Local": os.environ.get("LOCAL_URI"),
}

connected = []
for name, uri in targets.items():
    if not uri:
        print(f"IGNORE  : {name} (aucune URI dans .env.local)")
        continue
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=6000)
        version = client.admin.command("buildInfo")["version"]
        print(f"OK      : {name} joignable, MongoDB {version}")
        connected.append(name)
    except PyMongoError as exc:
        print(f"ECHEC   : {name} - {type(exc).__name__}")
        print(f"          {str(exc)[:160]}")

# --- 4. Verdict ---
print("-" * 52)
if connected and tools_ok:
    print("VERDICT : setup complet. Vous êtes prêt pour lundi.")
elif connected:
    print("VERDICT : connexion OK mais outils manquants.")
    print("          Reprenez la section 03 du guide.")
else:
    print("VERDICT : aucune connexion établie.")
    print("          Reprenez la section 07 du guide.")
print("=" * 52)
```

Lancez-le :
```bash
uv run python check_setup.py
```

Vous devez obtenir une ligne `VERDICT : setup complet`. Tant que ce n'est pas le cas, vous n'avez pas fini.

---

## 06. Votre preuve de setup

Deux minutes de votre temps, qui font gagner une heure à toute la promo.

Faites une capture d'écran de la sortie complète de `check_setup.py`, y compris la ligne de verdict, et déposez-la dans le canal Teams du module.

- **Nom du fichier :** `setup_NOM_Prenom.png`
- **Échéance :** **dimanche 22h00 heure de Paris**
- **Si votre verdict n'est pas bon :** postez quand même la capture. C'est encore plus utile, parce que je verrai votre erreur avant lundi et j'arriverai avec la réponse.

> 💡 **Pourquoi cette contrainte**  
> Les captures déposées dimanche soir sont dépouillées avant le début du cours, ce qui permet d'arriver lundi avec les réponses déjà prêtes pour ceux qui sont bloqués. Un message envoyé lundi à 8h55 arrive trop tard pour être traité avant la séance.

---

## 07. Les erreurs qui vont vous arriver

Elles sont dix, elles reviennent chaque année, et elles ont toutes une cause précise. Cherchez votre message dans la colonne de gauche.

| Ce que vous voyez | Ce qui se passe vraiment | Ce que vous faites |
| :--- | :--- | :--- |
| `ServerSelectionTimeoutError`, ou « timed out » | Votre adresse IP n'est pas autorisée sur le cluster Atlas. | Network Access, ajoutez `0.0.0.0/0`, attendez une minute que le changement se propage. |
| `Authentication failed` ou `bad auth` | Vous utilisez votre compte Atlas au lieu de l'utilisateur de base de données. Ce sont deux choses différentes. | Database Access, recréez un utilisateur, notez son mot de passe, refaites la chaîne. |
| Connexion refusée sans message clair, alors que le mot de passe est bon | Votre mot de passe contient un caractère spécial qui casse l'URL : `@`, `:`, `/`, `#`, `%`. | Changez-le pour un mot de passe uniquement alphanumérique. C'est plus rapide que d'encoder. |
| `mongoimport: command not found` | Les Database Tools ne sont pas installés. `mongosh` ne les contient pas. | Section 03, deuxième bloc. Puis relancez votre terminal. |
| `Failed: cannot decode array into a Document` | Le fichier JSON est un tableau unique, et vous avez oublié le drapeau qui le dit. | Ajoutez `--jsonArray` à votre commande `mongoimport`. Tous les jeux de données du module sont dans ce cas. |
| `dnspython module must be installed` | pymongo a été installé sans le support des URI `mongodb+srv://`. | `uv add "pymongo[srv]"`, avec les crochets et les guillemets. |
| `mongosh` introuvable sous Windows alors que l'installation a réussi | Le PATH n'est pas rechargé dans le terminal ouvert. | Fermez complètement le terminal et rouvrez-le. Si ça persiste, redémarrez la session Windows. |
| `port is already allocated` au lancement Docker | Un autre conteneur ou un MongoDB local occupe déjà le port 27017. | `docker rm -f mongo8` puis relancez, ou changez le port hôte en `-p 27018:27017`. |
| Atlas inaccessible depuis le réseau de l'entreprise ou de l'école | Le port sortant 27017 est filtré par le pare-feu. | Basculez sur la voie B, Docker en local. Refaites la voie A depuis chez vous le soir. |
| Le cluster Atlas affiche `Paused` | Un cluster gratuit se met en pause après une longue inactivité. | Cliquez **Resume**, patientez deux minutes. |

> ⚠️ **Si rien de tout cela ne correspond**  
> Postez dans le canal Teams : le message d'erreur **complet**, votre système d'exploitation, et la voie que vous avez choisie. Une capture d'écran vaut mieux qu'un message d'erreur recopié de mémoire.

---

## 08. Checklist finale

- [ ] **Serveur MongoDB opérationnel** : Cluster Atlas M0 créé, ou conteneur Docker qui tourne, ou installation locale démarrée
- [ ] **Utilisateur et accès réseau configurés** : *(Voie A uniquement)* utilisateur de base créé, IP autorisée
- [ ] **Chaîne de connexion en main** : Testée au moins une fois, et rangée dans `.env.local`
- [ ] **mongosh installé** : `mongosh --version` répond
- [ ] **Database Tools installés** : `mongoimport --version` répond
- [ ] **Compass installé et connecté** : Vous voyez vos bases dans l'interface
- [ ] **uv installé** : `uv --version` répond
- [ ] **Projet Python créé** : `mia4-nosql` avec `pymongo` et `python-dotenv`
- [ ] **`.env.local` créé et ignoré par git** : La ligne est bien dans `.gitignore`
- [ ] **`check_setup.py` affiche « setup complet »** : Le seul critère qui compte vraiment
- [ ] **Capture déposée sur Teams** : Avant dimanche 22h00 heure de Paris

---

**NEEKOCODE** pour IPSSI · Module *« Conception et intégration d'une base de données NoSQL »* · MIA4 27.2 · 24 au 28 août 2026  
*Une question ce week-end : le canal Teams du module. Un message avec un vrai message d'erreur obtient toujours une vraie réponse.*
