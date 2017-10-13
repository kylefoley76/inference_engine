# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0024_algorithm_try_input_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, default=None, upload_to=''),
        ),
    ]
