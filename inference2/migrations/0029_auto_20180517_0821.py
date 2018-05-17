# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0028_versionitem_item_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='versionitem',
            old_name='item_choices',
            new_name='item_category',
        ),
    ]
