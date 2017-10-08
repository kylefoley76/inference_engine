# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0021_testeddictionary'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithm',
            name='test_machine',
            field=models.FileField(blank=True, null=True, default=None, upload_to='./inference2/Proofs/'),
        ),
    ]
