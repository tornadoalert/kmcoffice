# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20170831_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
