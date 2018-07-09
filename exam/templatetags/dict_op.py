from django import template

register = template.Library()


@register.filter(name='key')
def key(value, key_name):
    return value[key_name]
