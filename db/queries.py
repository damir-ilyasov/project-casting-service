"""SQL-запросы, используемые Django-представлениями."""

from types import SimpleNamespace

from db.database import get_connection, initialize_database
from db.import_json import import_json_data


def _ensure_data():
    """Подготовить схему и импортировать JSON при первом запуске."""
    initialize_database()
    with get_connection() as connection:
        project_count = connection.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0]
    if project_count == 0:
        import_json_data()


def get_projects(search=""):
    """Вернуть проекты с ролями и отметкой занятости каждой роли."""
    _ensure_data()
    with get_connection() as connection:
        if search:
            rows = connection.execute(
                """SELECT id, name FROM projects
                   WHERE name LIKE ? ORDER BY name""",
                (f"%{search}%",),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT id, name FROM projects ORDER BY name"
            ).fetchall()

        projects = []
        for row in rows:
            project = SimpleNamespace(id=row["id"], name=row["name"], roles=[])
            role_rows = connection.execute(
                """SELECT r.id, r.name,
                          NOT EXISTS (
                            SELECT 1 FROM applications a
                            WHERE a.project_id = r.project_id
                              AND a.role_id = r.id AND a.status = 'accepted'
                          ) AS available
                   FROM roles r WHERE r.project_id = ? ORDER BY r.id""",
                (project.id,),
            ).fetchall()
            project.roles = [
                SimpleNamespace(
                    id=role["id"],
                    name=role["name"],
                    available=bool(role["available"]),
                )
                for role in role_rows
            ]
            projects.append(project)
        return projects


def get_project(project_id):
    """Вернуть один проект с ролями либо None."""
    projects = get_projects()
    return next((project for project in projects if project.id == project_id), None)


def get_applications(status=""):
    """Вернуть заявки с данными связанных кандидата, проекта и роли."""
    _ensure_data()
    sql = """SELECT a.id, a.status,
                    c.id AS candidate_id, c.name AS candidate_name,
                    c.contact AS candidate_contact,
                    p.id AS project_id, p.name AS project_name,
                    r.id AS role_id, r.name AS role_name
             FROM applications a
             JOIN candidates c ON c.id = a.candidate_id
             JOIN projects p ON p.id = a.project_id
             JOIN roles r ON r.project_id = a.project_id AND r.id = a.role_id"""
    params = ()
    if status:
        sql += " WHERE a.status = ?"
        params = (status,)
    sql += " ORDER BY a.id DESC"

    with get_connection() as connection:
        rows = connection.execute(sql, params).fetchall()

    return [
        SimpleNamespace(
            id=row["id"],
            status=row["status"],
            candidate=SimpleNamespace(
                id=row["candidate_id"],
                name=row["candidate_name"],
                contact=row["candidate_contact"],
            ),
            project=SimpleNamespace(id=row["project_id"], name=row["project_name"]),
            role=SimpleNamespace(id=row["role_id"], name=row["role_name"]),
        )
        for row in rows
    ]


def get_application(application_id):
    """Получить заявку по ID через параметризованный SQL-запрос."""
    return next(
        (item for item in get_applications() if item.id == application_id),
        None,
    )
