import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow
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
        profile = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    
    posts = Post.objects.filter(author=profile).order_by("-timestamp").all()
    
    return render(request, "network/profile.html",{
        "profile": profile,
        "followers": profile.get_followers(),
        "following": profile.get_following(),
        "is_following": user.is_following(profile),
        "posts": posts,
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


## API Views:

# Creates or deletes a follow
@csrf_exempt
@login_required
def set_follow(request, username):
    try:
        followee = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    if request.method == "PUT":
        user = User.objects.get(id=request.user.pk)
        if user.is_following(followee):
            try:
                follow = Follow.objects.get(followee=followee, follower=user).delete()
            except Follow.DoesNotExist:
                return JsonResponse({"error": "No such follow exists"}, status=404)
                
            return JsonResponse({"message": "Unfollowed successfully", "following": False}, status=201)
            
        follow = Follow.objects.create(followee=followee, follower=user)
        return JsonResponse({"message": "Followed successfully", "following": True}, status=201)
        

def posts(request, type):
    print(type)
    # Remove as you add this usage to front end
    # print(type)
    if type == "all":
        posts = Post.objects.all()
    
    
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
    
    # return JsonResponse({"error": "Something went wrong"}, status=400)
        