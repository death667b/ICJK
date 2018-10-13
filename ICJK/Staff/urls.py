from django.urls import include, path, re_path
from . import views

appName = "Staff"

urlpatterns = [
    re_path(r'^login/.*$', views.login_view, name="login"),
    path('create/', views.create, name="create"),
    path('auth/', views.auth, name="auth"),
    path('logout/', views.logout_view, name="logout"),
    path('landing/', views.landing_view, name="landing"),
    path('priority/', views.priority_purchase_view, name="priority"),
    path('logistics/', views.logistics_view, name="logistics")
]
