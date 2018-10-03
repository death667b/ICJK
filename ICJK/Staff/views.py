from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from enum import Enum

class SIGNUP_RESULT(Enum):
    NO_ERROR = 0
    INVALID_EMAIL = 1
    INVALID_PASSWORD = 2
    INVALID_CONFIRMATION = 3
    EMAIL_IN_USE = 4
    OTHER = 5



# Create your views here.
def login_view(request):
    form = UserCreationForm()
    result = request.GET.get('result', None)
    return render(request, "Staff/login.html", {
        "result": result if result is not None else SIGNUP_RESULT.NO_ERROR,
        "form": form,
        "applink": "http://" + get_current_site(request).domain + "/",
        "appname": "ICJK Car Rentals"
    })

def landing_view(request):
    return render(request, "Staff/landing.html")

def create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing")
        else:
            reason = SIGNUP_RESULT.OTHER




            return redirect(reverse('login') + '/?result=%s'%'5')