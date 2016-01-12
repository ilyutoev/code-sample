# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20141027_1946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'verbose_name_plural': 'сеансы', 'ordering': ['event', 'place', 'date', 'time'], 'verbose_name': 'сеанс'},
        ),
    ]
