# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('user', models.PositiveIntegerField(verbose_name='user')),
                ('date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
            ],
            options={
                'ordering': ('date_add',),
                'verbose_name': 'bookmark',
                'verbose_name_plural': 'bookmarks',
            },
        ),
        migrations.CreateModel(
            name='PinnedApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=255, verbose_name='application name')),
                ('user', models.PositiveIntegerField(verbose_name='user')),
                ('date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
            ],
            options={
                'ordering': ('date_add',),
                'verbose_name': 'pinned application',
                'verbose_name_plural': 'pinned applications',
            },
        ),
        migrations.CreateModel(
            name='UserDashboardModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('module', models.CharField(max_length=255, verbose_name='module')),
                ('app_label', models.CharField(max_length=255, null=True, verbose_name='application name', blank=True)),
                ('user', models.PositiveIntegerField(verbose_name='user')),
                ('column', models.PositiveIntegerField(verbose_name='column')),
                ('order', models.IntegerField(verbose_name='order')),
                ('settings', models.TextField(default=b'', verbose_name='settings', blank=True)),
                ('children', models.TextField(default=b'', verbose_name='children', blank=True)),
                ('collapsed', models.BooleanField(default=False, verbose_name='collapsed')),
            ],
            options={
                'ordering': ('column', 'order'),
                'verbose_name': 'user dashboard module',
                'verbose_name_plural': 'user dashboard modules',
            },
        ),
    ]
