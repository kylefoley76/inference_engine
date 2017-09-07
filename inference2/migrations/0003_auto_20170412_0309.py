# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inference2', '0002_output_archives'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.FileField(upload_to=b'./inference2/Proofs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='output',
            options={'managed': True, 'verbose_name': 'Argument', 'verbose_name_plural': 'Arguments'},
        ),
        migrations.AddField(
            model_name='output',
            name='archives',
            field=models.ForeignKey(default=1, to='inference2.Archives'),
            preserve_default=False,
        ),
    ]
