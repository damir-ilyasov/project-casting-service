"""Однократная загрузка исходных данных JSON в SQLite."""

import json
from pathlib import Path

from db.database import BASE_DIR, get_connection, initialize_database


def _read_json(filename):
    path = BASE_DIR / "data" / filename
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def import_json_data(force=False):
    """Импортировать проекты, роли, кандидатов и заявки из JSON.

    При force=True содержимое таблиц заменяется данными из файлов.
    Без force импорт выполняется только в пустую базу.
    """
    initialize_database()
    projects = _read_json("projects.json")
    candidates = _read_json("candidates.json")
    applications = _read_json("applications.json")

    with get_connection() as connection:
        count = connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        if count and not force:
            return {"projects": count, "imported": False}

        connection.execute("DELETE FROM applications")
        connection.execute("DELETE FROM roles")
        connection.execute("DELETE FROM candidates")
        connection.execute("DELETE FROM projects")

        for project in projects:
            connection.execute(
                "INSERT INTO projects (id, name) VALUES (?, ?)",
                (project["id"], project["name"]),
            )
            connection.executemany(
                "INSERT INTO roles (id, project_id, name) VALUES (?, ?, ?)",
                [
                    (role["id"], project["id"], role["name"])
                    for role in project.get("roles", [])
                ],
            )

        connection.executemany(
            "INSERT INTO candidates (id, name, contact) VALUES (?, ?, ?)",
            [(item["id"], item["name"], item["contact"]) for item in candidates],
        )
        connection.executemany(
            """INSERT INTO applications
               (id, project_id, role_id, candidate_id, status)
               VALUES (?, ?, ?, ?, ?)""",
            [
                (
                    item["id"],
                    item["project_id"],
                    item["role_id"],
                    item["candidate_id"],
                    item["status"],
                )
                for item in applications
            ],
        )

        return {
            "projects": len(projects),
            "roles": sum(len(project.get("roles", [])) for project in projects),
            "candidates": len(candidates),
            "applications": len(applications),
            "imported": True,
        }


if __name__ == "__main__":
    print(import_json_data(force=True))
