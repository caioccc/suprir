from django import template

register = template.Library()


@register.filter
def get_user_name(user):
    try:
        return user.first_name
    except (Exception,):
        return ''
