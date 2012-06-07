from django import template

register = template.Library()

@register.filter(is_safe=True)
def mult(value, arg):
	return value * arg

@register.filter(is_safe=True)
def sub(value, arg):
    return value - arg