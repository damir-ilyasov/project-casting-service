"""Классы Project, Role и функции для работы с коллекцией проектов."""

from typing import List, Optional


class Role:
    """Роль в рамках проекта, на которую ищут кандидата."""

    def __init__(self, role_id: int, name: str) -> None:
        """Создать объект роли."""
        self.id = role_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление роли."""
        return f"[{self.id}] {self.name}"


class Project:
    """Проект (фильм, сериал, реклама и т.п.), для которого проводится кастинг."""

    def __init__(self, project_id: int, name: str) -> None:
        """Создать объект проекта с пустым списком ролей."""
        self.id = project_id
        self.name = name
        self.roles: List[Role] = []

    def add_role(self, name: str) -> Role:
        """Добавить роль в проект и вернуть созданный объект роли."""
        role_id = max((role.id for role in self.roles), default=0) + 1
        role = Role(role_id, name)
        self.roles.append(role)
        return role

    def find_role(self, role_id: int) -> Optional[Role]:
        """Найти роль проекта по идентификатору."""
        for role in self.roles:
            if role.id == role_id:
                return role
        return None

    def __str__(self) -> str:
        """Вернуть строковое представление проекта."""
        return f"{self.name} ({len(self.roles)} ролей)"


def add_project(projects: List[Project], name: str) -> Project:
    """Создать проект, добавить его в коллекцию и вернуть созданный объект."""
    project_id = max((project.id for project in projects), default=0) + 1
    project = Project(project_id, name)
    projects.append(project)
    return project


def find_project_by_id(projects: List[Project], project_id: int) -> Optional[Project]:
    """Найти проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project
    return None


def find_project(projects: List[Project], query: str) -> List[Project]:
    """Найти проекты, в названии которых встречается подстрока query."""
    query = query.lower()
    return [project for project in projects if query in project.name.lower()]


def filter_projects_with_open_roles(projects: List[Project]) -> List[Project]:
    """Отобрать проекты, в которых есть хотя бы одна роль.

    Использует генератор для отбора подходящих проектов.
    """
    return [project for project in projects if len(project.roles) > 0]


def sort_projects_by_role_count(projects: List[Project]) -> List[Project]:
    """Отсортировать проекты по количеству ролей (по убыванию)."""
    return sorted(projects, key=lambda project: len(project.roles), reverse=True)
