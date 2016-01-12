# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20150302_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyimage',
            name='image',
            field=models.ImageField(verbose_name='Изображение', upload_to='company/news/%Y/%m/%d', null=True, default=None),
            preserve_default=True,
        ),
    ]
