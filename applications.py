"""Функции для работы с заявками кандидатов на роли.

Заявки хранятся в списке applications; каждая заявка — словарь:
{"id": int, "candidate_id": int, "project_id": int, "role_id": int,
 "status": str}. Статус принимает значения "pending" (на рассмотрении),
"accepted" (принята) и "cancelled" (отменена).
"""

STATUS_PENDING = "pending"
STATUS_ACCEPTED = "accepted"
STATUS_CANCELLED = "cancelled"


def is_role_available(applications: list[dict], project_id: int, role_id: int) -> bool:
    """Проверить, свободна ли роль (нет принятой на неё заявки).

    :param applications: список заявок
    :param project_id: идентификатор проекта
    :param role_id: идентификатор роли
    :return: True, если на роль ещё нет принятой заявки
    """
    for application in applications:
        same_role = (
            application["project_id"] == project_id
            and application["role_id"] == role_id
        )
        if same_role and application["status"] == STATUS_ACCEPTED:
            return False
    return True


def get_application_status(is_available: bool) -> str:
    """Вернуть текстовый статус роли (функция перенесена из ПР1).

    :param is_available: результат проверки доступности роли
    :return: сообщение о доступности роли
    """
    if is_available:
        return "Роль свободна, можно подавать заявку"
    return "Роль уже занята"


def create_application(
    applications: list[dict],
    candidate_id: int,
    project_id: int,
    role_id: int,
) -> dict:
    """Создать новую заявку кандидата на роль.

    :param applications: список заявок
    :param candidate_id: идентификатор кандидата
    :param project_id: идентификатор проекта
    :param role_id: идентификатор роли
    :return: созданная заявка
    :raises ValueError: если роль на этот проект уже занята
    """
    if not is_role_available(applications, project_id, role_id):
        raise ValueError("Роль уже занята, заявку создать нельзя")

    application_id = max(
        (application["id"] for application in applications), default=0
    ) + 1
    application = {
        "id": application_id,
        "candidate_id": candidate_id,
        "project_id": project_id,
        "role_id": role_id,
        "status": STATUS_PENDING,
    }
    applications.append(application)
    return application


def cancel_application(applications: list[dict], application_id: int) -> bool:
    """Отменить заявку по идентификатору.

    :param applications: список заявок
    :param application_id: идентификатор заявки
    :return: True, если заявка найдена и отменена, иначе False
    """
    for application in applications:
        if application["id"] == application_id:
            application["status"] = STATUS_CANCELLED
            return True
    return False


def get_applications_statistics(applications: list[dict]) -> dict:
    """Собрать статистику по заявкам: количество по каждому статусу.

    :param applications: список заявок
    :return: словарь {статус: количество заявок}
    """
    statistics = {STATUS_PENDING: 0, STATUS_ACCEPTED: 0, STATUS_CANCELLED: 0}
    for application in applications:
        status = application["status"]
        statistics[status] = statistics.get(status, 0) + 1
    return statistics
