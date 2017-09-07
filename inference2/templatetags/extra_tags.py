from django.template import Library
register = Library()

@register.filter
def range(value):
    return xrange(value)
