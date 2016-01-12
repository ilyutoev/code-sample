# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_auto_20150508_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.CharField(verbose_name='Номер телефона', max_length=200),
            preserve_default=True,
        ),
    ]
