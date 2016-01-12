# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0018_auto_20150404_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='article',
            field=models.TextField(verbose_name='Статья о компании', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='keywords',
            field=models.CharField(max_length=255, verbose_name='Ключевые слова', blank=True),
            preserve_default=True,
        ),
    ]
