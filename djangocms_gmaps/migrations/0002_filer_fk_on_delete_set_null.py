# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gmaps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='marker_icon',
            field=filer.fields.image.FilerImageField(related_name='djangocms_map_marker_icons', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Marker Icon', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='photo',
            field=filer.fields.image.FilerImageField(related_name='djangocms_map_locations', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Location Photo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
    ]
