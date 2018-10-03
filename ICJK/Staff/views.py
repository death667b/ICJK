from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def login_view(request):
    form = UserCreationForm()
    return render(request, "Staff/login.html", {
        "form": form,
        "applink": "http://" + get_current_site(request).domain + "/",
        "appname": "ICJK Car Rentals"
    })