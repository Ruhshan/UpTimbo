# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-25 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=100)),
                ('interval', models.IntegerField(default=120)),
            ],
        ),
    ]
