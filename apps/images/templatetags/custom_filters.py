import json
from django import template

register = template.Library()

@register.filter
def split(value, separator=","):
    """
    Divide una cadena en una lista usando el separador especificado.
    Por defecto, el separador es un punto.
    """
    if value is None:
        return []  # Retornar una lista vacía si el valor es None
    return value.split(separator)

@register.filter
def trim(value):
    """
    Elimina espacios en blanco al principio y al final de una cadena.
    """
    if value is None:
        return ""  # Retornar una cadena vacía si el valor es None
    return value.strip()

@register.filter
def json_load(value):
    """
    Convierte una cadena JSON en un objeto de Python.
    """
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}