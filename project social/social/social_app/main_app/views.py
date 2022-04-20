from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('main_app:dashboard')
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
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
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


def gallery_view(request, pk):
    pet = Pet.objects.get(id=pk)
    return render(request, 'gallery.html', {"pet":pet})

def add_pet_view(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm)

    if request.method == "GET":
        pet_form = PetForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        return render(request, 'create.html', {"pet_form":pet_form, "formset":formset})
    elif request.method == "POST":
        pet_form = PetForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        if pet_form.is_valid() and formset.is_valid():
            pet_obj = pet_form.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    Image.objects.create(image=image, pet=pet_obj)
            return HttpResponseRedirect('main_app:gallery')
        else:
            print(pet_form.errors, formset.errors)