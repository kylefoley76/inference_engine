# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0020_auto_20171004_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestedDictionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('extra', models.CharField(max_length=1000, blank=True, null=True)),
                ('type', models.CharField(max_length=1000, blank=True, null=True)),
                ('word', models.CharField(max_length=1000, blank=True, null=True)),
                ('rel', models.CharField(max_length=1000, blank=True, null=True)),
                ('definition', models.CharField(max_length=1000, blank=True, null=True)),
                ('subject', models.CharField(max_length=1000, blank=True, null=True)),
                ('def_object', models.CharField(max_length=1000, blank=True, null=True)),
                ('archives', models.ForeignKey(to='inference2.Archives')),
            ],
            options={
                'db_table': 'testeddict',
                'managed': True,
            },
        ),
    ]
