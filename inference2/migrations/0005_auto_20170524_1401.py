# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0004_algorithm_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionfile',
            name='color_type',
            field=models.CharField(default=b'green', max_length=10, choices=[(b'red', b'instruction'), (b'green', b'sophomore'), (b'glue', b'junior')]),
        ),
        migrations.AddField(
            model_name='instructionfile',
            name='file_type',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'instruction'), (b'1', b'sophomore'), (b'2', b'junior'), (b'3', b'senior')]),
        ),
    ]
