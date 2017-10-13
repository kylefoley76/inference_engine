# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0025_profile_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, default=None, upload_to='img'),
        ),
    ]
