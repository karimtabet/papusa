# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-30 20:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_homepagepennantitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagepennantitem',
            name='position',
        ),
    ]
