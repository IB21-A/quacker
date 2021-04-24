from django import template
from ..models import User

register = template.Library()

# Will return true if the currently logged in user likes the 
# post being displayed by django template
# Usage: post|is_liked_by_user:user
@register.filter(name='is_liked_by_user')
def is_liked_by_user(post, user):
    return user.likes_post(post)