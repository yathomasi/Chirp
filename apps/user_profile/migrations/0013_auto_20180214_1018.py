# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-14 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_auto_20180210_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='user_profile.User_details'),
        ),
    ]