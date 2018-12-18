"""
    Test de usuario para decoradores de permisos de acceso.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

def is_teacher(user):

    """
        Comprueba si es un Profesor
    """

    return user.groups.filter(
        name__in=['Teachers']
    )

def is_departaments(user):

    """
        Comprueba si es un Departamento
    """

    return user.groups.filter(
        name__in=['Departaments']
    )

def is_center(user):

    """
        Comprueba si es un Centro
    """

    return user.groups.filter(
        name__in=['Centers']
    )

def is_from_group(user):

    """
        Comprueba si es un Centro, Departamento o Profesor
    """

    return user.groups.filter(
        name__in=[
            'Teachers',
            'Departaments',
            'Centers'
        ]
    )
