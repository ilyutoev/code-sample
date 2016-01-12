# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_auto_20150328_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(verbose_name='Заголовок страницы', max_length=200)),
                ('slug', models.SlugField(verbose_name='Ссылка страницы', help_text='Латинские буквы, нижнее подчеркивание')),
                ('text', models.TextField(verbose_name='Наполнение страницы')),
                ('ismemu', models.BooleanField(default=False, verbose_name='Вывести в меню')),
                ('title_menu', models.CharField(blank=True, verbose_name='Заголовок для меню', max_length=200)),
                ('priority', models.IntegerField(help_text='Больше - лучше', default=0, verbose_name='Приоритет в меню')),
                ('company', models.ForeignKey(to='company.Company', verbose_name='компания')),
            ],
            options={
                'verbose_name_plural': 'Страницы сайта визитки',
                'verbose_name': 'Страница сайта визитки',
            },
            bases=(models.Model,),
        ),
    ]
