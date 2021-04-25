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


# Will display either sec/min/hours sine post
# or the date of the post if more than 24hrs
@register.filter(name='time_since_or_date')
def time_since_or_date(timestamp):
    SECONDS_IN_DAY = 86400
    delta_in_seconds = abs((timestamp - datetime.now(timezone.utc)).total_seconds())
    if delta_in_seconds < SECONDS_IN_DAY:
        return naturaltime(timestamp)
    
    return timestamp.strftime('%b %d')