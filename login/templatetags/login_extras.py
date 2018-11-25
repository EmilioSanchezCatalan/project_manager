from django import template
from django.contrib.auth.models import Group 
from login.models import Userinfos

register = template.Library()

@register.filter(name='user_departament')
def user_departament(value):
    return Userinfos.objects.get(auth_id=value).departaments.name

@register.filter(name='user_area')
def user_area(value):
    return Userinfos.objects.get(auth_id=value).areas.name

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 