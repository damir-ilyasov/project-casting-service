"""View-функции приложения projects: список проектов и страница проекта.

HTML больше не формируется в Python. Представления получают данные
(через storage.py и models/), готовят контекст и вызывают render() —
разметку формируют шаблоны rooms/templates/projects/*.html.
"""

from django.shortcuts import render

from models.applications import is_role_available
from models.projects import find_project_by_id
from storage import load_applications, load_candidates, load_projects


def projects(request):
    """Страница /projects/: список проектов с их ролями."""
    projects_list = load_projects("data/projects.json")

    context = {
        "projects": projects_list,
    }

    return render(request, "projects/project_list.html", context)


def project_detail(request, project_id):
    """Страница /projects/<id>/: информация о проекте и статус ролей."""
    projects_list = load_projects("data/projects.json")
    project = find_project_by_id(projects_list, project_id)

    roles_with_status = []
    if project is not None:
        candidates_list = load_candidates("data/candidates.json")
        applications_list = load_applications(
            "data/applications.json",
            projects_list,
            candidates_list,
        )
        for role in project.roles:
            available = is_role_available(applications_list, project, role)
            roles_with_status.append({"role": role, "available": available})

    context = {
        "project": project,
        "roles_with_status": roles_with_status,
    }

    return render(
        request,
        "projects/project_detail.html",
        context,
        status=404 if project is None else 200,
    )
