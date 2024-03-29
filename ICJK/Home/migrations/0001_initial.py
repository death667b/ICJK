# Generated by Django 2.1 on 2018-08-30 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('make_name', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('series', models.CharField(max_length=100)),
                ('series_year', models.IntegerField()),
                ('price_new', models.IntegerField()),
                ('engine_size', models.FloatField()),
                ('fuel_system', models.CharField(max_length=100)),
                ('tank_capacity', models.FloatField()),
                ('power', models.IntegerField()),
                ('seating_capacity', models.IntegerField()),
                ('standard_transmission', models.CharField(max_length=100)),
                ('body_type', models.CharField(max_length=100)),
                ('drive', models.CharField(max_length=100)),
                ('wheelbase', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('adress', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
                ('birthday', models.DateField()),
                ('occupation', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateField()),
                ('pickup_date', models.DateField()),
                ('return_date', models.DateField()),
                ('fk_car_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Home.Car')),
                ('fk_customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Home.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='fk_pickup_store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_pickup_store_id', to='Home.Store'),
        ),
        migrations.AddField(
            model_name='order',
            name='fk_return_store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_return_store_id', to='Home.Store'),
        ),
    ]
