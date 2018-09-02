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
