from django.test import TestCase
from .StaffAccountCreationForm import StaffAccountCreationForm
from django.test.client import RequestFactory
from django.http import Http404, HttpRequest
from django.forms import ValidationError
from .AuthResult import AUTH_RESULT
from Home.models import Order, Store
import re
from django.contrib.auth.models import User
from .views import priority_purchase_view, get_orders_from_store
import random

# Create your tests here.

class StaffAccountCreationFormTests(TestCase):

    def create_user(self, email, password):
        try:
            u = User.objects.get(email=email)
            self.delete_user(email)
        except User.DoesNotExist:
            pass
        form = StaffAccountCreationForm({
            'email':email,
            'password': password,
            'password_confirm': password
        })
        form.is_valid()
        return form.save()

    def delete_user(self, email):
        try:
            u = User.objects.get(email=email)
            u.delete()
        except User.DoesNotExist:
            pass

    def test_form_creation(self):
        form = None
        try:
            form = StaffAccountCreationForm({
                'email':'user@icjk.com.au',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        except Exception:
            pass
        self.assertIsNotNone(form)

    def test_password_similarity(self):
        form = StaffAccountCreationForm({
                'email':'staffaccount12@icjk.com.au',
                'password':'staffaccount12',
                'password_confirm':'staffaccount12'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_small_password(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'smolpwd',
                'password_confirm':'smolpwd'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_numeric_only_password(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'4815162342',
                'password_confirm':'4815162342'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_alpha_only_password(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'staffpassword',
                'password_confirm':'staffpassword'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_PASSWORD)

    def test_non_staff_email(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@gmail.com',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_EMAIL)

    def test_existing_email(self):
        user_email = 'staff_test@icjk.com.au'
        user_password = 'p45sword1235'
        self.create_user(user_email, user_password)
        form = StaffAccountCreationForm({
                'email':user_email,
                'password':user_password,
                'password_confirm':user_password
            })
        res = form.is_valid()
        self.delete_user(user_email)
        self.assertEqual(res, False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_EMAIL_IN_USE)

    def test_different_password_confirmation(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'p45sword1235',
                'password_confirm':'password54321'
            })
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.previous_error, AUTH_RESULT.SIGNUP_INVALID_CONFIRMATION)

    def test_working_combination(self):
        form = StaffAccountCreationForm({
                'email':'staff_test@icjk.com.au',
                'password':'p45sword1235',
                'password_confirm':'p45sword1235'
            })
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.previous_error, AUTH_RESULT.NO_ERROR)

class LogisticsViewTests(TestCase):
    def get_random_store(self):
        stores = Store.objects.all()
        num_results = stores.count()
        return stores[random.randint(0,num_results-1)]
    
    def test_different_stores_filter_off(self):
        for i in range(1,20):
            store_start = self.get_random_store()
            store_end = None
            while True:
                store_end = self.get_random_store()
                if store_end.id != store_start.id: # Ensure they are different stores
                    break
            orders = get_orders_from_store(store_start.name, store_end.name, False)
            for order in orders:
                self.assertEqual(order.fk_pickup_store_id.id, store_start.id)
                self.assertEqual(order.fk_return_store_id.id, store_end.id)


    def test_same_store_filter_off(self):
        for i in range(1,20):
            store_start = self.get_random_store()
            store_end = store_start
            orders = get_orders_from_store(store_start.name, store_end.name, False)
            for order in orders:
                self.assertEqual(order.fk_pickup_store_id.id, store_start.id)
                self.assertEqual(order.fk_pickup_store_id.id, order.fk_return_store_id.id)

    def test_different_stores_filter_on(self):
        pass
    
    def test_same_store_filter_on(self):
        pass

    def test_anywhere_filter_off(self):
        pass

    def test_anywhere_filter_on(self):
        pass




class priority_purchase_view_test(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = RequestFactory()

    def test_store_filter(self):
        print("test priority_purchase")
        m = re.compile('\w+\/([0-9]+)')
        for store in Store.objects.all():
            request = self.factory.get('/priority',{'store': str(store.id)})
            result = priority_purchase_view(request)
            #self.assertEqual(len(result["carlist"])  , 2)
            for car_result in result["carlist"]:
                car_id = m.match(car_result["link"])[1]
                last_order = Order.objects.filter(fk_car_id=car_id).order_by('-return_date').first()

                o = Order.objects.filter(fk_car_id=car_id).order_by('-return_date')
                for ord in o:
                    last_store_id = last_order.fk_return_store_id.id
                    self.assertEqual(last_store_id, store.id)
