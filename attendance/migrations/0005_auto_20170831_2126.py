# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='pre_claim_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='preclaim',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preclaims', to='attendance.Event'),
        ),
    ]
