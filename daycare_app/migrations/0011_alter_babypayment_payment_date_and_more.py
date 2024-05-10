# Generated by Django 4.2.13 on 2024-05-09 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0010_alter_babypayment_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babypayment',
            name='payment_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 9, 13, 32, 27, 421600, tzinfo=datetime.timezone.utc)),
        ),
    ]