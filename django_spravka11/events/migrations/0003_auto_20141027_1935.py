# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141025_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'verbose_name': 'сеанс', 'verbose_name_plural': 'сеансы', 'ordering': ['date']},
        ),
    ]
