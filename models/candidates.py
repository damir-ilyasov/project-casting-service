"""Класс Candidate и функции для работы с коллекцией кандидатов."""

from typing import List, Optional


class Candidate:
    """Кандидат, претендующий на роль в одном или нескольких проектах."""

    def __init__(self, candidate_id: int, name: str, contact: str) -> None:
        """Создать объект кандидата."""
        self.id = candidate_id
        self.name = name
        self.contact = contact

    @classmethod
    def from_data(cls, data: dict) -> "Candidate":
        """Создать кандидата из словаря данных (например, из JSON)."""
        return cls(data["id"], data["name"], data["contact"])

    def __str__(self) -> str:
        """Вернуть строковое представление кандидата."""
        return f"{self.name} ({self.contact})"


def add_candidate(
    candidates: List[Candidate], name: str, contact: str
) -> Candidate:
    """Создать кандидата, добавить его в коллекцию и вернуть созданный объект."""
    candidate_id = max((candidate.id for candidate in candidates), default=0) + 1
    candidate = Candidate(candidate_id, name, contact)
    candidates.append(candidate)
    return candidate


def find_candidate_by_id(
    candidates: List[Candidate], candidate_id: int
) -> Optional[Candidate]:
    """Найти кандидата по идентификатору."""
    for candidate in candidates:
        if candidate.id == candidate_id:
            return candidate
    return None


def find_candidate(candidates: List[Candidate], query: str) -> List[Candidate]:
    """Найти кандидатов, в имени которых встречается подстрока query."""
    query = query.lower()
    return [
        candidate for candidate in candidates if query in candidate.name.lower()
    ]
