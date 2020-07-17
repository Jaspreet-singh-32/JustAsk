from django import template

register = template.Library()


@register.filter(name='Qmark')
def Qmark(val):
    return val.replace('?', '003qmark')
