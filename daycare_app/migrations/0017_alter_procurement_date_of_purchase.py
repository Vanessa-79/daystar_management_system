# Generated by Django 4.2.13 on 2024-05-10 17:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0016_alter_babypayment_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 10, 17, 48, 9, 888619, tzinfo=datetime.timezone.utc)),
        ),
    ]
