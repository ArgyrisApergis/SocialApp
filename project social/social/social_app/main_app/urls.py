from django.urls import path
from .views import *
from django.conf.urls.static import static

app_name = "main_app"

urlpatterns = [
    path("", dash_home, name="dash_home"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("user_logout", user_logout, name="user_logout"),
    path("dashboard", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("donate", donate, name= "donate"),
    path("donate2", donate2, name= "donate2"),
]