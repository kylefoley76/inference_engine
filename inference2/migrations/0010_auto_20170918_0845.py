# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0009_auto_20170916_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='define3',
            name='extra',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='rel',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='type',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='word',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
    ]
