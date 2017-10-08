# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0008_auto_20170916_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='dictionary',
            field=models.FileField(blank=True, null=True, default=None,upload_to='./inference2/Proofs/'),
        ),
    ]
