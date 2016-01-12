# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_auto_20150408_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='blue',
            field=models.BooleanField(help_text='Выделяем синим и ставим на второе метос', verbose_name='На второе место', default=False),
            preserve_default=True,
        ),
    ]
