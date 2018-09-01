from django.shortcuts import render, redirect
from django.http import JsonResponse

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In orci justo, facilisis non pulvinar aliquam, ullamcorper vel purus."

dummy_carlist = [
            {
                "name": "Suzuki Swift",
                "desc": lorem,
                "link": "Suzuki_Swift"
            },
            {
                "name": "Toyota Yaris",
                "desc": lorem,
                "link": "Toyota_Yaris"
            },
            {
                "name": "Toyota Corolla",
                "desc": lorem,
                "link": "Toyota_Corolla"
            },
            {
                "name": "Hyundai Elantra",
                "desc": lorem,
                "link": "Hyundai_Elantra"
            },
            {
                "name": "Toyota Landcruiser Workmate",
                "desc": lorem,
                "link": "Toyota_Landcruiser_Workmate"
            },
            {
                "name": "Mercedes-Benz Sprinter",
                "desc": lorem,
                "link": "Mercedes-Benz_Sprinter"
            },
            {
                "name": "Toyota Hiace",
                "desc": lorem,
                "link": "Toyota_Hiace"
            }
]


# Create your views here.
def index(request):
    return redirect("/personal")

def search_view(request, viewtype):

    query = request.GET.get('query', None)

    query_result = []
    if query is not None:
        # Simple dummy search until actual search is implemented
        result = [car for car in dummy_carlist if query in car["name"]]

    return render(request, "Home/index.html", {
        "appname": "ICJK Car Rentals",
        "query": query_result,
        "viewtype":viewtype,
        "carlist":result
    })

def personal(request):
    return search_view(request, "personal")

def commercial(request):
    return search_view(request, "commercial")


