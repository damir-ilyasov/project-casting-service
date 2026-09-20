import pytest

from applications import (
    cancel_application,
    create_application,
    is_role_available,
)


def test_is_role_available_when_empty():
    applications = []
    assert is_role_available(applications, 1, 1)


def test_create_application_fills_role():
    applications = []
    application = create_application(applications, 1, 1, 1)
    application["status"] = "accepted"
    assert not is_role_available(applications, 1, 1)


def test_duplicate_application_forbidden():
    applications = []
    application = create_application(applications, 1, 1, 1)
    application["status"] = "accepted"
    with pytest.raises(ValueError):
        create_application(applications, 2, 1, 1)


def test_cancel_application():
    applications = []
    create_application(applications, 1, 1, 1)
    assert cancel_application(applications, 1)
    assert applications[0]["status"] == "cancelled"


def test_cancel_unknown_application():
    applications = []
    assert not cancel_application(applications, 999)
