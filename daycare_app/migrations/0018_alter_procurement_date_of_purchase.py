# Generated by Django 4.2.13 on 2024-05-10 17:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0017_alter_procurement_date_of_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 10, 17, 49, 55, 963018, tzinfo=datetime.timezone.utc)),
        ),
    ]
