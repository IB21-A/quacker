import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like
from .forms import NewPostForm

def index(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.pk)
        initial_data = Post(author=user)
        post_form = NewPostForm(request.POST, instance=initial_data)
        if post_form.is_valid():
            new_post = post_form.save()
            return HttpResponseRedirect(reverse("index"))
    
    # quack(request)  # Used to populate the feed with quacks
    post_form = NewPostForm
    
    posts = Post.objects.all()
    # organize posts in chronological order
    posts = posts.order_by("-timestamp").all()
    
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
        "post_form": post_form,
        "data_title": "index"
    })
    

# TODO there HAS to be a better way to do this, I'm just too tired to think of it right now.
# For now, getting a minimum viable product going here, displaying posts from following
def following_posts_view(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.pk)
        initial_data = Post(author=user)
        post_form = NewPostForm(request.POST, instance=initial_data)
        if post_form.is_valid():
            new_post = post_form.save()
            return HttpResponseRedirect(reverse("index"))
    
    # quack(request)  # Used to populate the feed with quacks
    post_form = NewPostForm
    
    user = User.objects.get(pk=request.user.pk)
    posts = user.get_following_posts()
    
    # organize posts in chronological order
    posts = posts.order_by("-timestamp").all()
    
    paginator = Paginator(posts, 5) # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
        "post_form": post_form,
        "data_title": "index"
    })
    

# Make posts from back end
def quack(request):
    user = User.objects.get(pk=2)
    new_post = Post(author=user, body="QUACK!")
    new_post.save()
    
    
@login_required
def profile_view(request, username):
    user = User.objects.get(id=request.user.pk)
    try:
        profile = get_user_by_username(username)
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    
    posts = Post.objects.filter(author=profile).order_by("-timestamp").all()
    
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html",{
        "profile": profile,
        "followers": profile.get_followers(),
        "following": profile.get_following(),
        "is_following": user.is_following(profile),
        "posts": posts,
        "page_obj": page_obj,
        "data_title": "profile"
    })
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
    
def get_posts(request, type):

    if type == "all":
        posts = Post.objects.all()
       
    if type == "following":
        user = User.objects.get(pk=request.user.pk)
        posts = user.get_following_posts()
    
    
    # organize posts in chronological order
    posts = posts.order_by("-timestamp").all()
    return posts
    
    
    


## API Views:

# Creates or deletes a follow
@csrf_exempt
@login_required
def set_follow(request, username):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    try:
        followee = get_user_by_username(username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    user = User.objects.get(id=request.user.pk)
    if user.is_following(followee):
        try:
            follow = Follow.objects.get(followee=followee, follower=user).delete()
            user.decrease_following_count()
            followee.decrease_follower_count()
        except Follow.DoesNotExist:
            return JsonResponse({"error": "No such follow exists"}, status=404)
            
        return JsonResponse({"message": "Unfollowed successfully", "following": False}, status=201)
        
    follow = Follow.objects.create(followee=followee, follower=user)
    user.increase_following_count()
    followee.increase_follower_count()
    
    return JsonResponse({"message": "Followed successfully", "following": True}, status=201)

@csrf_exempt
def get_follow_counts(request, username):
    profile = get_user_by_username(username)
    followers = profile.follower_count
    following = profile.following_count
    return JsonResponse({"followers": followers, "following": following}, status=201)
    
    
@csrf_exempt
@login_required
def like_post(request, post_id):
    
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    user = User.objects.get(id=request.user.pk)
    # TODO add try/catch to post exists
    post = Post.objects.get(id=post_id)
    
    if user.likes_post(post):
        try:
            like = Like.objects.get(user=user, post=post).delete()
            post.decrease_like_count()
        except Like.DoesNotExist:
                return JsonResponse({"error": "No such like exists"}, status=404)
        return JsonResponse({"message": "Unliked post successfully", "liked": False, "likes": post.like_count}, status=201)
        
    like = Like.objects.create(user=user, post=post)
    post.increase_like_count()
    return JsonResponse({"message": "Liked post successfully", "liked": True, "likes": post.like_count}, status=201)
        

def posts(request, type):

    if type == "all":
        posts = Post.objects.all()
       
    if type == "following":
        user = User.objects.get(pk=request.user.pk)
        posts = user.get_following_posts()
    
    
    # organize posts in chronological order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def publish(request):
    # publish post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    
    data = json.loads(request.body)
    
    # Get contents of post
    body = data.get("body", "")
    user = User.objects.get(id=request.user.pk)
    # initial_data = Post(author=user, body=body)
    # post_form = NewPostForm(instance=initial_data)
    # print(body)
    post = Post(author=user, body=body)
    post.save()

    
    return JsonResponse({"Received": "POST request received."}, status=200)
    

@csrf_exempt
@login_required
def edit_post(request, post_id):
    # edit must be done via put
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    try:
        post = Post.objects.get(pk=post_id, author=request.user.pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Invalid post ID or invalid user"}, status=400)
    
    data = json.loads(request.body)
    new_body = data.get("body", "")
    post.body = new_body
    
    post.save()
    
    return JsonResponse(post.serialize(), safe=False)
    # return JsonResponse({"Received": "POST request received."}, status=200)
    

def get_user_by_username(username):
    return User.objects.get(username=username)