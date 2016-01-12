# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='priority',
            field=models.IntegerField(verbose_name='Рекламная позиция', default=0),
            preserve_default=True,
        ),
    ]
