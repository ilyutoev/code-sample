# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0015_company_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='ico',
            field=models.ImageField(default=None, null=True, upload_to='company/category', blank=True, verbose_name='Иконка'),
            preserve_default=True,
        ),
    ]
