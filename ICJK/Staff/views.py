from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from .StaffAccountCreationForm import StaffAccountCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .AuthResult import AUTH_RESULT
from django.db.models import Q, Max
from Home.models import Car, Order, Store





# Create your views here.
@login_required(login_url='login')
def priority_purchase_view(request):

    #get value for store
    store = request.GET.get('store', None)

    #init db_query and query result
    query_result = []
    db_query = Q(~Q(make_name__icontains="null") & ~Q(model__icontains="null"))

    # get orders for selected store
    # car could also be somewhere else; annotate doesn´t work
    orders = Order.objects.values("fk_car_id", "fk_return_store_id").annotate(Max('return_date')).filter(fk_return_store_id = store)

    # filter for cars which have been ordered in selected store
    db_query_help = Q()
    for order in orders:
        db_query_help |= Q(id = order['fk_car_id'])

    db_query &= db_query_help
    query_set = Car.objects.filter(db_query).order_by('make_name', 'model', 'series')

    #build result
    for car in query_set:
        timeStore = 0
        time = 0
        ord = Order.objects.filter(fk_car_id = car.id)
        for o in ord:
            time += (o.return_date - o.pickup_date).days
            if str(o.fk_pickup_store_id.id) == store or str(o.fk_return_store_id.id) == store:
                timeStore += (o.return_date - o.pickup_date).days

        query_result.append(
        {"name": ("%s %s %s"%(car.make_name.title(), car.model.title(), car.series.title())),
         "total": "Rented for %i days in total."%(time),
         "store": "Rented for %i days in selected store."%(timeStore),
         "orders": "Was ordered %i time(s)."%(len(ord)),
         "avg": "The average renting time is %i days." %(time/len(ord)),
         "profit": "The total profit is %i$."%((time*(car.price_new/500)-car.price_new)),
         # "link": "%s/%i"%(viewtype,car.id)
         # "link": "todo"
         })

    #select storelist for dropdown
    storelist = Store.objects.all().order_by("name")

    return render(request, "Staff/priority_purchase.html", {
        "appname": "ICJK Car Rentals - Priority Purchase Report",
        "applink": "http://" + get_current_site(request).domain + "/",
        "carlist": query_result,
        "storelist": storelist,
        "store": store,
    })

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
