# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(blank=True, verbose_name='Title', max_length=255)),
                ('alt', models.CharField(verbose_name='Alt', max_length=255)),
                ('text', models.TextField(blank=True, verbose_name='Text', null=True)),
                ('img', models.FileField(blank=True, verbose_name='Image', null=True, upload_to='banners')),
                ('url', models.CharField(verbose_name='URL', max_length=1024)),
                ('sort', models.PositiveSmallIntegerField(verbose_name='Sort', default=500)),
                ('html', models.BooleanField(verbose_name='Is HTML?', default=False)),
                ('flash', models.BooleanField(verbose_name='Is Flash?', default=False)),
                ('public', models.BooleanField(verbose_name='Public', default=True)),
                ('created_at', models.DateTimeField(verbose_name='Created At', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Updated At', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Banners',
                'verbose_name': 'Banner',
                'ordering': ['sort'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BannerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', unique=True)),
                ('public', models.BooleanField(verbose_name='Public', default=True)),
                ('created_at', models.DateTimeField(verbose_name='Created At', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Updated At', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Banner Groups',
                'verbose_name': 'Banner Group',
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField(verbose_name='Clicked At', auto_now_add=True)),
                ('ip', models.IPAddressField(blank=True, verbose_name='IP', null=True)),
                ('user_agent', models.CharField(blank=True, verbose_name='User Agent', null=True, max_length=1024)),
                ('page', models.URLField(blank=True, verbose_name='Page', null=True)),
                ('key', models.CharField(blank=True, verbose_name='User Agent', null=True, max_length=32)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'impressions'), (1, 'view'), (2, 'click')], verbose_name='Type', max_length=1, default=0)),
                ('banner', models.ForeignKey(related_name='banner_logs', to='banners.Banner')),
                ('group', models.ForeignKey(verbose_name='Group', blank=True, to='banners.BannerGroup', related_name='group_logs')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='users')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date', models.DateField(verbose_name='Data')),
                ('view', models.PositiveIntegerField(verbose_name='Views')),
                ('click', models.PositiveIntegerField(verbose_name='Clicks')),
                ('unique_click', models.PositiveIntegerField(blank=True, verbose_name='Unique Views', null=True)),
                ('unique_view', models.PositiveIntegerField(verbose_name='Unique Clicks')),
                ('banner', models.ForeignKey(verbose_name='Banner', blank=True, to='banners.Banner', related_name='banner_stat')),
                ('group', models.ForeignKey(verbose_name='Group', blank=True, to='banners.BannerGroup', related_name='group_stat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='banner',
            name='group',
            field=models.ForeignKey(verbose_name='Group', to='banners.BannerGroup', related_name='banners'),
            preserve_default=True,
        ),
    ]
