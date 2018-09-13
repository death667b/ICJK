from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Car
from django.db.models import Q

from .CarView import PersonalCarView, CommercialCarView

# Create your views here.
def index(request):
    return redirect("/personal")

def search_view(request, viewtype):

    query = request.GET.get('query', None)
    min_seats = request.GET.get('min_seats', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    make = request.GET.get('make', None)
    model_name = request.GET.get('model', None)
    year = request.GET.get('year', None)


    query_result = []
    db_query = Q()
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
    model_query = Q()
    make_name_set = Car.objects.filter(model_query).values_list('make_name').distinct()
    if make is not None:
        db_query &= Q(make_name = make)
        model_query &= Q(make_name = make)

    #model filter
    model_set = Car.objects.filter(model_query).values_list('model').distinct()
    if model_name is not None:
        db_query &= Q(model = model_name)
        model_query &= Q(model = model_name)

    #year filter
    year_set = Car.objects.filter(model_query).values_list('series_year').distinct()
    if year is not None:
        db_query &= Q(series_year = year)
        model_query &= Q(series_year = year)

    query_set = Car.objects.filter(db_query).order_by('make_name', 'model', 'series')

    query_result = [
        {"name": ("%s %s %s"%(car.make_name.title(), car.model.title(), car.series.title())),
         "desc": "The %s %s %s made in %i is a %s %s with %i seats and a %i horsepower %iL engine." %
                 (car.make_name.title(), car.model.title(), car.series, car.series_year, car.body_type.lower(), car.drive.lower()
                  , car.seating_capacity, car.power, car.engine_size),
         "link": "cars/%i"%car.id}
        for car in query_set
        #isn´t it more efficient to do this in the index.html since there is already a for loop?
        ]


    return render(request, "Home/index.html", {
        "appname": "ICJK Car Rentals",
        "query": query,
        "viewtype": viewtype,
        "min_seats": min_seats,
        "makelist" : make_name_set,
        "modellist" : model_set,
        "yearlist" : year_set,
        "min_price": min_price,
        "max_price": max_price,
        "carlist": query_result,
    })

def personal(request):
    return search_view(request, "personal")

def commercial(request):
    return search_view(request, "commercial")

def carview(request, db_id):
    return PersonalCarView(db_id).render(request)
