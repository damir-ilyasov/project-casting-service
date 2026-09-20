"""Функции сохранения и загрузки данных проекта в JSON-файлах."""

import json


def load_projects(filename: str) -> dict[int, dict]:
    """Загрузить проекты из JSON-файла.

    Файл хранит список проектов; функция преобразует его в словарь,
    ключом которого является идентификатор проекта.

    :param filename: путь к JSON-файлу с проектами
    :return: словарь проектов; пустой словарь, если файл отсутствует
        или повреждён
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_projects = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый список проектов")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные проектов не загружены")
        return {}

    return {
        project["id"]: {"name": project["name"], "roles": project["roles"]}
        for project in raw_projects
    }


def save_projects(filename: str, projects: dict[int, dict]) -> None:
    """Сохранить проекты в JSON-файл.

    :param filename: путь к JSON-файлу с проектами
    :param projects: словарь проектов
    """
    raw_projects = [
        {"id": project_id, "name": data["name"], "roles": data["roles"]}
        for project_id, data in projects.items()
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_projects, file, ensure_ascii=False, indent=2)


def load_candidates(filename: str) -> dict[int, dict]:
    """Загрузить кандидатов из JSON-файла.

    :param filename: путь к JSON-файлу с кандидатами
    :return: словарь кандидатов; пустой словарь, если файл отсутствует
        или повреждён
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_candidates = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый список кандидатов")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные кандидатов не загружены")
        return {}

    return {
        candidate["id"]: {"name": candidate["name"], "contact": candidate["contact"]}
        for candidate in raw_candidates
    }


def save_candidates(filename: str, candidates: dict[int, dict]) -> None:
    """Сохранить кандидатов в JSON-файл.

    :param filename: путь к JSON-файлу с кандидатами
    :param candidates: словарь кандидатов
    """
    raw_candidates = [
        {"id": candidate_id, "name": data["name"], "contact": data["contact"]}
        for candidate_id, data in candidates.items()
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_candidates, file, ensure_ascii=False, indent=2)


def load_applications(filename: str) -> list[dict]:
    """Загрузить заявки из JSON-файла.

    :param filename: путь к JSON-файлу с заявками
    :return: список заявок; пустой список, если файл отсутствует
        или повреждён
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый список заявок")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные заявок не загружены")
        return []


def save_applications(filename: str, applications: list[dict]) -> None:
    """Сохранить заявки в JSON-файл.

    :param filename: путь к JSON-файлу с заявками
    :param applications: список заявок
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(applications, file, ensure_ascii=False, indent=2)
