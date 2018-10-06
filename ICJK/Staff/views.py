from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from .StaffAccountCreationForm import StaffAccountCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .AuthResult import AUTH_RESULT



# Create your views here.
def login_view(request):
    createform = StaffAccountCreationForm()
    authform = AuthenticationForm()
    return render(request, "Staff/login.html", {
        "createform": createform,
        "authform": authform,
        "applink": "http://" + get_current_site(request).domain + "/",
        "appname": "ICJK Car Rentals"
    })

@login_required(login_url='login')
def landing_view(request):
    return render(request, "Staff/landing.html", {
        "applink": "http://" + get_current_site(request).domain + "/",
        "appname": "ICJK Car Rentals"
    })

def auth(request):
    if request.method == 'POST':
        authform = AuthenticationForm(data=request.POST)
        if authform.is_valid():
            user = authform.get_user()
            return log_in_and_send_to_next(request, user)
        else:
            return redirect(reverse('login') + '/?result=%i&view=0'%AUTH_RESULT.LOGIN_INVALID_COMBINATION.value)
    else:
        return redirect(reverse('login') + '/?result=%i&view=0'%AUTH_RESULT.LOGIN_OTHER.value)

def create(request):
    if request.method == 'POST':
        form = StaffAccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return log_in_and_send_to_next(request, user)
        else:
            error = form.previous_error
            return redirect(reverse('login') + '/?result=%i&view=1'%error.value)

def log_in_and_send_to_next(request, user):
    login(request, user)
    if(request.POST.get("next", None) is not None):
        return redirect(request.POST.next)
    return redirect("landing")

def logout_view(request):
    try:
        logout(request)
    except Exception:
        pass
    finally:
        return redirect(reverse('login'))
    
    