# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20141017_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='photo',
            field=models.ImageField(upload_to='images/', null=True, default=None),
            preserve_default=True,
        ),
    ]
