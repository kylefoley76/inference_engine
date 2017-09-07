# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archives',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archives_date', models.DateField()),
                ('algorithm', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'archives',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Define3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra', models.CharField(max_length=5, null=True, blank=True)),
                ('type', models.CharField(max_length=5, null=True, blank=True)),
                ('word', models.CharField(max_length=66, null=True, blank=True)),
                ('rel', models.CharField(max_length=4, null=True, blank=True)),
                ('definition', models.CharField(max_length=1000, null=True, blank=True)),
                ('archives', models.ForeignKey(to='inference2.Archives')),
            ],
            options={
                'db_table': 'define3',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('col1', models.CharField(max_length=5, null=True, blank=True)),
                ('col2', models.CharField(max_length=1000, null=True, blank=True)),
                ('col3', models.CharField(max_length=300, null=True, blank=True)),
                ('archives', models.ForeignKey(to='inference2.Archives')),
            ],
            options={
                'db_table': 'input',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='InstructionFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.FileField(upload_to=b'./static/inference2/')),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('col1', models.CharField(max_length=200, null=True, blank=True)),
                ('col2', models.CharField(max_length=1000, null=True, blank=True)),
                ('col3', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
                'db_table': 'output',
                'managed': True,
            },
        ),
    ]
