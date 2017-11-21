# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0029_auto_20170726_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='seocategory',
            name='priority',
            field=models.IntegerField(help_text='Приоритет категории (меньше - лучше)', verbose_name='Приоритет', default=100),
            preserve_default=True,
        ),
    ]
