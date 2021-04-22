from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    profile_photo = models.URLField(blank=True, null=True, default=None)
    # likes
    
    def is_following(self, followee):
        if self.following.filter(follower=self, followee=followee):
            return True
        
        return False
        
    
    def get_posts(self):
        return self.posts.all()
    
    def get_followers(self):
        return self.followers.all()
    
    def get_following(self):
        return self.following.all().values_list('followee', flat=True)
    
    def get_following_posts(self):
        following = self.get_following()
        return Post.objects.filter(author__in=following)
    
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
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} followed {self.followee.username} at {self.timestamp}"


# class Like()
#   user
#   post
#   date

