# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='heigth',
            field=models.PositiveIntegerField(default=0, help_text='Для flash баннеров', verbose_name='Высота', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='width',
            field=models.PositiveIntegerField(default=0, help_text='Для flash баннеров', verbose_name='Ширина', blank=True),
            preserve_default=False,
        ),
    ]
