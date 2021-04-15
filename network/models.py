from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    profile_photo = models.URLField(blank=True, null=True, default=None)
    # likes
    # following
    
    def get_posts(self):
        return self.posts.all()
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="posts", null=True)
    body = models.TextField(blank=False, null=False, max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True, db_column='date_posted')
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
    


# class Like()
#   user
#   post
#   date

# # class Follow()
#   Follower
#   Followee
#   date


