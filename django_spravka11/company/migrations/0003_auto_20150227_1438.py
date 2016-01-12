# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_company_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='banner',
            field=models.ImageField(upload_to='compnay/logo/%Y/%m/%d', verbose_name='Рекламный модуль', null=True, default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='compnay/logo/%Y/%m/%d', verbose_name='Логотип', null=True, default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, verbose_name='E-mail', max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='icq',
            field=models.CharField(blank=True, verbose_name='ICQ', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='skype',
            field=models.CharField(blank=True, verbose_name='Skype', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(blank=True, verbose_name='Адрес сайта'),
            preserve_default=True,
        ),
    ]
