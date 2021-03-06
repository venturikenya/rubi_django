# Generated by Django 2.0.5 on 2018-05-04 15:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rubi_food', '0014_auto_20180504_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 15, 55, 28, 469008, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 15, 55, 28, 466074, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='ORD_No',
            field=models.CharField(default=datetime.datetime(2018, 5, 4, 15, 55, 28, 468184), max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 4, 15, 55, 28, 468384, tzinfo=utc)),
        ),
    ]
