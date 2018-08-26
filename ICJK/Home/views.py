from django.shortcuts import render, redirect

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In orci justo, facilisis non pulvinar aliquam, ullamcorper vel purus."
# Create your views here.
def index(request):
    return redirect("/personal")

def personal(request):
    return render(request, "Home/index.html", {
        "appname": "ICJK Car Rentals",
        "viewtype":"personal",
        "carlist":[
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
        ]
    })

def commercial(request):
    return render(request, "Home/index.html", {
        "appname": "ICJK Car Rentals",
        "viewtype": "commercial",
        "carlist": [
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
    })