"""Класс Application и функции для работы с коллекцией заявок.

Application связывает объекты Candidate, Project и Role: заявка хранит
ссылки на эти объекты, а не только их идентификаторы (аналогично тому,
как Booking в методичке хранит ссылки на Room и User).
"""

from typing import List, Optional

from .candidates import Candidate
from .projects import Project, Role

STATUS_PENDING = "pending"
STATUS_ACCEPTED = "accepted"
STATUS_CANCELLED = "cancelled"
VALID_STATUSES = {STATUS_PENDING, STATUS_ACCEPTED, STATUS_CANCELLED}


class Application:
    """Заявка кандидата на роль в проекте."""

    def __init__(
        self,
        application_id: int,
        candidate: Candidate,
        project: Project,
        role: Role,
        status: str = STATUS_PENDING,
    ) -> None:
        """Создать заявку, связав её с кандидатом, проектом и ролью."""
        self.id = application_id
        self.candidate = candidate
        self.project = project
        self.role = role
        self.status = status

    def accept(self) -> None:
        """Принять заявку (утвердить кандидата на роль)."""
        self.status = STATUS_ACCEPTED

    def cancel(self) -> None:
        """Отменить заявку, не удаляя её из коллекции."""
        self.status = STATUS_CANCELLED

    @staticmethod
    def is_valid_status(status: str) -> bool:
        """Проверить, является ли значение допустимым статусом заявки."""
        return status in VALID_STATUSES

    def __str__(self) -> str:
        """Вернуть строковое представление заявки с учётом её состояния."""
        return (
            f"{self.candidate.name} -> {self.project.name} / "
            f"{self.role.name}: {self.status}"
        )


def is_role_available(
    applications: List[Application], project: Project, role: Role
) -> bool:
    """Проверить, свободна ли роль (нет принятой заявки на неё)."""
    for application in applications:
        same_role = application.project is project and application.role is role
        if same_role and application.status == STATUS_ACCEPTED:
            return False
    return True


def get_application_status(is_available: bool) -> str:
    """Вернуть текстовый статус роли (функция унаследована из ПР1/ПР2)."""
    if is_available:
        return "Роль свободна, можно подавать заявку"
    return "Роль уже занята"


def create_application(
    applications: List[Application],
    candidate: Candidate,
    project: Project,
    role: Role,
) -> Application:
    """Создать заявку кандидата на роль и добавить её в коллекцию.

    :raises ValueError: если на роль уже есть принятая заявка
    """
    if not is_role_available(applications, project, role):
        raise ValueError("Роль уже занята, заявку создать нельзя")

    application_id = (
        max((application.id for application in applications), default=0) + 1
    )
    application = Application(application_id, candidate, project, role)
    applications.append(application)
    return application


def find_application_by_id(
    applications: List[Application], application_id: int
) -> Optional[Application]:
    """Найти заявку по идентификатору.

    Используется веб-страницей заявки (ПР5): идентификатор передаётся
    в URL, а представление получает соответствующий объект Application.
    """
    for application in applications:
        if application.id == application_id:
            return application
    return None


def cancel_application(applications: List[Application], application_id: int) -> bool:
    """Отменить заявку по идентификатору, вызвав её метод cancel()."""
    for application in applications:
        if application.id == application_id:
            application.cancel()
            return True
    return False


def get_applications_statistics(applications: List[Application]) -> dict:
    """Собрать статистику по заявкам: количество по каждому статусу."""
    statistics = {STATUS_PENDING: 0, STATUS_ACCEPTED: 0, STATUS_CANCELLED: 0}
    for application in applications:
        statistics[application.status] = statistics.get(application.status, 0) + 1
    return statistics
