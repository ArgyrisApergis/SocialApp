from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout
import requests

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('main_app:login')
    return render(request, 'register.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)

                return redirect("main_app:dashboard")
            else:
                return redirect("main_app:login")
        else:
            form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect("main_app:login")

@login_required(login_url='http://127.0.0.1:8000/')
def dashboard(request):
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            qweet = form.save(commit=False)
            qweet.user = request.user
            qweet.save()
            return redirect("main_app:dashboard")

    followed_comments = Comments.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by("-created_at")

    return render(request,"dashboard.html",{"form": form, "comments": followed_comments},)

@login_required(login_url='http://127.0.0.1:8000/')
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})

@login_required(login_url='http://127.0.0.1:8000/')
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "profile.html", {"profile": profile})


def donate(request):
    price = 2
    url = "https://api.kanye.rest"
    r = requests.get(url)
    object = r.json()
   
    context = {
    'object': object,'price': price}
    return render(request,'donate.html', context)
    
def donate2(request):
    price = 2
    url = "https://api.kanye.rest"
    r = requests.get(url)
    object = r.json()
   
    context = {
    'object': object,'price': price}
    return render(request,'donate2.html', context)


def dash_home(request):
    comments = Comments.objects.all().order_by("-created_at")
    context = {'comments':comments}
    return render(request,"dash_home.html",context)
    
    