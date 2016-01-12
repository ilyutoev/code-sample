# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_company_yellow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('day', models.IntegerField(verbose_name='День недели', choices=[(1, 'Пн'), (2, 'Вт'), (3, 'Ср'), (4, 'Чт'), (5, 'Пт'), (6, 'Сб'), (7, 'Вс')])),
                ('worktimebegin', models.TimeField(verbose_name='Начало работы')),
                ('worktimeend', models.TimeField(verbose_name='Конец работы')),
                ('holiday', models.IntegerField(default=0, verbose_name='Выходной')),
                ('lunchtimebegin', models.TimeField(verbose_name='Начало обеда')),
                ('lunchtimeend', models.TimeField(verbose_name='Конец обеда')),
                ('address', models.ForeignKey(to='company.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='company',
            name='recomendation',
            field=models.BooleanField(default=False, verbose_name='Рекомендуем', help_text='Вывод на главную страницу в блок "Рекомендуем", бирка "Рекомендуем"'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyimage',
            name='image',
            field=models.ImageField(default=None, null=True, verbose_name='Изображение', upload_to='company/images/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
