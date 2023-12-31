# Generated by Django 4.2.6 on 2023-11-25 16:57

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0002_trendingplace_multiimagestrendingplace_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='noName', unique=True)),
                ('company', models.CharField(choices=[('A', 'Airbus'), ('B', 'Boeing'), ('L', 'Lockheed Martin'), ('R', 'Raytheon')], default='A', max_length=1)),
                ('capacity', models.PositiveIntegerField(default=100)),
                ('maxLoad', models.PositiveIntegerField(default=10)),
                ('baggageWeight', models.PositiveIntegerField(default=20)),
                ('maxDistance', models.PositiveIntegerField(default=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='noName')),
                ('additionalCostPercentage', models.FloatField(default=1000, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(70)])),
                ('seatCategory', models.CharField(choices=[('E', 'Economy Class Seats'), ('P', 'Premium Economy Class Seats'), ('B', 'Business Class Seats'), ('F', 'First-Class Seats')], default='E', max_length=1)),
                ('mealCategory', models.CharField(choices=[('S', 'Standard vegetarian.'), ('V', 'Vegan'), ('F', 'Fruit platter'), ('R', 'Raw vegetable'), ('M', 'Muslim meal')], default='M', max_length=1)),
                ('drinkCategory', models.CharField(choices=[('O', 'Only water'), ('W', 'Warm Drinks only'), ('C', 'Cold drinks only'), ('B', 'Both Cold and Warm drinks')], default='O', max_length=1)),
                ('wifiAvailability', models.BooleanField(default=False)),
                ('powerOutlet', models.BooleanField(default=False)),
                ('streamEntertainment', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureTime', models.DateTimeField(default=datetime.datetime.now)),
                ('arrivalTime', models.DateTimeField(default=datetime.datetime.now)),
                ('distance', models.PositiveIntegerField(default=0)),
                ('availableSeats', models.PositiveIntegerField(default=0)),
                ('baseCost', models.FloatField(default=1000, validators=[django.core.validators.MinValueValidator(0)])),
                ('offerPercentage', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('status', models.CharField(choices=[('A', 'Active'), ('C', 'cancelled')], default='M', max_length=1)),
                ('aircraft', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='flights.aircraft')),
                ('endAirport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inFlights', to='countries.airport')),
                ('startAirport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outFlights', to='countries.airport')),
            ],
        ),
    ]
