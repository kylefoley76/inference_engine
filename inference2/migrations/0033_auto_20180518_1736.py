# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0032_remove_version_version_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionitem',
            name='code_file_name',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='versionitem',
            name='version',
            field=models.ForeignKey(blank=True, null=True, to='inference2.Version'),
        ),
    ]
