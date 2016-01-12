# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0025_company_img_vizitka'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='recomendation_text',
            field=models.CharField(max_length=255, blank=True, verbose_name='Текст рекомендации для главной'),
            preserve_default=True,
        ),
    ]
