# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150210_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='ganre',
            field=models.CharField(verbose_name='Жанр', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
