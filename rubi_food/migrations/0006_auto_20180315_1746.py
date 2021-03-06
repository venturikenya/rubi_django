# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-15 17:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rubi_food', '0005_auto_20180315_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 15, 17, 46, 12, 240197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 15, 17, 46, 12, 237277, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='food',
            name='belongs_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubi_food.Category'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ORD_No',
            field=models.CharField(default=datetime.datetime(2018, 3, 15, 17, 46, 12, 239263), max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 15, 17, 46, 12, 239443, tzinfo=utc)),
        ),
    ]
