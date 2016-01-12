# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_auto_20150608_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='heigth',
            field=models.PositiveIntegerField(default=0, blank=True, help_text='Для flash баннеров', verbose_name='Высота'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='banner',
            name='width',
            field=models.PositiveIntegerField(default=0, blank=True, help_text='Для flash баннеров', verbose_name='Ширина'),
            preserve_default=True,
        ),
    ]
