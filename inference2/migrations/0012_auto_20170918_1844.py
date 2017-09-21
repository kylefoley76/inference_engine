# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0011_auto_20170918_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='define3',
            name='def_object',
        ),
        migrations.RemoveField(
            model_name='define3',
            name='subject',
        ),
    ]
