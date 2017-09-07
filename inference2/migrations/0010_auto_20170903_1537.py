# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0009_auto_20170903_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='define3',
            name='definition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='extra',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='rel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='define3',
            name='word',
            field=models.TextField(blank=True, null=True),
        ),
    ]
