from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('personal', views.personal),
    path('commercial', views.commercial),
    path('personal/<int:db_id>', views.personalCarView),
    path('commercial/<int:db_id>', views.commercialCarView)
]
