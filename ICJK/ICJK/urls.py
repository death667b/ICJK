from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('Staff.urls')),
    path('/', include('Home.urls'), name='Home'),
    path('', include('Home.urls')),
]
