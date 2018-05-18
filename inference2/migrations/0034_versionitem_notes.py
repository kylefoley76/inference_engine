# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0033_auto_20180518_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionitem',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]
