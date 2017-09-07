# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0007_auto_20170818_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='archives',
            name='name',
            field=models.CharField(max_length=300, default='September 2017'),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='file_type',
            field=models.CharField(max_length=1, default='0', choices=[('0', 'rules_in_depth'), ('1', 'downloadable_file'), ('2', 'rules_in_brief')]),
        ),
    ]
