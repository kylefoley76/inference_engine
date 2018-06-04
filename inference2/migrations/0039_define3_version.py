# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0038_auto_20180524_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='define3',
            name='version',
            field=models.ForeignKey(blank=True, null=True, to='inference2.Version'),
        ),
    ]
