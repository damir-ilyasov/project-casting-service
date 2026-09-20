from projects import add_project, add_role, find_project, get_role


def test_add_project():
    projects = {}
    add_project(projects, "Сериал")
    assert len(projects) == 1


def test_add_role():
    projects = {}
    project_id = add_project(projects, "Сериал")
    role_id = add_role(projects, project_id, "Главный герой")
    assert get_role(projects, project_id, role_id) is not None


def test_find_project():
    projects = {}
    add_project(projects, "Сериал")
    assert find_project(projects, "сериал")


def test_find_project_no_match():
    projects = {}
    add_project(projects, "Сериал")
    assert find_project(projects, "фильм") == []
