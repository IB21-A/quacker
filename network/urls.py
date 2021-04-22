
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("posts", views.publish, name="publish"),
    path("posts/<str:type>", views.posts, name="posts"),
    path("follow/<str:username>", views.set_follow, name="follows")
]
