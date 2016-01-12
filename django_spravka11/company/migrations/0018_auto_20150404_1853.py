# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_auto_20150403_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='holiday',
            field=models.BooleanField(default=False, verbose_name='Выходной'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='lunchtimebegin',
            field=models.TimeField(blank=True, null=True, verbose_name='Начало обеда', default='00:00:00'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='lunchtimeend',
            field=models.TimeField(blank=True, null=True, verbose_name='Конец обеда', default='00:00:00'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='worktimebegin',
            field=models.TimeField(blank=True, null=True, verbose_name='Начало работы', default='00:00:00'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='worktimeend',
            field=models.TimeField(blank=True, null=True, verbose_name='Конец работы', default='00:00:00'),
            preserve_default=True,
        ),
    ]
