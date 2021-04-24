from django.contrib import admin
from .models import User, Post, Follow, Like


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "body", "timestamp")
    
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "followee")
    
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)