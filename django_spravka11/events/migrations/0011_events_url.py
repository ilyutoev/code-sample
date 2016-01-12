# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150302_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='url',
            field=models.CharField(blank=True, null=True, verbose_name='Ссылка с парсинга', max_length=255),
            preserve_default=True,
        ),
    ]
