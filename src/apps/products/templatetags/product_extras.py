from django import template
from apps.products.models import Category

register = template.Library()


@register.filter
def get_item_by_slug(categories, slug):
    return categories.filter(slug=slug).first()
