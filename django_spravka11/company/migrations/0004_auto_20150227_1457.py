# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20150227_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(verbose_name='Изображение', upload_to='company/images/%Y/%m/%d', default=None, null=True)),
                ('company', models.ForeignKey(to='company.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='company',
            name='banner',
            field=models.ImageField(verbose_name='Рекламный модуль', upload_to='company/module', default=None, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(verbose_name='Логотип', upload_to='company/logo', default=None, null=True),
            preserve_default=True,
        ),
    ]
