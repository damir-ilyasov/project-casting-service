"""Тесты схемы SQLite и переноса данных из JSON."""

import sqlite3

from db import database
from db.import_json import import_json_data


def test_import_json_populates_all_tables(tmp_path, monkeypatch):
    """Импорт переносит записи во все четыре таблицы."""
    monkeypatch.setattr(database, "DB_DIR", tmp_path)
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.sqlite3")
    monkeypatch.setattr(
        database,
        "SCHEMA_PATH",
        database.BASE_DIR / "sql" / "schema.sql",
    )

    result = import_json_data(force=True)

    assert result["imported"] is True
    assert result["projects"] == 2
    assert result["roles"] == 4
    assert result["candidates"] == 1
    assert result["applications"] == 1

    with database.get_connection() as connection:
        row = connection.execute(
            """SELECT c.name AS candidate, p.name AS project, r.name AS role
               FROM applications a
               JOIN candidates c ON c.id = a.candidate_id
               JOIN projects p ON p.id = a.project_id
               JOIN roles r ON r.project_id = a.project_id AND r.id = a.role_id
               WHERE a.id = ?""",
            (1,),
        ).fetchone()

    assert row["candidate"] == "Иван Иванов"
    assert row["project"] == "Сериал"
    assert row["role"] == "Главный герой"


def test_application_status_constraint(tmp_path, monkeypatch):
    """SQLite запрещает статус заявки вне разрешённого списка."""
    monkeypatch.setattr(database, "DB_DIR", tmp_path)
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.sqlite3")
    database.initialize_database()

    with database.get_connection() as connection:
        connection.execute("INSERT INTO projects (id, name) VALUES (1, 'Project')")
        connection.execute(
            "INSERT INTO roles (id, project_id, name) VALUES (1, 1, 'Role')"
        )
        connection.execute(
            "INSERT INTO candidates (id, name, contact) VALUES (1, 'Candidate', 'test')"
        )
        try:
            connection.execute(
                """INSERT INTO applications
                   (id, project_id, role_id, candidate_id, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (99, 1, 1, 1, "unknown"),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("SQLite should reject an invalid status")
