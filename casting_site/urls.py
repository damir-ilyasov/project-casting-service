"""Корневая маршрутизация Django-проекта casting_site.

Файл подключает маршруты каждого приложения функцией include():
конкретные адреса описаны в urls.py соответствующего приложения.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("projects/", include("projects.urls")),
    path("applications/", include("applications.urls")),
]

handler404 = "homepage.views.page_not_found"
