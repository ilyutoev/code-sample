# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20150303_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Название товара/услуги', max_length=200)),
                ('text', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(verbose_name='Изображение', upload_to='company/service/%Y/%m/%d', null=True, default=None)),
                ('company', models.ForeignKey(verbose_name='компания', to='company.Company')),
            ],
            options={
                'verbose_name': 'товар/услуга',
                'verbose_name_plural': 'товара/услуги',
            },
            bases=(models.Model,),
        ),
    ]
