# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 19:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_remove_claim_pre_claim_approved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='claim',
            options={'permissions': (('claim_js_approve', 'Can approve the claim with js status'),)},
        ),
        migrations.AlterModelOptions(
            name='preclaim',
            options={'permissions': (('preclaim_dean_approve', 'Dean approval for Preclaim'),)},
        ),
    ]