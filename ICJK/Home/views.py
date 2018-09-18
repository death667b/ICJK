from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Car
from django.db.models import Q
from .CarView import PersonalCarView, CommercialCarView
from django.contrib.sites.shortcuts import get_current_site
import json

# Create your views here.
def index(request):
    return redirect("/personal")

def get_search_results(request, viewtype):
    query = request.GET.get('query', None)
    min_seats = request.GET.get('min_seats', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    make = request.GET.get('make', None)
    model_name = request.GET.get('model', None)
    year = request.GET.get('year', None)


    query_result = []
    db_query = Q(~Q(make_name__icontains="null") & ~Q(model__icontains="null"))
    if query is not None and query is not '':
        query_words = query.split()
        print(query_words)
        for word in query_words:
            db_query &= Q(Q(make_name__icontains=word) | Q(model__icontains=word))

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
    make_name_set = Car.objects.values_list('make_name').distinct().filter(~Q(make_name__icontains="null"))
    if make is not None:
        db_query &= Q(make_name = make)

    makes_models_years_set = {}
    for make in make_name_set:
        model_name_set = Car.objects.filter(make_name__icontains=make[0]).values_list('model').distinct()
        models_years = {}
        for model in model_name_set:
            years_set = Car.objects.filter(Q(make_name__icontains=make[0]) & Q(model__icontains=model[0])).values_list('series_year').distinct()
            models_years[model[0]] = [year[0] for year in years_set]            
        makes_models_years_set[make[0]] = models_years

    #commercial / personal filter
    if viewtype == "commercial":
        db_query &= Q(model__icontains="VAN")
    elif viewtype == "personal":
        db_query &= ~Q(model__icontains="VAN")

    query_set = Car.objects.filter(db_query).order_by('make_name', 'model', 'series')

    query_result = [
        {"name": ("%s %s %s"%(car.make_name.title(), car.model.title(), car.series.title())),
         "desc": "The %s %s %s made in %i is a %s %s with %i seats and a %i horsepower %iL engine." %
                 (car.make_name.title(), car.model.title(), car.series, car.series_year, car.body_type.lower(), car.drive.lower()
                  , car.seating_capacity, car.power, car.engine_size),
         "link": "%s/%i"%(viewtype,car.id)}
        for car in query_set
        ]
    return {
        "appname": "ICJK Car Rentals",
        "homelink": get_current_site(request).domain,
        "query": query,
        "viewtype": viewtype,
        "min_seats": min_seats,
        "makes_models_years_set" : json.dumps(makes_models_years_set),
        "min_price": min_price,
        "max_price": max_price,
        "carlist": query_result,
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
