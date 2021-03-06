# Generated by Django 2.0.5 on 2018-05-05 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rubi_food', '0017_auto_20180504_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 5, 9, 16, 52, 401886, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 5, 9, 16, 52, 399066, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='ORD_No',
            field=models.CharField(default=datetime.datetime(2018, 5, 5, 9, 16, 52, 401061), max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 5, 9, 16, 52, 401259, tzinfo=utc)),
        ),
    ]
