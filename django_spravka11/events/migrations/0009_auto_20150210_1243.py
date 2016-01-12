# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150210_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='limit_year',
            field=models.CharField(max_length=10, verbose_name='Возрастное ограничение', blank=True),
            preserve_default=True,
        ),
    ]
