# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0008_auto_20170903_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='define3',
            name='object_col',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='define3',
            name='subject',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='define3',
            name='superscript',
            field=models.TextField(blank=True, null=True),
        ),
    ]
