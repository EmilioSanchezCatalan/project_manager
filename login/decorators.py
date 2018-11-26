def is_teacher(user):
    return user.groups.filter(
        name__in=['Teachers']
    )

def is_departaments(user):
    return user.groups.filter(
        name__in=['Departaments']
    )

def is_center(user):
    return user.groups.filter(
        name__in=['Centers']
    )

def is_from_group(user):
    return user.groups.filter(
        name__in=[
            'Teachers',
            'Departaments',
            'Centers'
        ]
    )
