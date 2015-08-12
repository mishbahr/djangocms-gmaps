# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangocms_gmaps.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gmaps', '0002_filer_fk_on_delete_set_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='plugin_template',
            field=models.CharField(
                default=settings.DJANGOCMS_GMAPS_TEMPLATES[0][0],
                max_length=255, verbose_name='Template',
                choices=settings.DJANGOCMS_GMAPS_TEMPLATES),
        ),
    ]
