# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDashboardModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('module', models.CharField(verbose_name='module', max_length=255)),
                ('app_label', models.CharField(verbose_name='application name', max_length=255, blank=True, null=True)),
                ('user', models.PositiveIntegerField(verbose_name='user')),
                ('column', models.PositiveIntegerField(verbose_name='column')),
                ('order', models.IntegerField(verbose_name='order')),
                ('settings', models.TextField(verbose_name='settings', blank=True, default='')),
                ('children', models.TextField(verbose_name='children', blank=True, default='')),
                ('collapsed', models.BooleanField(verbose_name='collapsed', default=False)),
            ],
            options={
                'verbose_name': 'user dashboard module',
                'verbose_name_plural': 'user dashboard modules',
                'ordering': ('column', 'order'),
            },
        ),
    ]
