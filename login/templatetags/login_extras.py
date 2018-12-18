"""
    Modulos para la conversión y adaptación de la información.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django import template
from django.contrib.auth.models import Group
from login.models import Userinfos

register = template.Library()

@register.filter(name='user_departament')
def user_departament(value):

    """
        Devuelve el nombre del departamento del usuario

        Parametros:
            value(int): id del usuario

        Returns:
            String: Nombre del departamento.

    """

    return Userinfos.objects.get(auth_id=value).departaments.name

@register.filter(name='user_area')
def user_area(value):

    """
        Devuelve el nombre del area del usuario

        Parametros:
            value(int): id del usuario

        Returns:
            String: Nombre del departamento.

    """

    return Userinfos.objects.get(auth_id=value).areas.name

@register.filter(name='has_group')
def has_group(user, group_name):

    """
        Comprueba si el usuario pertenece al grupo de usuarios

        Parametros:
            value(int): id del usuario
            group_name(str): nombre del grupo

        Returns:
            Boolean: devuelve si el usuario pertenece al grupo designado

    """

    group = Group.objects.get(name=group_name) 
    return group in user.groups.all()
