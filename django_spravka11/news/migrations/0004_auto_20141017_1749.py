# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20141017_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категорию', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'новость', 'verbose_name_plural': 'новости', 'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, max_length=40, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(verbose_name='Название', max_length=100),
        ),
        migrations.AlterField(
            model_name='news',
            name='announcement',
            field=models.CharField(verbose_name='Анонс', max_length=255),
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(verbose_name='Текст новости'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(verbose_name='Заголовок', max_length=200),
        ),
    ]
