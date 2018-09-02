from django.contrib import admin
from .models import Store, Customer, Car, Order
# Register your models here.
admin.site.register(Store)
admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Order)