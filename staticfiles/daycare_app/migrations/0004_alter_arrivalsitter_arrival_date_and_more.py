# Generated by Django 4.2.13 on 2024-05-12 16:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0003_babie_registration_arrival_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrivalsitter',
            name='Arrival_Date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 12, 16, 50, 50, 393843, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 16, 50, 50, 398842, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellingdoll',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 5, 12, 16, 50, 50, 400354, tzinfo=datetime.timezone.utc)),
        ),
    ]
