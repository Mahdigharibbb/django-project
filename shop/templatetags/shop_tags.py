from django import template
from ..models import Product, Comment

register = template.Library()


@register.simple_tag()
def total_comment(product):
    return Comment.objects.filter(active=True, product=product).count()


@register.simple_tag(takes_context=True)
def update_query(context, **kwargs):
    request = context['request']
    query = request.GET.copy()

    for key, value in kwargs.items():
        query[key] = value

    keys_to_remove = [key for key, val in kwargs.items() if val is None]
    for key in keys_to_remove:
        query.pop(key, None)

    return '?' + query.urlencode()
