"""View-функции приложения projects: список проектов и страница проекта."""

from django.http import HttpResponse

from homepage.views import page
from models.applications import is_role_available
from models.projects import find_project_by_id
from storage import load_applications, load_candidates, load_projects


def projects(request):
    """Страница /projects/: список проектов с их ролями."""
    items = ""
    for project in load_projects("data/projects.json"):
        roles = "".join(
            f'<li class="list-group-item">{role}</li>'
            for role in project.roles
        )
        items += f"""
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">
                    <a href="/projects/{project.id}/">{project.name}</a>
                </h5>
                <p class="card-text text-muted">
                    {len(project.roles)} ролей
                </p>
                <ul class="list-group list-group-flush">{roles}</ul>
            </div>
        </div>
        """
    content = f"""
    <h1>Проекты</h1>
    {items if items else "<p>Проектов пока нет.</p>"}
    """
    return HttpResponse(page("Casting Service — проекты", content))


def project_detail(request, project_id):
    """Страница /projects/<id>/: информация о проекте и статус ролей."""
    projects_list = load_projects("data/projects.json")
    project = find_project_by_id(projects_list, project_id)
    if project is None:
        content = """
        <h1 class="text-danger">Проект не найден</h1>
        <a href="/projects/" class="btn btn-outline-secondary">
            ← к списку проектов
        </a>
        """
        return HttpResponse(
            page("Проект не найден", content),
            status=404,
        )

    candidates_list = load_candidates("data/candidates.json")
    applications_list = load_applications(
        "data/applications.json",
        projects_list,
        candidates_list,
    )

    roles_items = ""
    for role in project.roles:
        available = is_role_available(applications_list, project, role)
        status = "свободна" if available else "занята"
        badge = "bg-success" if available else "bg-danger"
        roles_items += f"""
        <li class="list-group-item d-flex justify-content-between
                    align-items-center">
            {role.name}
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{project.name}</h5>
            <p class="card-text"><strong>ID:</strong> {project.id}</p>
            <p class="card-text"><strong>Роли:</strong></p>
            <ul class="list-group mb-3">{roles_items}</ul>
            <a href="/projects/" class="btn btn-outline-secondary">
                ← к списку проектов
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(project.name, content),
        status=200,
    )
