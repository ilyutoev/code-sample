# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20141027_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'verbose_name': 'сеанс', 'ordering': ['event'], 'verbose_name_plural': 'сеансы'},
        ),
    ]
