# Generated by Django 4.2.13 on 2024-05-28 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycare_app', '0014_sellingdoll_total_amount_alter_babypayment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrivalsitter',
            name='Status',
            field=models.CharField(choices=[('', 'select status'), ('On Duty', 'On Duty'), ('Off Duty', 'Off Duty')], max_length=10),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='Date_of_purchase',
            field=models.DateField(default=datetime.datetime(2024, 5, 28, 8, 24, 8, 836132, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellingdoll',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 5, 28, 8, 24, 8, 836645, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellingdoll',
            name='total_amount',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]
