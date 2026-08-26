# check_setup.py
# Verifie que l'environnement du module NoSQL est operationnel.

import os
import shutil
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv(dotenv_path=".env.local", override=True)
load_dotenv(dotenv_path=".env", override=True)

print("=" * 52)
print("  MIA4 NoSQL - verification de l'environnement")
print("=" * 52)

# --- 1. Versions Python et pymongo ---
import pymongo

print(f"Python  : {sys.version.split()[0]}")
print(f"pymongo : {pymongo.__version__}")

# --- 2. Presence des outils en ligne de commande ---
tools_ok = True
for tool in ("mongosh", "mongoimport", "mongodump"):
    path = shutil.which(tool)
    if path:
        print(f"OK      : {tool} trouve")
    else:
        print(f"MANQUE  : {tool} introuvable dans le PATH")
        tools_ok = False

print("-" * 52)

# --- 3. Connexion aux serveurs declares ---
# On teste toutes les URI presentes dans .env.local.
# Une seule connexion reussie suffit pour valider le setup.
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
    print("VERDICT : Setup complet. Vous êtes pret pour travailler.")
elif connected:
    print("VERDICT : Connexion OK mais outils manquants.")
    print("          Reprenez la section 03 du guide.")
else:
    print("VERDICT : Aucune connexion etablie.")
    print("          Reprenez la section 07 du guide.")
print("=" * 52)
