
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following-posts/", views.following_posts_view, name="following"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("posts", views.publish, name="publish"),
    path("posts/like/<int:post_id>", views.like_post, name="like"),
    path("posts/<str:type>", views.posts, name="posts"),
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("follow/<str:username>", views.set_follow, name="follows"),
    path("<str:username>/get-follow-counts", views.get_follow_counts, name="follow_counts")
    
]
