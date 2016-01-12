# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20150325_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='yellow',
            field=models.BooleanField(default=False, verbose_name='На первое место', help_text='Выделяем желтым и добавляем выоский приоритет'),
            preserve_default=True,
        ),
    ]
