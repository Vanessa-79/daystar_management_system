# Generated by Django 4.2.13 on 2024-05-12 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0007_remove_babie_registration_arrival_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='babie_registration',
            name='Arrival_Time',
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 17, 10, 22, 107995, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellingdoll',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 17, 10, 22, 110550, tzinfo=datetime.timezone.utc)),
        ),
    ]