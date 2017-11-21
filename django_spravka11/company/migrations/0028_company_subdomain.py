# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0027_auto_20150909_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='subdomain',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Поддомен сайта визитки', help_text='Поддомен для сайта визитки. Только на английском и без пробелов. Возможен символ дефиса.'),
            preserve_default=True,
        ),
    ]
