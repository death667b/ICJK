from .models import Car
from django.shortcuts import render
from django.http import Http404
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site

class CarView():
    def __init__(self, db_id):
        self.id = db_id
        self.db_query = Car.objects.filter(id=db_id).order_by('make_name', 'model', 'series')
        self.car_data = None
        num_results = self.db_query.count()
        if num_results == 0:
            raise Http404("Unknown Car ID")
        for car in self.db_query:
            self.car_data = car
            break

    def make_default_json_params(self, request):
        data = {
            "fullname": "%s %s %s"%(self.car_data.make_name.title(), self.car_data.model.title(), self.car_data.series.title()),
            "appname": "ICJK Car Rentals",
            "homelink": "http://" + get_current_site(request).domain,
            "actlink": "http://127.0.0.1:8000" + request.get_full_path(),
        }
        model_data = model_to_dict(self.car_data)
        model_data_pretty = {}
        for k,v in model_data.items():
            if k.lower() == "id":
                continue
            if k.lower() == "null" or str(v).lower() == "null":
                continue
            model_data_pretty[k.title().replace('_',' ')] = str(v).title()
        data.update({"details":model_data_pretty})
        return data

    def get_rental_price_for_days(self, days):
        return int((self.car_data.price_new * days)/500)

    def render(self, request):
        raise Http404("Unknown Car Type")


class CommercialCarView(CarView):
    def __init__(self, db_id):
        super().__init__(db_id)

    def render(self, request):
        json_data = super().make_default_json_params(request)
        json_data["viewtype"] = "commercial"
        json_data["pricemultiplier"] = super().get_rental_price_for_days(1)
        return render(request, 'Home/car.html', json_data)

class PersonalCarView(CarView):
    def __init__(self, db_id):
        super().__init__(db_id)

    def render(self, request):
        json_data = super().make_default_json_params(request)
        json_data["viewtype"] = "personal"
        json_data["pricelist"] = [
            {
                "period":"24 hours",
                "cost":super().get_rental_price_for_days(1)
            },
            {
                "period":"48 hours",
                "cost":super().get_rental_price_for_days(2)
            },
            {
                "period":"7 days",
                "cost":super().get_rental_price_for_days(7)
            }
        ]
        return render(request, 'Home/car.html', json_data)
