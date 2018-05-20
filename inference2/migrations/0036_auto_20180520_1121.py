# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0035_versionitem_explanation_file'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='versionitem',
            unique_together=set([('version', 'item_category')]),
        ),
    ]
