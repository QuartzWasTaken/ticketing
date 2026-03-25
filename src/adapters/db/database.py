"""
Utilitaires helper pour SQLite.

Ce module fournit des fonctions pour gerer les connexions SQLite,
l'initialisation de la base de donnees et la creation du schema.
"""

import sqlite3
from pathlib import Path
from typing import Optional


def get_connection(db_path: str = "ticketing.db") -> sqlite3.Connection:
    """
    Obtient une connexion a la base de donnees SQLite.

    Args:
        db_path: Chemin vers le fichier de base de donnees

    Returns:
        Connexion SQLite avec Row factory active
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path: str = "ticketing.db", schema_path: Optional[str] = None):
    """
    Initialise la base de donnees en creant les tables depuis schema.sql.

    Args:
        db_path: Chemin vers le fichier de base de donnees
        schema_path: Chemin vers le fichier schema.sql (optionnel)
    """
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"

    if not Path(schema_path).exists():
        raise FileNotFoundError(f"Fichier schema non trouve : {schema_path}")

    conn = get_connection(db_path)
    cursor = conn.cursor()

    with open(schema_path, encoding="utf-8") as file:
        schema_sql = file.read()
        cursor.executescript(schema_sql)

    conn.commit()
    conn.close()


def close_connection(conn: sqlite3.Connection):
    """
    Ferme une connexion a la base de donnees.

    Args:
        conn: La connexion a fermer
    """
    if conn:
        conn.close()
