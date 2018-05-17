# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0030_version_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
