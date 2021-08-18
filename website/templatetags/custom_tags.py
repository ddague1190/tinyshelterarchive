from django import template

register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)

@register.simple_tag
def most_recent_ancestor(node):
    parents = node.get_ancestors()
    return list(parents)[-1]


@register.filter
def get_images(queryset, pk):
    return queryset.filter(parent__vehicle=int(pk))

@register.filter
def first_five(queryset):
    return queryset[:5]