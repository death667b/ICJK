from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Car
from django.db.models import Q

# Create your views here.
def index(request):
    return redirect("/personal")

def search_view(request, viewtype):

    query = request.GET.get('query', None)

    query_result = []
    if query is not None and query is not '':
        query_words = query.split()
        print(query_words)
        db_query = Q()
        for word in query_words:
            db_query &= Q(Q(make_name__contains=word) | Q(model__contains=word))
        #db_query.add(Q(model__in=query_words), Q.OR)

        query_set = Car.objects.filter(db_query).order_by('make_name', 'model', 'series')
        query_result = [
            {"name": ("%s %s %s"%(car.make_name.title(), car.model.title(), car.series.title())),
             "desc": "The %s %s %s made in %i is a %s %s with %i seats and a %i horsepower %iL engine." %
                     (car.make_name.title(), car.model.title(), car.series, car.series_year, car.body_type.lower(), car.drive.lower()
                      , car.seating_capacity, car.power, car.engine_size),
             "link": car.id}
            for car in query_set
        ]

    return render(request, "Home/index.html", {
        "appname": "ICJK Car Rentals",
        "query": query,
        "viewtype": viewtype,
        "carlist": query_result
    })

def personal(request):
    return search_view(request, "personal")

def commercial(request):
    return search_view(request, "commercial")
