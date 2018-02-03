# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-30 20:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePagePennantItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('header', models.CharField(blank=True, max_length=126)),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('fa_icon', models.CharField(blank=True, help_text='Copy the name of any icon from fontawesome.io/icons/', max_length=30, verbose_name='Font Awesome Icon')),
                ('position', models.IntegerField(choices=[(1, 'Left'), (2, 'Middle'), (3, 'Right')], null=True, unique=True)),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='pennant_items', to='app.HomePage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
    ]