# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0022_algorithm_test_machine'),
    ]

    operations = [
        migrations.AddField(
            model_name='archives',
            name='test_machine',
            field=models.CharField(max_length=300, default=''),
        ),
    ]
