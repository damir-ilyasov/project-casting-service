"""Низкоуровневая работа с SQLite для веб-приложения Casting Service."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "casting_service.sqlite3"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection():
    """Открыть соединение SQLite с доступом к столбцам по имени."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Создать таблицы и индексы согласно sql/schema.sql."""
    with get_connection() as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
