# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-06 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemonitor', '0004_auto_20180501_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='isdeleted',
            field=models.BooleanField(default=False),
        ),
    ]
