# Generated by Django 2.1 on 2018-09-05 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_auto_20180902_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='phone',
            field=models.CharField(max_length=100),
        ),
    ]