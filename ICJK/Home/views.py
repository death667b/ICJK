from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Car
from django.db.models import Q

# Create your views here.
def index(request):
    return redirect("/personal")

def search_view(request, viewtype):

    query = request.GET.get('query', None)
    min_seats = request.GET.get('min_seats', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)


    query_result = []
    db_query = Q()
    if query is not None and query is not '':
        query_words = query.split()
        print(query_words)
        for word in query_words:
            db_query &= Q(Q(make_name__contains=word) | Q(model__contains=word))
        #db_query.add(Q(model__in=query_words), Q.OR)

    #passenger Count filter
    if min_seats is not None:
        db_query &= (Q(seating_capacity__gte = min_seats))

    #price filter
    #bug: try max: 1 you will get cars, what doesnt make sense
    if min_price is not None:
        if min_price:
            min_new_price = min_price*3000 #change factor
            db_query &= (Q(price_new__gte = min_new_price))

    if max_price is not None:
        if max_price:
            max_new_price = max_price*3000 #change factor
            db_query &= (Q(price_new__lt = max_new_price))

    query_set = Car.objects.filter(db_query).order_by('make_name', 'model', 'series')

    query_result = [
        {"name": ("%s %s %s"%(car.make_name.title(), car.model.title(), car.series.title())),
         "desc": "The %s %s %s made in %i is a %s %s with %i seats and a %i horsepower %iL engine." %
                 (car.make_name.title(), car.model.title(), car.series, car.series_year, car.body_type.lower(), car.drive.lower()
                  , car.seating_capacity, car.power, car.engine_size),
         "link": car.id}
        for car in query_set
        #isn´t it more efficient to do this in the index.html since there is already a for loop?
        ]


    return render(request, "Home/index.html", {
        "appname": "ICJK Car Rentals",
        "query": query,
        "viewtype": viewtype,
        "min_seats": min_seats,
        "min_price": min_price,
        "max_price": max_price,
        "carlist": query_result,
    })

def personal(request):
    return search_view(request, "personal")

def commercial(request):
    return search_view(request, "commercial")
