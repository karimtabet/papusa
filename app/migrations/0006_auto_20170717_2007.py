# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('app', '0005_auto_20170716_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormPageSidebarItem',
            fields=[
                ('sidebaritem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.SidebarItem')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('app.sidebaritem', models.Model),
        ),
        migrations.AddField(
            model_name='formpage',
            name='feed_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='formpage',
            name='sidebar',
            field=models.CharField(choices=[('no_sidebar', 'No  Sidebar'), ('left_sidebar', 'Left Sidebar'), ('right_sidebar', 'Right Sidebar')], default='no_sidebar', max_length=13),
        ),
        migrations.AddField(
            model_name='formpagesidebaritem',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='sidebar_items', to='app.FormPage'),
        ),
    ]
