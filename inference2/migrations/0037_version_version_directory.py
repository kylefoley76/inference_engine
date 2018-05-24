# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0036_auto_20180520_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='version_directory',
            field=models.CharField(max_length=50, default='version1'),
        ),
    ]
