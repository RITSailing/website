# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 01:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_request_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='teammember',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex=b'^\\+?1?\\d{9,15}$')]),
        ),
    ]