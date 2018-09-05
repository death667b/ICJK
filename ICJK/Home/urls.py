from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('personal', views.personal, name='Home'),
    path('commercial', views.commercial)
]
