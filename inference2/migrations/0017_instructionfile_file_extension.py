# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0016_define3notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionfile',
            name='file_extension',
            field=models.CharField(max_length=20, default='PDF', choices=[('pdf', 'Pdf'), ('csv', 'Csv')]),
        ),
    ]
