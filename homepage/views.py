"""View-функции главной страницы и обработчик ошибки 404.

В ПР6 HTML больше не формируется в Python: каждое представление
подготавливает контекст и вызывает render() с именем шаблона.
"""

from django.shortcuts import render


def index(request):
    """Главная страница: описание сервиса и навигация к разделам."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Собственная страница ошибки 404 вместо технической страницы Django."""
    return render(request, "homepage/404.html", status=404)
