#!/usr/bin/env python3
"""Sauvegarde hebdomadaire de la base securite_routiere. A lancer via cron chaque vendredi."""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
env = {**dotenv_values(ROOT / ".env.local"), **dotenv_values(ROOT / ".env")}
ATLAS_URI = env.get("ATLAS_URI")
DB_NAME = "securite_routiere"
BACKUP_DIR = ROOT / "backups"
BACKUP_DIR.mkdir(exist_ok=True)


def main() -> int:
    if not ATLAS_URI:
        print("ATLAS_URI manquant dans .env / .env.local", file=sys.stderr)
        return 1

    timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    target = BACKUP_DIR / f"{DB_NAME}_{timestamp}"

    result = subprocess.run(
        ["mongodump", f"--uri={ATLAS_URI}", f"--db={DB_NAME}", f"--out={target}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"mongodump a échoué :\n{result.stderr}", file=sys.stderr)
        return 1

    print(f"Sauvegarde créée : {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
