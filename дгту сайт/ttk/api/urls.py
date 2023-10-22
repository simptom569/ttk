from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_place),
    path('create_link', views.create_link)
]
