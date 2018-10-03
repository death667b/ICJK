from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', include('Staff.urls'), name='Staff'),
    path('/', include('Home.urls'), name='Home'),
    path('', include('Home.urls'), name='Home'),
]
