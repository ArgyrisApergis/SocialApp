from django.urls import path, include
from .views import *

urlpatterns = [
    path('quotes/', quotes, name= 'quotes')
]