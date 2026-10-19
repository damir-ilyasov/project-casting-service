"""View-функции приложения applications: список заявок и страница заявки.

HTML больше не формируется в Python. Представления получают данные
(через storage.py и models/), готовят контекст и вызывают render() —
разметку формируют шаблоны applications/templates/applications/*.html.
"""

from django.shortcuts import render

from models.applications import find_application_by_id
from storage import load_applications, load_candidates, load_projects


def _load_applications_list():
    """Загрузить проекты, кандидатов и связанные с ними заявки."""
    projects_list = load_projects("data/projects.json")
    candidates_list = load_candidates("data/candidates.json")
    return load_applications(
        "data/applications.json",
        projects_list,
        candidates_list,
    )


def applications(request):
    """Страница /applications/: список заявок кандидатов на роли."""
    context = {
        "applications": _load_applications_list(),
    }

    return render(request, "applications/application_list.html", context)


def application_detail(request, application_id):
    """Страница /applications/<id>/: подробности одной заявки."""
    applications_list = _load_applications_list()
    application = find_application_by_id(applications_list, application_id)

    context = {
        "application": application,
    }

    return render(
        request,
        "applications/application_detail.html",
        context,
        status=404 if application is None else 200,
    )
