# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0010_auto_20170903_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='define3',
            name='col1',
            field=models.TextField(blank=True, null=True),
        ),
    ]
