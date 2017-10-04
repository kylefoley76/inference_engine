# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0019_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name_plural': 'Settings'},
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='file_type',
            field=models.CharField(max_length=1, default='0', choices=[('0', 'rules_in_depth'), ('1', 'download_dictionary'), ('2', 'rules_in_brief'), ('3', 'arguments')]),
        ),
    ]
