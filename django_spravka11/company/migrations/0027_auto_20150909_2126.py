# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0026_company_recomendation_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='recomendation_text',
            new_name='recomendationtext',
        ),
    ]
