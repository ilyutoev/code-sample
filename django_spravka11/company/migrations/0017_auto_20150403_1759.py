# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_category_ico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='counter',
            field=models.IntegerField(default=1, verbose_name='Счетчик посещений'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='priority',
            field=models.IntegerField(default=1, help_text='Приоритет компании в зависимости от купленной рекламы (больше - лучше)', verbose_name='Приоритет'),
            preserve_default=True,
        ),
    ]
