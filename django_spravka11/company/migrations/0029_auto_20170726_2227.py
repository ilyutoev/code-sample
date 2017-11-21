# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0028_company_subdomain'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('ico', models.ImageField(upload_to='company/seocategory', blank=True, verbose_name='Иконка', null=True, default=None)),
                ('article', models.TextField(blank=True, verbose_name='Статья', null=True, default=None)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', null=True, blank=True, to='company.SeoCategory')),
            ],
            options={
                'verbose_name_plural': 'seo рубрики',
                'verbose_name': 'seo рубрику',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='seo_category',
            field=models.ManyToManyField(to='company.SeoCategory', verbose_name='seo рубрики'),
            preserve_default=True,
        ),
    ]
