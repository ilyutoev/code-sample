# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventPlace',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200, verbose_name='Название места')),
                ('description', models.TextField(verbose_name='Описание места')),
            ],
            options={
                'verbose_name_plural': 'места',
                'verbose_name': 'место',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='Название мероприятия')),
                ('description', models.TextField(verbose_name='Описание мероприятия')),
            ],
            options={
                'verbose_name_plural': 'события',
                'verbose_name': 'событие',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=30, verbose_name='Тип мероприятия')),
            ],
            options={
                'verbose_name_plural': 'типы мероприятий',
                'verbose_name': 'тип мероприятия',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField(verbose_name='Дата проведения мероприятия')),
                ('time', models.TimeField(verbose_name='Время проведения')),
                ('price', models.CharField(max_length=20, verbose_name='Цена')),
                ('event', models.ForeignKey(to='events.Events')),
            ],
            options={
                'verbose_name_plural': 'сеансы',
                'verbose_name': 'сеанс',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='events',
            name='event_type',
            field=models.ForeignKey(to='events.EventType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='events',
            name='place',
            field=models.ForeignKey(to='events.EventPlace'),
            preserve_default=True,
        ),
    ]
