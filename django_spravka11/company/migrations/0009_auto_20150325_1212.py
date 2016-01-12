# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Адрес компании', 'verbose_name_plural': 'Адреса компании'},
        ),
        migrations.AlterModelOptions(
            name='companyservice',
            options={'verbose_name': 'товар/услуга', 'verbose_name_plural': 'товары/услуги'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='index_logo',
        ),
        migrations.AddField(
            model_name='company',
            name='recomendation',
            field=models.BooleanField(help_text='Вывод на главную страницу, бирка "Рекомендуем"', verbose_name='Рекомендуем', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='vizitka',
            field=models.BooleanField(verbose_name='Сайт визитка', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='priority',
            field=models.IntegerField(help_text='Приоритет компании в зависимости от купленной рекламы (больше - лучше)', verbose_name='Приоритет', default=0),
            preserve_default=True,
        ),
    ]
