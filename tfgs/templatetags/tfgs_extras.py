from django import template

register = template.Library()

@register.filter(name='tfg_mode')
def tfg_mode(value):
    mode_texts = [
        "proyecto de ingeniería",
        "estudio técnico",
        "trabajo teórico experimental"
    ]
    return mode_texts[value]

@register.filter(name="tfg_type")
def tfg_type(value):
    type_texts = [
        "general",
        "específico"
    ]
    return type_texts[value]