from django import template
from login.models import Userinfos

register = template.Library()

@register.filter(name='user_departament')
def user_departament(value):
    return Userinfos.objects.get(auth_id=value).departaments.name

@register.filter(name='user_area')
def user_area(value):
    return Userinfos.objects.get(auth_id=value).areas.name