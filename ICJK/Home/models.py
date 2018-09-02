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
    address = models.CharField(max_length=255)
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

class Order(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    create_date = models.DateField()
    pickup_date = models.DateField()
    return_date = models.DateField()
    order_complete = models.BooleanField(default=True)
    fk_car_id = models.ForeignKey(Car, on_delete=models.PROTECT)
    fk_customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    fk_pickup_store_id = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='fk_pickup_store_id')
    fk_return_store_id = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='fk_return_store_id')