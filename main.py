"""Точка входа приложения «Сервис проведения кастингов».

Разработка продолжает сценарий ПР1 (функции creating_casting,
add_role_on_casting, get_all_castings), переработанный в наборы функций,
распределённые по модулям projects.py, candidates.py, applications.py,
storage.py, utils.py.
"""

from applications import (
    cancel_application,
    create_application,
    get_application_status,
    get_applications_statistics,
    is_role_available,
)
from candidates import add_candidate, find_candidate
from projects import add_project, add_role, find_project, sort_projects_by_role_count
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


def show_projects(projects: dict[int, dict]) -> None:
    """Вывести список проектов с их ролями.

    :param projects: словарь проектов
    """
    if not projects:
        print("Проектов пока нет")
        return

    for project_id, data in projects.items():
        print(f"[{project_id}] {data['name']}")
        for role in data["roles"]:
            print(f"    роль [{role['id']}] {role['name']}")


def show_candidates(candidates: dict[int, dict]) -> None:
    """Вывести список кандидатов.

    :param candidates: словарь кандидатов
    """
    if not candidates:
        print("Кандидатов пока нет")
        return

    for candidate_id, data in candidates.items():
        print(f"[{candidate_id}] {data['name']} ({data['contact']})")


def show_applications(applications: list[dict]) -> None:
    """Вывести список заявок с указанием проекта, роли и статуса.

    :param applications: список заявок
    """
    if not applications:
        print("Заявок пока нет")
        return

    for application in applications:
        print(
            f"[{application['id']}] кандидат {application['candidate_id']} -> "
            f"проект {application['project_id']}, роль {application['role_id']}: "
            f"{application['status']}"
        )


def show_statistics(projects: dict[int, dict], applications: list[dict]) -> None:
    """Вывести статистику по проектам и заявкам.

    :param projects: словарь проектов
    :param applications: список заявок
    """
    total_roles = sum(len(data["roles"]) for data in projects.values())
    print(f"Проектов: {len(projects)}")
    print(f"Ролей всего: {total_roles}")

    statistics = get_applications_statistics(applications)
    for status, count in statistics.items():
        print(f"Заявок со статусом {status}: {count}")

    print("Проекты по убыванию числа ролей:")
    for project in sort_projects_by_role_count(projects):
        print(f"  {project['name']}: {len(project['roles'])} ролей")


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    projects = load_projects(PROJECTS_FILE)
    candidates = load_candidates(CANDIDATES_FILE)
    applications = load_applications(APPLICATIONS_FILE)

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
                print(f"[{project['id']}] {project['name']}")
        elif choice == "3":
            name = input_nonempty_str("Название проекта: ")
            project_id = add_project(projects, name)
            print(f"Проект создан, id={project_id}")
        elif choice == "4":
            project_id = input_int("Id проекта: ")
            role_name = input_nonempty_str("Название роли: ")
            try:
                role_id = add_role(projects, project_id, role_name)
                print(f"Роль добавлена, id={role_id}")
            except KeyError as error:
                print(f"Ошибка: {error}")
        elif choice == "5":
            show_candidates(candidates)
        elif choice == "6":
            query = input_nonempty_str("Подстрока имени кандидата: ")
            for candidate in find_candidate(candidates, query):
                print(f"[{candidate['id']}] {candidate['name']}")
        elif choice == "7":
            name = input_nonempty_str("Имя кандидата: ")
            contact = input_nonempty_str("Контакт кандидата: ")
            candidate_id = add_candidate(candidates, name, contact)
            print(f"Кандидат добавлен, id={candidate_id}")
        elif choice == "8":
            project_id = input_int("Id проекта: ")
            role_id = input_int("Id роли: ")
            available = is_role_available(applications, project_id, role_id)
            print(get_application_status(available))
        elif choice == "9":
            candidate_id = input_int("Id кандидата: ")
            project_id = input_int("Id проекта: ")
            role_id = input_int("Id роли: ")
            try:
                application = create_application(
                    applications, candidate_id, project_id, role_id
                )
                print(f"Заявка создана, id={application['id']}")
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
