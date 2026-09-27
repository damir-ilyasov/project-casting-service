import pytest

from models import Candidate, Project
from models.applications import cancel_application, create_application, is_role_available


def _make_project_and_role():
    project = Project(1, "Сериал")
    role = project.add_role("Главный герой")
    return project, role


def test_is_role_available_when_empty():
    applications = []
    project, role = _make_project_and_role()
    assert is_role_available(applications, project, role)


def test_create_application_and_accept_fills_role():
    applications = []
    project, role = _make_project_and_role()
    candidate = Candidate(1, "Иван Иванов", "ivan@example.com")

    application = create_application(applications, candidate, project, role)
    application.accept()

    assert not is_role_available(applications, project, role)


def test_duplicate_accepted_application_forbidden():
    applications = []
    project, role = _make_project_and_role()
    candidate_1 = Candidate(1, "Иван Иванов", "ivan@example.com")
    candidate_2 = Candidate(2, "Пётр Петров", "petr@example.com")

    application = create_application(applications, candidate_1, project, role)
    application.accept()

    with pytest.raises(ValueError):
        create_application(applications, candidate_2, project, role)


def test_cancel_application():
    applications = []
    project, role = _make_project_and_role()
    candidate = Candidate(1, "Иван Иванов", "ivan@example.com")
    application = create_application(applications, candidate, project, role)

    assert cancel_application(applications, application.id)
    assert application.status == "cancelled"


def test_cancel_unknown_application():
    applications = []
    assert not cancel_application(applications, 999)
