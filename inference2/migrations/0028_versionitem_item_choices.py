# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0027_auto_20180517_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='versionitem',
            name='item_choices',
            field=models.CharField(max_length=50, default='dictionary', choices=[('downloadable_dictionary', 'Download Dict'), ('explanation', 'Explanation'), ('alphabetic', 'Alphabetical Word List'), ('categorize', 'Categorized Word List'), ('dictionary', 'Dictionary')]),
        ),
    ]
