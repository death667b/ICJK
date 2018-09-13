from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('personal', views.personal),
    path('commercial', views.commercial),
    path('cars/<int:db_id>', views.carview)
]
