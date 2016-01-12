# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_auto_20150327_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='icq',
        ),
        migrations.RemoveField(
            model_name='company',
            name='skype',
        ),
        migrations.AddField(
            model_name='company',
            name='vkontakte',
            field=models.URLField(blank=True, verbose_name='Страница ВКонтакте'),
            preserve_default=True,
        ),
    ]
