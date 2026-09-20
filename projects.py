"""Функции для работы с проектами и ролями кастинга.

Проекты хранятся в словаре projects: ключ — id проекта (int),
значение — словарь {"name": str, "roles": list[dict]}.
Каждая роль — словарь {"id": int, "name": str}.
"""


def add_project(projects: dict[int, dict], name: str) -> int:
    """Добавить новый проект в словарь projects.

    :param projects: словарь проектов
    :param name: название проекта (фильм, сериал, реклама и т.п.)
    :return: идентификатор созданного проекта
    """
    project_id = max(projects.keys(), default=0) + 1
    projects[project_id] = {"name": name, "roles": []}
    return project_id


def add_role(projects: dict[int, dict], project_id: int, role_name: str) -> int:
    """Добавить роль в существующий проект.

    :param projects: словарь проектов
    :param project_id: идентификатор проекта
    :param role_name: название роли
    :return: идентификатор созданной роли
    :raises KeyError: если проект с указанным id не найден
    """
    if project_id not in projects:
        raise KeyError(f"Проект с id={project_id} не найден")

    roles = projects[project_id]["roles"]
    role_id = max((role["id"] for role in roles), default=0) + 1
    roles.append({"id": role_id, "name": role_name})
    return role_id


def find_project(projects: dict[int, dict], query: str) -> list[dict]:
    """Найти проекты, в названии которых встречается подстрока query.

    :param projects: словарь проектов
    :param query: искомая подстрока названия
    :return: список найденных проектов вида {"id": int, "name": str}
    """
    query = query.lower()
    return [
        {"id": project_id, "name": data["name"]}
        for project_id, data in projects.items()
        if query in data["name"].lower()
    ]


def get_role(projects: dict[int, dict], project_id: int, role_id: int) -> dict | None:
    """Найти роль по идентификаторам проекта и роли.

    :param projects: словарь проектов
    :param project_id: идентификатор проекта
    :param role_id: идентификатор роли
    :return: словарь роли либо None, если роль не найдена
    """
    project = projects.get(project_id)
    if project is None:
        return None

    for role in project["roles"]:
        if role["id"] == role_id:
            return role
    return None


def filter_projects_with_open_roles(projects: dict[int, dict]) -> list[dict]:
    """Отобрать проекты, в которых есть хотя бы одна роль.

    Использует генератор для отбора подходящих проектов.

    :param projects: словарь проектов
    :return: список подходящих проектов
    """
    return [
        {"id": project_id, "name": data["name"], "roles": data["roles"]}
        for project_id, data in projects.items()
        if len(data["roles"]) > 0
    ]


def sort_projects_by_role_count(projects: dict[int, dict]) -> list[dict]:
    """Отсортировать проекты по количеству ролей (по убыванию).

    :param projects: словарь проектов
    :return: список проектов, упорядоченный по числу ролей
    """
    items = [
        {"id": project_id, "name": data["name"], "roles": data["roles"]}
        for project_id, data in projects.items()
    ]
    return sorted(items, key=lambda project: len(project["roles"]), reverse=True)
