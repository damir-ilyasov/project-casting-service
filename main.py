"""Точка входа приложения «Сервис проведения кастингов» (объектная модель ПР3).

Программа больше не хранит проекты, кандидатов и заявки в виде словарей:
основные данные передаются в виде коллекций объектов List[Project],
List[Candidate], List[Application]. Создание, поиск и взаимодействие
объектов организовано через классы и функции пакета models.
"""

from typing import List

from models import Application, Candidate, Project
from models.applications import (
    cancel_application,
    create_application,
    get_application_status,
    get_applications_statistics,
    is_role_available,
)
from models.candidates import add_candidate, find_candidate, find_candidate_by_id
from models.projects import (
    add_project,
    find_project,
    find_project_by_id,
    sort_projects_by_role_count,
)
from storage import (
    load_applications,
    load_candidates,
    load_projects,
    save_applications,
    save_candidates,
    save_projects,
)
from utils import input_int, input_nonempty_str

PROJECTS_FILE = "data/projects.json"
CANDIDATES_FILE = "data/candidates.json"
APPLICATIONS_FILE = "data/applications.json"


def show_projects(projects: List[Project]) -> None:
    """Вывести список проектов с их ролями.

    :param projects: список объектов Project
    """
    if not projects:
        print("Проектов пока нет")
        return

    for project in projects:
        print(f"[{project.id}] {project}")
        for role in project.roles:
            print(f"    роль {role}")


def show_candidates(candidates: List[Candidate]) -> None:
    """Вывести список кандидатов.

    :param candidates: список объектов Candidate
    """
    if not candidates:
        print("Кандидатов пока нет")
        return

    for candidate in candidates:
        print(f"[{candidate.id}] {candidate}")


def show_applications(applications: List[Application]) -> None:
    """Вывести список заявок с указанием проекта, роли и статуса.

    :param applications: список объектов Application
    """
    if not applications:
        print("Заявок пока нет")
        return

    for application in applications:
        print(f"[{application.id}] {application}")


def show_statistics(
    projects: List[Project], applications: List[Application]
) -> None:
    """Вывести статистику по проектам и заявкам.

    :param projects: список объектов Project
    :param applications: список объектов Application
    """
    total_roles = sum(len(project.roles) for project in projects)
    print(f"Проектов: {len(projects)}")
    print(f"Ролей всего: {total_roles}")

    statistics = get_applications_statistics(applications)
    for status, count in statistics.items():
        print(f"Заявок со статусом {status}: {count}")

    print("Проекты по убыванию числа ролей:")
    for project in sort_projects_by_role_count(projects):
        print(f"  {project.name}: {len(project.roles)} ролей")


def main() -> None:
    """Точка запуска приложения: загрузка данных, меню, сохранение данных."""
    projects = load_projects(PROJECTS_FILE)
    candidates = load_candidates(CANDIDATES_FILE)
    applications = load_applications(APPLICATIONS_FILE, projects, candidates)

    menu = """
=== Сервис проведения кастингов ===
1. Показать проекты
2. Найти проект по названию
3. Добавить проект
4. Добавить роль в проект
5. Показать кандидатов
6. Найти кандидата по имени
7. Добавить кандидата
8. Проверить доступность роли
9. Подать заявку на роль
10. Отменить заявку
11. Показать заявки
12. Показать статистику
0. Выход
Выберите действие: """

    while True:
        choice = input(menu).strip()

        if choice == "1":
            show_projects(projects)
        elif choice == "2":
            query = input_nonempty_str("Подстрока названия: ")
            for project in find_project(projects, query):
                print(f"[{project.id}] {project}")
        elif choice == "3":
            name = input_nonempty_str("Название проекта: ")
            project = add_project(projects, name)
            print(f"Проект создан, id={project.id}")
        elif choice == "4":
            project_id = input_int("Id проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print(f"Проект с id={project_id} не найден")
            else:
                role_name = input_nonempty_str("Название роли: ")
                role = project.add_role(role_name)
                print(f"Роль добавлена, id={role.id}")
        elif choice == "5":
            show_candidates(candidates)
        elif choice == "6":
            query = input_nonempty_str("Подстрока имени кандидата: ")
            for candidate in find_candidate(candidates, query):
                print(f"[{candidate.id}] {candidate}")
        elif choice == "7":
            name = input_nonempty_str("Имя кандидата: ")
            contact = input_nonempty_str("Контакт кандидата: ")
            candidate = add_candidate(candidates, name, contact)
            print(f"Кандидат добавлен, id={candidate.id}")
        elif choice == "8":
            project_id = input_int("Id проекта: ")
            role_id = input_int("Id роли: ")
            project = find_project_by_id(projects, project_id)
            role = project.find_role(role_id) if project else None
            if project is None or role is None:
                print("Проект или роль не найдены")
            else:
                available = is_role_available(applications, project, role)
                print(get_application_status(available))
        elif choice == "9":
            candidate_id = input_int("Id кандидата: ")
            project_id = input_int("Id проекта: ")
            role_id = input_int("Id роли: ")
            candidate = find_candidate_by_id(candidates, candidate_id)
            project = find_project_by_id(projects, project_id)
            role = project.find_role(role_id) if project else None
            if candidate is None or project is None or role is None:
                print("Кандидат, проект или роль не найдены")
            else:
                try:
                    application = create_application(
                        applications, candidate, project, role
                    )
                    print(f"Заявка создана, id={application.id}")
                except ValueError as error:
                    print(f"Ошибка: {error}")
        elif choice == "10":
            application_id = input_int("Id заявки: ")
            if cancel_application(applications, application_id):
                print("Заявка отменена")
            else:
                print("Заявка с таким id не найдена")
        elif choice == "11":
            show_applications(applications)
        elif choice == "12":
            show_statistics(projects, applications)
        elif choice == "0":
            save_projects(PROJECTS_FILE, projects)
            save_candidates(CANDIDATES_FILE, candidates)
            save_applications(APPLICATIONS_FILE, applications)
            print("Данные сохранены, выход из программы")
            break
        else:
            print("Неизвестный пункт меню, попробуйте снова")


if __name__ == "__main__":
    main()
