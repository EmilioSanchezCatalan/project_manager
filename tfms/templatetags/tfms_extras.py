from django import template

register = template.Library()

@register.filter(name='tfm_mode')
def tfg_mode(value):
    mode_texts = [
        "investigador",
        "profesionalizante"
    ]
    return mode_texts[value]

@register.filter(name="tfm_type")
def tfg_type(value):
    type_texts = [
        "universidad",
        "empresa"
    ]
    return type_texts[value]