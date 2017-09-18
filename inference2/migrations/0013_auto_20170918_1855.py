# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0012_auto_20170918_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='define3',
            name='def_object',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='define3',
            name='subject',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
    ]
