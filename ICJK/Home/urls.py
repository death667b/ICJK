from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.index),
    path('personal', views.personal),
    path('commercial', views.commercial),
    path('personal/<int:db_id>', views.personalCarView, name="personal"),
    path('commercial/<int:db_id>', views.commercialCarView, name="commercial")
]
