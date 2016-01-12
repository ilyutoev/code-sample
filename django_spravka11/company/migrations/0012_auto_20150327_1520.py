# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_auto_20150327_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timetable',
            options={'verbose_name_plural': 'Время работы', 'verbose_name': 'Время работы'},
        ),
        migrations.AlterField(
            model_name='timetable',
            name='lunchtimebegin',
            field=models.TimeField(null=True, blank=True, verbose_name='Начало обеда'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='lunchtimeend',
            field=models.TimeField(null=True, blank=True, verbose_name='Конец обеда'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='worktimebegin',
            field=models.TimeField(null=True, blank=True, verbose_name='Начало работы'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='worktimeend',
            field=models.TimeField(null=True, blank=True, verbose_name='Конец работы'),
            preserve_default=True,
        ),
    ]
