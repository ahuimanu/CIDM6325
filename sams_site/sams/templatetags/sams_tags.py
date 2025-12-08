from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """Return True if the user is in the given group name."""
    if user is None:
        return False
    return user.groups.filter(name=group_name).exists()
