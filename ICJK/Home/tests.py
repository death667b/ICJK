from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
import random
from .models import Car
from .CarView import CarView, PersonalCarView, CommercialCarView
from django.http import Http404, HttpRequest
from .views import get_search_results
import re


# Create your tests here.

class PersonalHomeViewTest(TestCase):

    def test_no_search(self):
        #response = self.client.get(reverse('Home'))

        response = self.client.get('/personal')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars here")
        self.assertQuerysetEqual(response.context['carlist'], [])

    def test_toyota(self):
        response = self.client.get('/personal?query=Toyota&viewtype=personal&action=submit')
        self.assertEqual(response.status_code, 200)
        #change after connecting database
        self.assertContains(response, "Toyota Yaris")
        self.assertEqual(len(response.context['carlist']), 4)

class CarViewTestCases(TestCase):

    def get_random_car(self):
        cars = Car.objects.all()
        num_results = cars.count()
        return cars[random.randint(0,num_results-1)]

    def get_invalid_car_id(self):
        cars = Car.objects.order_by('id').all()
        num_results = cars.count()
        return num_results + random.randint(1,100)

    def test_create_valid_view(self):
        random_car = self.get_random_car()
        view = None
        try:
            view = CarView(random_car.id)
        except Http404:
            pass
        self.assertIsNotNone(view)

    def test_create_invalid_view(self):
        random_invalid_car_id = self.get_invalid_car_id()
        view = None
        try:
            view = CarView(random_invalid_car_id)
        except Http404:
            pass
        self.assertIsNone(view)

    def test_render_base_carview(self):
        factory = RequestFactory()
        random_car = self.get_random_car()
        view = CarView(random_car.id)
        request = factory.get('/personal')
        try:
            view.render(request)
            self.assertEqual(0,1,"'abstract' class CarView should not be able to have render() called.")
        except Http404:
            self.assertEqual(1,1)
    
    def test_create_valid_personal_view(self):
        random_car = self.get_random_car()
        view = None
        try:
            view = PersonalCarView(random_car.id)
        except Http404:
            pass
        self.assertIsNotNone(view)

    def test_create_invalid_personal_view(self):
        random_invalid_car_id = self.get_invalid_car_id()
        view = None
        try:
            view = PersonalCarView(random_invalid_car_id)
        except Http404:
            pass
        self.assertIsNone(view)

    def test_render_personal_view(self):
        factory = RequestFactory()
        random_car = self.get_random_car()
        view = PersonalCarView(random_car.id)
        request = factory.get('/personal')
        response = view.render(request)
        self.assertEquals(response.status_code, 200)

    def test_create_valid_commercial_view(self):
        random_car = self.get_random_car()
        view = None
        try:
            view = CommercialCarView(random_car.id)
        except Http404:
            pass
        self.assertIsNotNone(view)

    def test_create_invalid_commercial_view(self):
        random_invalid_car_id = self.get_invalid_car_id()
        view = None
        try:
            view = CommercialCarView(random_invalid_car_id)
        except Http404:
            pass
        self.assertIsNone(view)
    
    def test_render_commercial_view(self):
        factory = RequestFactory()
        random_car = self.get_random_car()
        view = CommercialCarView(random_car.id)
        request = factory.get('/commercial')
        response = view.render(request)
        self.assertEquals(response.status_code, 200)

    def test_get_rental_price(self):
        random_car = self.get_random_car()
        for i in range(1,10):
            d = random.randint(1,100)
            view = CarView(random_car.id)
            self.assertEqual(view.get_rental_price_for_days(d), int((random_car.price_new * d)/500))

class FilterTestCases(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = RequestFactory()

    def get_random_car(self):
        cars = Car.objects.all()
        num_results = cars.count()
        return cars[random.randint(0,num_results-1)]

    def test_text_filter(self): 
        for i in range(1,10):
            car = self.get_random_car();
            request = self.factory.get('/personal',{'query':car.make_name})
            result = get_search_results(request, 'personal')
            for car_result in result["carlist"]:
                self.assertEqual(car.make_name.lower() in car_result["name"].lower(), True)
    
    def test_capacity_filter(self):
        m = re.compile('\w+\/([0-9]+)')
        for i in range(1,10):
            request = self.factory.get('/personal',{'min_seats':i})
            result = get_search_results(request, 'personal')
            for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(car_in_db.seating_capacity >= i, True)
    
    def test_price_filter(self):
        m = re.compile('\w+\/([0-9]+)')
        for i in range(1,10):
            min = random.randint(1,200)
            max = min + random.randint(100,200)
            request = self.factory.get('/personal',{'min_price':min, 'max_price':max})
            result = get_search_results(request, 'personal')
            for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_view = CarView(car_id)
                self.assertEqual(car_view.get_rental_price_for_days(1) >= min, True)
                self.assertEqual(car_view.get_rental_price_for_days(1) <= max, True)
    
    def test_make_model_year_filter(self):
        m = re.compile('\w+\/([0-9]+)')
        for i in range(1,10):
            car = self.get_random_car();
            make = car.make_name
            model = car.model
            year = car.series_year

            request = self.factory.get('/personal',{'make':make})
            result = get_search_results(request, 'personal')
            for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(car_in_db.make_name.lower(), make.lower())

            request = self.factory.get('/personal',{'make':make,'model':model})
            result = get_search_results(request, 'personal')
            for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(car_in_db.make_name.lower(), make.lower())
                self.assertEqual(car_in_db.model.lower(), model.lower())

            request = self.factory.get('/personal',{'make':make,'model':model,'year':year})
            result = get_search_results(request, 'personal')
            for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(car_in_db.make_name.lower(), make.lower())
                self.assertEqual(car_in_db.model.lower(), model.lower())
                self.assertEqual(car_in_db.series_year, year)
            

    def test_luggage_capacity_filter(self):
        m = re.compile('\w+\/([0-9]+)')
        request = self.factory.get('/personal',{'capacity':'small'})
        result = get_search_results(request, 'personal')
        for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(any(type in car_in_db.body_type.lower() for type in ['hardback','hardtop','convertible','roadster','cabriolet']), True)

        request = self.factory.get('/personal',{'capacity':'medium'})
        result = get_search_results(request, 'personal')
        for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(any(type in car_in_db.body_type.lower() for type in ['wagon','sedan','coupe','hatchback']), True)

        request = self.factory.get('/personal',{'capacity':'large'})
        result = get_search_results(request, 'personal')
        for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                car_in_db = Car.objects.filter(id=car_id)[0]
                self.assertEqual(any(type in car_in_db.body_type.lower() for type in ['van']), True)


