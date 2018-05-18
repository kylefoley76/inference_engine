# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0031_auto_20180517_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='version_items',
        ),
    ]
