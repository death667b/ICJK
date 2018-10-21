from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Car, Order, Store
from django.db.models import Q, Max
from .CarView import PersonalCarView, CommercialCarView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import resolve
import json

# Create your views here.
def index(request):
    return redirect("/personal")

def get_latest_order_for_car(car):
    return Order.objects.filter(fk_car_id=car.id).order_by('-return_date').first()


def get_search_results(request, viewtype):
    query = request.GET.get('query', None)
    min_seats = request.GET.get('min_seats', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    make = request.GET.get('make', None)
    model_name = request.GET.get('model', None)
    year = request.GET.get('year', None)
    capacity = request.GET.get('capacity',None)
    store = request.GET.get('store', None)
    profession = request.GET.get('profession', None)

    query_result = []
    db_query = Q(~Q(make_name__icontains="null") & ~Q(model__icontains="null"))
    if query is not None and query is not '':
        query_words = query.split()
        for word in query_words:
            db_query &= Q(Q(make_name__icontains=word) | Q(model__icontains=word))

    #store availability filter
    # get orders for selected store
    db_query_help = Q()
    orders = Order.objects.filter(fk_return_store_id = store)
    # filter for cars which have been ordered in selected store
    for ord in orders:
        if str(get_latest_order_for_car(ord.fk_car_id).fk_return_store_id.id) == str(store):
            #add cars which last location was store to query
            db_query_help |= Q(id = ord.fk_car_id.id)
    #add help query to main query
    db_query &= db_query_help

    #passenger Count filter
    if min_seats is not None:
        db_query &= (Q(seating_capacity__gte = min_seats))

    #price filter
    if min_price is not None:
        if min_price:
            min_new_price = int(min_price)*500 #change factor
            db_query &= (Q(price_new__gte = min_new_price))

    if max_price is not None:
        if max_price:
            max_new_price = int(max_price)*500 #change factor
            db_query &= (Q(price_new__lt = max_new_price))

    #make_name filter
    make_name_set = Car.objects.values_list('make_name').distinct().filter(~Q(make_name__iexact="null"))
    if make is not None:
        db_query &= Q(make_name__iexact = make)

    if model_name is not None:
        db_query &=Q(model__iexact = model_name)

    if year is not None:
        db_query &=Q(series_year__iexact = year)

    #capacity filter
    if capacity is not None:
        capacity_restriction = Q()
        if capacity == 'small':
            for type in ['hardback','hardtop','convertible','roadster','cabriolet']:
                capacity_restriction |= Q(body_type__icontains=type)
        elif capacity == 'medium':
            for type in ['wagon','sedan','coupe','hatchback']:
                capacity_restriction |= Q(body_type__icontains=type)
        elif capacity == 'large':
            for type in ['van']:
                capacity_restriction |= Q(body_type__icontains=type)
        db_query &= capacity_restriction

    makes_models_years_set = {}
    for make in make_name_set:
        model_name_set = Car.objects.filter(make_name__iexact=make[0]).values_list('model').distinct()
        models_years = {}
        for model in model_name_set:
            years_set = Car.objects.filter(Q(make_name__iexact=make[0]) & Q(model__iexact=model[0])).values_list('series_year').distinct()
            models_years[model[0]] = [year[0] for year in years_set]
        makes_models_years_set[make[0]] = models_years

    #commercial / personal filter
    if viewtype == "commercial":
        db_query &= Q(body_type__icontains="van")
    elif viewtype == "personal":
        db_query &= ~Q(body_type__icontains="van")

    query_set = Car.objects.filter(db_query).order_by('make_name', 'model', 'series')

    #recomendation
    recomendation = None
    if len(query_set) > 1:
        recomendationCar = query_set.order_by('price_new').first()
        if recomendationCar is not None:
            recomendation = {"name": ("%s %s %s"%(recomendationCar.make_name.title(), recomendationCar.model.title(), recomendationCar.series.title())),
             "desc": "The %s %s %s made in %i is a %s %s with %i seats and a %i horsepower %iL engine." %
                     (recomendationCar.make_name.title(), recomendationCar.model.title(), recomendationCar.series, recomendationCar.series_year, recomendationCar.body_type.lower(), recomendationCar.drive.lower()
                      , recomendationCar.seating_capacity, recomendationCar.power, recomendationCar.engine_size),
             "link": "%s/%i"%(viewtype,recomendationCar.id)}

    query_result = [
        {"name": ("%s %s %s"%(car.make_name.title(), car.model.title(), car.series.title())),
         "desc": "The %s %s %s made in %i is a %s %s with %i seats and a %i horsepower %iL engine." %
                 (car.make_name.title(), car.model.title(), car.series, car.series_year, car.body_type.lower(), car.drive.lower()
                  , car.seating_capacity, car.power, car.engine_size),
         "link": "%s/%i"%(viewtype,car.id)}
        for car in query_set
        ]

    storelist = Store.objects.all().order_by("name")
    actlink = "http://127.0.0.1:8000" + request.get_full_path()

    return {

        "recomendation": recomendation,
        "appname": "ICJK Car Rentals",
        "homelink": get_current_site(request).domain,
        "query": query,
        "viewtype": viewtype,
        "min_seats": min_seats,
        "capacity": capacity,
        "makes_models_years_set" : json.dumps(makes_models_years_set),
        "min_price": min_price,
        "max_price": max_price,
        "carlist": query_result,
        "storelist": storelist,
        "store": store,
        "actlink": actlink,
    }

def search_view(request, viewtype):
    return render(request, "Home/index.html", get_search_results(request, viewtype))

def personal(request):
    return search_view(request, "personal")

def commercial(request):
    return search_view(request, "commercial")

def personalCarView(request, db_id):
    return PersonalCarView(db_id).render(request)

def commercialCarView(request, db_id):
    return CommercialCarView(db_id).render(request)
