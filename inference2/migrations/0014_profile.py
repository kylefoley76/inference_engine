# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0013_auto_20170918_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('about', models.TextField()),
                ('hobbies', models.CharField(max_length=500, blank=True, null=True)),
                ('skills', models.CharField(max_length=500, blank=True, null=True)),
                ('facebook', models.CharField(max_length=200, blank=True, null=True)),
                ('twitter', models.CharField(max_length=200, blank=True, null=True)),
                ('instagram', models.CharField(max_length=200, blank=True, null=True)),
            ],
        ),
    ]
