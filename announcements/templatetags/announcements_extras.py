from django import template
from announcements.models import AnnouncementsTfg, AnnouncementsTfm

register = template.Library()

@register.filter(name='announ_tfg_status')
def user_departament(value):
    if value == AnnouncementsTfg.STATUS_OPEN:
        return AnnouncementsTfg.STATUS_TEXT_OPEN
    elif value == AnnouncementsTfg.STATUS_PUBLIC:
        return AnnouncementsTfg.STATUS_TEXT_PUBLIC
    elif value == AnnouncementsTfg.STATUS_CLOSE:
        return AnnouncementsTfg.STATUS_TEXT_CLOSE
    else:
        return "Nan"

@register.filter(name='announ_tfm_status')
def user_departament(value):
    if value == AnnouncementsTfm.STATUS_OPEN:
        return AnnouncementsTfm.STATUS_TEXT_OPEN
    elif value == AnnouncementsTfm.STATUS_PUBLIC:
        return AnnouncementsTfm.STATUS_TEXT_PUBLIC
    elif value == AnnouncementsTfm.STATUS_CLOSE:
        return AnnouncementsTfm.STATUS_TEXT_CLOSE
    else:
        return "Nan"