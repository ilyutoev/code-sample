# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20150407_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(null=True, upload_to='news/%Y/%m/%d', default=None),
            preserve_default=True,
        ),
    ]
