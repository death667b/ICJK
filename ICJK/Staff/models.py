from django.db import models

class StaffAccount(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    pass_hash = models.CharField(max_length=100)
    last_seen = models.DateField()