from django import template

register = template.Library()


@register.filter
def is_list(value):
    """Check if a value is a list or a tuple."""
    return isinstance(value, (list, tuple))
