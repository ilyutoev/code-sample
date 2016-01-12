# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='place',
        ),
        migrations.AddField(
            model_name='session',
            name='place',
            field=models.ForeignKey(to='events.EventPlace', default=None),
            preserve_default=True,
        ),
    ]
