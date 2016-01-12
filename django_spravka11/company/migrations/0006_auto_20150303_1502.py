# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20150302_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='index_logo',
            field=models.BooleanField(default=False, verbose_name='Вывести на главную в рекомендуемые'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyimage',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='company/news/%Y/%m/%d', verbose_name='Изображение'),
            preserve_default=True,
        ),
    ]
