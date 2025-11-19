from django import template

register = template.Library()


@register.filter
def get_item_by_slug(categories, slug):
    return categories.filter(slug=slug).first()
