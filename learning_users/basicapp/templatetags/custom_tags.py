from django import template

register = template.Library()

@register.filter(name='mycut')
def mycut(value,arg):
    """
    This custs out all values of "arg" from the string
    """
    return value.replace(arg,'')
