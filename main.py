ProjectCastings = []

def creating_casting (name):
    casting = [name, []]
    ProjectCastings.append(casting)
    
def add_role_on_casting(casting_name, role):
    for casting in ProjectCastings:
        if casting[0] == casting_name:
            casting[1].append(role)
    
def get_all_castings():
    print(ProjectCastings)
    

creating_casting("Сериал")
add_role_on_casting("Сериал", "Главный герой")
add_role_on_casting("Сериал", "Второстепенный персонаж")

creating_casting("Реклама")
add_role_on_casting("Реклама", "Главный персонаж 1 (Ваня Дмитриенко)")
add_role_on_casting("Реклама", "Главный персонаж 2 (Нагиев)")

get_all_castings()