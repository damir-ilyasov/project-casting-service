"""Функции для работы с кандидатами.

Кандидаты хранятся в словаре candidates: ключ — id кандидата (int),
значение — словарь {"name": str, "contact": str}.
"""


def add_candidate(candidates: dict[int, dict], name: str, contact: str) -> int:
    """Добавить кандидата в словарь candidates.

    :param candidates: словарь кандидатов
    :param name: имя кандидата
    :param contact: контактные данные (телефон, email и т.п.)
    :return: идентификатор созданного кандидата
    """
    candidate_id = max(candidates.keys(), default=0) + 1
    candidates[candidate_id] = {"name": name, "contact": contact}
    return candidate_id


def find_candidate(candidates: dict[int, dict], query: str) -> list[dict]:
    """Найти кандидатов, в имени которых встречается подстрока query.

    :param candidates: словарь кандидатов
    :param query: искомая подстрока имени
    :return: список найденных кандидатов вида {"id": int, "name": str}
    """
    query = query.lower()
    return [
        {"id": candidate_id, "name": data["name"]}
        for candidate_id, data in candidates.items()
        if query in data["name"].lower()
    ]
