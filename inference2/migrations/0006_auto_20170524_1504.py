# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0005_auto_20170524_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionfile',
            name='name',
            field=models.CharField(default=b'name', max_length=100),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='color_type',
            field=models.CharField(default=b'white', max_length=10, choices=[(b'red', b'red'), (b'green', b'green'), (b'blue', b'blue'), (b'white', b'white')]),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='file_type',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'instruction'), (b'1', b'downloadable_file')]),
        ),
    ]
