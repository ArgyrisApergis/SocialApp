from django.urls import path
from .views import *

app_name = "main_app"

urlpatterns = [
    path("", login, name="login"),
    path("register", register, name="register"),
    path("dashboard", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
]