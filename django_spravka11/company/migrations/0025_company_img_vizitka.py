# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0024_auto_20150621_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='img_vizitka',
            field=models.ImageField(verbose_name='Изображение для шапки сайта визитки', help_text='Ширина картинки 1170 px, высоту регулируйте сами - оптимально от 100-200 px', null=True, blank=True, upload_to='uploads/vizitka', default=None),
            preserve_default=True,
        ),
    ]
