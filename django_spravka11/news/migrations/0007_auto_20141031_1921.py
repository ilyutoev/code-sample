# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20141031_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(null=True, default=None, upload_to='news/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
