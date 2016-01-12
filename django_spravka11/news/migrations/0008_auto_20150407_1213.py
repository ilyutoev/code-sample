# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20141031_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=filebrowser.fields.FileBrowseField(default=None, max_length=200, null=True),
            preserve_default=True,
        ),
    ]
