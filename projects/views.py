"""Представления страниц проектов, использующие SQL-запросы SQLite."""

from django.shortcuts import render

from db.queries import get_project, get_projects


def projects(request):
    """Список проектов; параметр q позволяет искать по названию."""
    search = request.GET.get("q", "").strip()
    context = {
        "projects": get_projects(search),
        "search": search,
    }
    return render(request, "projects/project_list.html", context)


def project_detail(request, project_id):
    """Страница проекта и статусы его ролей."""
    project = get_project(project_id)
    roles_with_status = [
        {"role": role, "available": role.available}
        for role in project.roles
    ] if project is not None else []

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
