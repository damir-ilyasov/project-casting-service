"""Представления страниц заявок, использующие JOIN в SQLite."""

from django.shortcuts import render

from db.queries import get_application, get_applications


def applications(request):
    """Список заявок; при передаче status список фильтруется."""
    status = request.GET.get("status", "").strip()
    valid_statuses = {"pending", "accepted", "cancelled", ""}
    if status not in valid_statuses:
        status = ""
    context = {
        "applications": get_applications(status),
        "selected_status": status,
    }
    return render(request, "applications/application_list.html", context)


def application_detail(request, application_id):
    """Подробная информация о заявке по её идентификатору."""
    application = get_application(application_id)
    context = {"application": application}
    return render(
        request,
        "applications/application_detail.html",
        context,
        status=404 if application is None else 200,
    )
