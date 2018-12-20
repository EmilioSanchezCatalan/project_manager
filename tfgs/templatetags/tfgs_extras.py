"""
    Modulos para la conversión y adaptación de la información.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django import template
from tfgs.models import Tfgs

register = template.Library()

@register.filter(name='tfg_mode')
def tfg_mode(value):

    """
        Devuelve el texto correspondiente al valor obtenido de la
        modalidad.

        Parametros:
            value(int): identificador del valor de la modalidad

        Returns:
            String: devuelve el texto correspondiente a la modalidad
                    seleccionada.
    """

    if value == Tfgs.MODE_ING_PROYECT:
        return Tfgs.MODE_TEXT_ING_PROYECT
    if value == Tfgs.MODE_EXP_THEORETICAL:
        return Tfgs.MODE_TEXT_EXP_THEORETICAL
    if value == Tfgs.MODE_TECHNICAL_STUDY:
        return Tfgs.MODE_TEXT_TECHNICAL_STUDY
    return "Nan"

@register.filter(name="tfg_type")
def tfg_type(value):

    """
        Devuelve un texto correspondiente al valor obtenido del 
        tipo de TFG

        Parametro:
            value(int): identificador del valor de la modalidad

        Returns:
            String: devuelve el texto correspondiente a al
                    tipo de TFG.
    """

    if value == Tfgs.TYPE_GENERAL:
        return Tfgs.TYPE_TEXT_GENERAL
    if value == Tfgs.TYPE_ESPECIFIC:
        return Tfgs.TYPE_TEXT_ESPECIFIC
    return "Nan"
