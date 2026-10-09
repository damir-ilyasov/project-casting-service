"""View-функции главной страницы и общий HTML-каркас всех страниц проекта.

Функция page() размещена здесь, потому что главная страница задаёт общий
вид всех остальных страниц — она точка входа в проект. Приложения
projects и applications импортируют её.
"""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ: кодировка, заголовок, Bootstrap, навигация.

    :param title: заголовок вкладки браузера
    :param content: HTML-содержимое страницы (тело <main>)
    :return: полный HTML-документ страницы
    """
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="navbar navbar-expand bg-body-tertiary mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Casting Service</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/projects/">Проекты</a>
                <a class="nav-link" href="/applications/">Заявки</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание приложения и навигация."""
    content = """
    <h1 class="display-4">Casting Service</h1>
    <p class="lead">Сервис организации и проведения кастингов.</p>
    <p>Основные разделы:</p>
    <a href="/projects/" class="btn btn-primary me-2">Проекты</a>
    <a href="/applications/" class="btn btn-secondary">Заявки</a>
    """
    return HttpResponse(page("Casting Service", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404 вместо стандартной Django."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
