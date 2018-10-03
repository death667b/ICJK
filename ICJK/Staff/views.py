from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from .StaffAccountCreationForm import StaffAccountCreationForm
from .SignupResult import SIGNUP_RESULT


# Create your views here.
def login_view(request):
    form = StaffAccountCreationForm()
    return render(request, "Staff/login.html", {
        "form": form,
        "applink": "http://" + get_current_site(request).domain + "/",
        "appname": "ICJK Car Rentals"
    })

def landing_view(request):
    return render(request, "Staff/landing.html")

def create(request):
    if request.method == 'POST':
        form = StaffAccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing")
        else:
            error = form.previous_error
            return redirect(reverse('login') + '/?result=%i'%error.value)