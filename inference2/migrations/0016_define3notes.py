# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0015_algorithm_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Define3Notes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('notes', models.TextField()),
            ],
        ),
    ]
