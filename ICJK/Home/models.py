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
