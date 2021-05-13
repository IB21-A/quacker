from django import template
from ..models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from datetime import datetime, timezone, timedelta

register = template.Library()

# Will return true if the currently logged in user likes the 
# post being displayed by django template
# Usage: post|is_liked_by_user:user
@register.filter(name='is_liked_by_user')
def is_liked_by_user(post, user):
    return user.likes_post(post)


@register.filter(name='post_timestamp')
def post_timestamp(timestamp):
    return timestamp.strftime('%x %I:%M %p') 


# Returns true if user is following a supplied username
@register.filter(name='is_following_user')
def is_following(user, username):
    try:
        username = User.objects.get(username=username)
        is_following = user.is_following(username)
    except User.DoesNotExist:
        return False
    except AttributeError: 
        return False
        
    return is_following
        
    