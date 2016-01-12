# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0003_auto_20150608_1331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='heigth',
            new_name='height',
        ),
    ]
