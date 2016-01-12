# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150210_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='poster',
            field=models.ImageField(null=True, default=None, blank=True, verbose_name='Постер', upload_to='events/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
