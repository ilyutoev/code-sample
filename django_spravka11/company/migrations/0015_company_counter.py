# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_companypage'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='counter',
            field=models.IntegerField(verbose_name='Счетчик посещений', default=0),
            preserve_default=True,
        ),
    ]
