"""View-функции приложения applications: список заявок и страница заявки."""

from django.http import HttpResponse

from homepage.views import page
from models.applications import find_application_by_id
from storage import load_applications, load_candidates, load_projects

STATUS_LABELS = {
    "pending": "на рассмотрении",
    "accepted": "принята",
    "cancelled": "отменена",
}
STATUS_BADGES = {
    "pending": "bg-warning text-dark",
    "accepted": "bg-success",
    "cancelled": "bg-secondary",
}


def _load_applications():
    """Загрузить проекты, кандидатов и связанные с ними заявки."""
    projects_list = load_projects("data/projects.json")
    candidates_list = load_candidates("data/candidates.json")
    applications_list = load_applications(
        "data/applications.json",
        projects_list,
        candidates_list,
    )
    return applications_list


def applications(request):
    """Страница /applications/: список заявок кандидатов на роли."""
    items = ""
    for application in _load_applications():
        status = STATUS_LABELS.get(application.status, application.status)
        badge = STATUS_BADGES.get(application.status, "bg-secondary")
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                    align-items-center">
            <a href="/applications/{application.id}/">
                {application.candidate.name} → {application.project.name}
                / {application.role.name}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Заявки</h1>
    <ul class="list-group">
        {items if items else '<li class="list-group-item">Заявок пока нет.</li>'}
    </ul>
    """
    return HttpResponse(page("Casting Service — заявки", content))


def application_detail(request, application_id):
    """Страница /applications/<id>/: подробности одной заявки."""
    applications_list = _load_applications()
    application = find_application_by_id(applications_list, application_id)
    if application is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <a href="/applications/" class="btn btn-outline-secondary">
            ← к списку заявок
        </a>
        """
        return HttpResponse(
            page("Заявка не найдена", content),
            status=404,
        )

    status = STATUS_LABELS.get(application.status, application.status)
    badge = STATUS_BADGES.get(application.status, "bg-secondary")
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заявка №{application.id}</h5>
            <p class="card-text">
                Кандидат: {application.candidate.name}
                ({application.candidate.contact})
            </p>
            <p class="card-text">
                Проект: {application.project.name}
            </p>
            <p class="card-text">
                Роль: {application.role.name}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/applications/" class="btn btn-outline-secondary">
                ← к списку заявок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Заявка №{application.id}", content),
        status=200,
    )
