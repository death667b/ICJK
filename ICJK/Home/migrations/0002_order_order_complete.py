# Generated by Django 2.1 on 2018-09-02 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_complete',
            field=models.BooleanField(default=True),
        ),
    ]
