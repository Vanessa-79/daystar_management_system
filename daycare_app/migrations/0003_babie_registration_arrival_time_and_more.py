# Generated by Django 4.2.13 on 2024-05-12 16:48

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0002_arrivalsitter_arrival_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='babie_registration',
            name='Arrival_Time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 16, 48, 37, 668435, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellingdoll',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 16, 48, 37, 669436, tzinfo=datetime.timezone.utc)),
        ),
    ]
