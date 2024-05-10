# Generated by Django 4.2.13 on 2024-05-10 05:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0011_alter_babypayment_payment_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='babie_registration',
            old_name='Arrival_Time',
            new_name='Arrival_Date_and_Time',
        ),
        migrations.AlterField(
            model_name='babypayment',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='babypayment',
            name='payment_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 10, 5, 36, 31, 872719, tzinfo=datetime.timezone.utc)),
        ),
    ]
