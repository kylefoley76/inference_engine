# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0029_auto_20180517_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
