# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-01 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemonitor', '0003_site_ismonitoring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.URLField(),
        ),
    ]
