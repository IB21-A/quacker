from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    profile_photo = models.URLField(blank=True)
    # likes
    # following
    
    def get_posts(self):
        return self.posts.all()
    
class Post():
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="posts", null=True)
    body = models.TextField(blank=False, null=False, max_length=280)
    


# class Like()
#   user
#   post
#   date

# # class Follow()
#   Follower
#   Followee
#   date


