# Generated by Django 4.2.13 on 2024-05-09 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0006_remove_arrivalsitter_total_babies_attended_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 9, 9, 53, 34, 620230, tzinfo=datetime.timezone.utc)),
        ),
    ]
