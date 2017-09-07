# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0006_auto_20170524_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='data',
            field=models.FileField(upload_to='./inference2/Proofs/'),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='color_type',
            field=models.CharField(choices=[('red', 'red'), ('green', 'green'), ('blue', 'blue'), ('white', 'white')], default='white', max_length=10),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='data',
            field=models.FileField(upload_to='./static/inference2/'),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='file_type',
            field=models.CharField(choices=[('0', 'instruction'), ('1', 'downloadable_file')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='instructionfile',
            name='name',
            field=models.CharField(default='name', max_length=100),
        ),
    ]
