from django.db import models

# Create your models here.
class Store(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class Customer(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=255)
    phone = models.IntegerField()
    birthday = models.DateField()
    occupation = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)

class Car(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    make_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    series = models.CharField(max_length=100)
    series_year = models.IntegerField()
    price_new = models.IntegerField()
    engine_size = models.FloatField()
    fuel_system = models.CharField(max_length=100)
    tank_capacity = models.FloatField()
    power =  models.IntegerField()
    seating_capacity = models.IntegerField()
    standard_transmission = models.CharField(max_length=100)
    body_type = models.CharField(max_length=100)
    drive = models.CharField(max_length=100)
    wheelbase = models.IntegerField()
