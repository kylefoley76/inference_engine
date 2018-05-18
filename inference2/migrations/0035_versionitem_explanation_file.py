# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0034_versionitem_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionitem',
            name='explanation_file',
            field=models.FileField(blank=True, null=True, upload_to='./static/inference2/'),
        ),
    ]
