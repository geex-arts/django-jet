# Generated by Django 2.2 on 2019-04-23 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jet', '0002_delete_userdashboardmodule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='user',
            field=models.CharField(max_length=255, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='pinnedapplication',
            name='user',
            field=models.CharField(max_length=255, verbose_name='user'),
        ),
    ]
