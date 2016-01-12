# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_auto_20150520_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='article',
            field=models.TextField(verbose_name='Статья', null=True, default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='banner',
            field=models.ImageField(verbose_name='Рекламный модуль', null=True, default=None, blank=True, upload_to='uploads/module'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(verbose_name='Логотип', null=True, default=None, blank=True, upload_to='uploads/logo'),
            preserve_default=True,
        ),
    ]
