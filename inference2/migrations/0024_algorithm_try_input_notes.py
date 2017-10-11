# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0023_archives_test_machine'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithm',
            name='try_input_notes',
            field=models.TextField(blank=True, null=True, default=''),
        ),
    ]
