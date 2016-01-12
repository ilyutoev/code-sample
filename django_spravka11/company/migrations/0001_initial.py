# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'адрес компании',
                'verbose_name_plural': 'адреса компаний',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', to='company.Category', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'рубрику',
                'verbose_name_plural': 'рубрики',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='Город')),
                ('priority', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name': 'город',
                'verbose_name_plural': 'города',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название компании')),
                ('website', models.URLField(verbose_name='Адрес сайта')),
                ('email', models.EmailField(max_length=75, verbose_name='E-mail')),
                ('skype', models.CharField(max_length=50, verbose_name='Skype')),
                ('icq', models.CharField(max_length=50, verbose_name='ICQ')),
                ('dateupdate', models.DateField(verbose_name='Дата последнего обновления')),
            ],
            options={
                'verbose_name': 'компанию',
                'verbose_name_plural': 'компании',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.ForeignKey(to='company.Address')),
            ],
            options={
                'verbose_name': 'номер телефона компании',
                'verbose_name_plural': 'номера телефонов компаний',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='category',
            field=models.ManyToManyField(to='company.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(to='company.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.ForeignKey(to='company.Company'),
            preserve_default=True,
        ),
    ]
