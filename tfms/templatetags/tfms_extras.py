"""
    Modulos para la conversión y adaptación de la información.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django import template
from tfms.models import Tfms

register = template.Library()

@register.filter(name="tfm_type")
def tfm_type(value):

    """
        Devuelve el texto correspondiente al valor obtenido del
        tipo de TFM.

        Parametros:
            value(int): identificador del valor del tipo de TFM

        Returns:
            String: devuelve el texto correspondiente al tipo de TFM
                    seleccionada.
    """

    if value == Tfms.TYPE_UNI:
        return Tfms.TYPE_TEXT_UNI
    if value == Tfms.TYPE_BUSINESS:
        return Tfms.TYPE_TEXT_BUSINESS
    return "Nan"
