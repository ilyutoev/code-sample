# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20150227_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('announcement', models.CharField(max_length=255, verbose_name='Анонс')),
                ('text', models.TextField(verbose_name='Текст новости')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации')),
                ('photo', models.ImageField(null=True, default=None, upload_to='news/%Y/%m/%d')),
                ('company', models.ForeignKey(to='company.Company', verbose_name='компания')),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name_plural': 'новости компаний',
                'verbose_name': 'новость компании',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='companyimage',
            options={'verbose_name_plural': 'изображения', 'verbose_name': 'изображение'},
        ),
        migrations.AlterField(
            model_name='address',
            name='category',
            field=models.ManyToManyField(to='company.Category', verbose_name='рубрики'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(to='company.City', verbose_name='город'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='company',
            field=models.ForeignKey(to='company.Company', verbose_name='компания'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='banner',
            field=models.ImageField(null=True, default=None, blank=True, verbose_name='Рекламный модуль', upload_to='company/module'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(null=True, default=None, blank=True, verbose_name='Логотип', upload_to='company/logo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyimage',
            name='company',
            field=models.ForeignKey(to='company.Company', verbose_name='компания'),
            preserve_default=True,
        ),
    ]
