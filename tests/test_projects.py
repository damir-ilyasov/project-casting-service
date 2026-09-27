from models import Project
from models.projects import (
    add_project,
    filter_projects_with_open_roles,
    find_project,
    find_project_by_id,
    sort_projects_by_role_count,
)


def test_project_creation():
    project = Project(1, "Сериал")
    assert project.id == 1
    assert project.name == "Сериал"
    assert project.roles == []


def test_add_role():
    project = Project(1, "Сериал")
    role = project.add_role("Главный герой")
    assert role.id == 1
    assert project.find_role(role.id) is role


def test_add_project():
    projects = []
    project = add_project(projects, "Сериал")
    assert len(projects) == 1
    assert project.name == "Сериал"


def test_find_project_by_id():
    projects = []
    project = add_project(projects, "Сериал")
    assert find_project_by_id(projects, project.id) is project


def test_find_project():
    projects = []
    add_project(projects, "Сериал")
    assert find_project(projects, "сериал")
    assert find_project(projects, "фильм") == []


def test_filter_and_sort_projects():
    projects = []
    project_1 = add_project(projects, "Сериал")
    project_1.add_role("Главный герой")
    add_project(projects, "Реклама")

    assert filter_projects_with_open_roles(projects) == [project_1]
    assert sort_projects_by_role_count(projects)[0] is project_1
