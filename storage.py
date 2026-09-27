"""Функции сохранения и загрузки объектов проекта в JSON-файлах.

Использование классов не отменяет хранение данных в JSON: при загрузке
данные из файла преобразуются в объекты Project, Role, Candidate и
Application, а перед сохранением объекты преобразуются обратно в
структуры JSON.
"""

import json
from typing import List

from models import Application, Candidate, Project, Role
from models.candidates import find_candidate_by_id
from models.projects import find_project_by_id


def load_projects(filename: str) -> List[Project]:
    """Загрузить проекты из JSON-файла и создать объекты Project.

    :param filename: путь к JSON-файлу с проектами
    :return: список объектов Project; пустой список, если файл отсутствует
        или повреждён
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_projects = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый список проектов")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные проектов не загружены")
        return []

    projects: List[Project] = []
    for item in raw_projects:
        project = Project(item["id"], item["name"])
        project.roles = [
            Role(role["id"], role["name"]) for role in item["roles"]
        ]
        projects.append(project)
    return projects


def save_projects(filename: str, projects: List[Project]) -> None:
    """Сохранить объекты Project в JSON-файл.

    :param filename: путь к JSON-файлу с проектами
    :param projects: список объектов Project
    """
    raw_projects = [
        {
            "id": project.id,
            "name": project.name,
            "roles": [
                {"id": role.id, "name": role.name} for role in project.roles
            ],
        }
        for project in projects
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_projects, file, ensure_ascii=False, indent=2)


def load_candidates(filename: str) -> List[Candidate]:
    """Загрузить кандидатов из JSON-файла и создать объекты Candidate.

    :param filename: путь к JSON-файлу с кандидатами
    :return: список объектов Candidate; пустой список, если файл отсутствует
        или повреждён
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_candidates = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый список кандидатов")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные кандидатов не загружены")
        return []

    return [Candidate.from_data(item) for item in raw_candidates]


def save_candidates(filename: str, candidates: List[Candidate]) -> None:
    """Сохранить объекты Candidate в JSON-файл.

    :param filename: путь к JSON-файлу с кандидатами
    :param candidates: список объектов Candidate
    """
    raw_candidates = [
        {"id": candidate.id, "name": candidate.name, "contact": candidate.contact}
        for candidate in candidates
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_candidates, file, ensure_ascii=False, indent=2)


def load_applications(
    filename: str,
    projects: List[Project],
    candidates: List[Candidate],
) -> List[Application]:
    """Загрузить заявки из JSON-файла, связав их с проектами и кандидатами.

    Заявка, для которой не найден проект, роль или кандидат, пропускается:
    такая заявка не может быть корректно восстановлена как объект.

    :param filename: путь к JSON-файлу с заявками
    :param projects: список уже загруженных объектов Project
    :param candidates: список уже загруженных объектов Candidate
    :return: список объектов Application
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_applications = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый список заявок")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные заявок не загружены")
        return []

    applications: List[Application] = []
    for item in raw_applications:
        project = find_project_by_id(projects, item["project_id"])
        candidate = find_candidate_by_id(candidates, item["candidate_id"])
        if project is None or candidate is None:
            continue

        role = project.find_role(item["role_id"])
        if role is None:
            continue

        application = Application(
            item["id"], candidate, project, role, item["status"]
        )
        applications.append(application)
    return applications


def save_applications(filename: str, applications: List[Application]) -> None:
    """Сохранить объекты Application в JSON-файл.

    Ссылки на объекты Project и Candidate преобразуются в их
    идентификаторы (project_id, role_id, candidate_id).

    :param filename: путь к JSON-файлу с заявками
    :param applications: список объектов Application
    """
    raw_applications = [
        {
            "id": application.id,
            "project_id": application.project.id,
            "role_id": application.role.id,
            "candidate_id": application.candidate.id,
            "status": application.status,
        }
        for application in applications
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_applications, file, ensure_ascii=False, indent=2)
