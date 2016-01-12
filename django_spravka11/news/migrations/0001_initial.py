# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('announcement', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
