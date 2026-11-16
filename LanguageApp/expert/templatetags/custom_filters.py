from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    """Get value from dictionary by key"""
    return dictionary.get(int(key), 0)