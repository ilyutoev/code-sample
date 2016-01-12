# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='ganre',
            field=models.TextField(blank=True, verbose_name='Жанр'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='events',
            name='limit_year',
            field=models.TextField(blank=True, verbose_name='Возрастное ограничение'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='events',
            name='poster',
            field=models.ImageField(upload_to='events/%Y/%m/%d', verbose_name='Постер', default=None, null=True),
            preserve_default=True,
        ),
    ]
