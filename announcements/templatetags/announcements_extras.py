"""
    Modulos para la conversión y adaptación de la información.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django import template
from announcements.models import AnnouncementsTfg, AnnouncementsTfm

register = template.Library()

@register.filter(name='announ_tfg_status')
def announ_tfg_status(value):
    """
        Devuelve el texto correspondiente al estado de la
        convocatoria de TFG

        Parametros:
            value(int): indentificador del estado de la convocatoria.

        Returns:
            str: devuelve el texto del estado de la convocatoria.

    """

    if value == AnnouncementsTfg.STATUS_OPEN:
        return AnnouncementsTfg.STATUS_TEXT_OPEN
    if value == AnnouncementsTfg.STATUS_PUBLIC:
        return AnnouncementsTfg.STATUS_TEXT_PUBLIC
    if value == AnnouncementsTfg.STATUS_CLOSE:
        return AnnouncementsTfg.STATUS_TEXT_CLOSE
    return "Nan"

@register.filter(name='announ_tfm_status')
def announ_tfm_status(value):

    """
        Devuelve el texto correspondiente al estado de la
        convocatoria de TFM

        Parametros:
            value(int): indentificador del estado de la convocatoria.

        Returns:
            str: devuelve el texto del estado de la convocatoria.

    """

    if value == AnnouncementsTfm.STATUS_OPEN:
        return AnnouncementsTfm.STATUS_TEXT_OPEN
    if value == AnnouncementsTfm.STATUS_PUBLIC:
        return AnnouncementsTfm.STATUS_TEXT_PUBLIC
    if value == AnnouncementsTfm.STATUS_CLOSE:
        return AnnouncementsTfm.STATUS_TEXT_CLOSE
    return "Nan"
