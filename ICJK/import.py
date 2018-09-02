# This will seed the data base with data from data.csv
# need to copy and paste this in to the shell
# python3 manage.py shell

from Home.models import Store, Customer, Car, Order
import csv
import datetime

def clear_database(Order, Store, Customer, Car):
    Order.objects.all().delete()
    Store.objects.all().delete()
    Customer.objects.all().delete()
    Car.objects.all().delete()
    
clear_database(Order, Store, Customer, Car)
