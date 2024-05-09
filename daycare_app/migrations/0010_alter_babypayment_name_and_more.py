# Generated by Django 4.2.13 on 2024-05-09 13:30

import datetime
import daycare_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0009_alter_babypayment_full_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babypayment',
            name='name',
            field=models.CharField(max_length=200, validators=[daycare_app.models.validate_letters]),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 9, 13, 30, 39, 351884, tzinfo=datetime.timezone.utc)),
        ),
    ]
