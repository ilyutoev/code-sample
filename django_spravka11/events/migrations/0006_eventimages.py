# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20141027_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, null=True, upload_to='events/%Y/%m/%d', verbose_name='Изображения')),
                ('event', models.ForeignKey(related_name='изображения', to='events.Events')),
            ],
            options={
                'verbose_name': 'изображение для события',
                'verbose_name_plural': 'изображения для событий',
            },
            bases=(models.Model,),
        ),
    ]
