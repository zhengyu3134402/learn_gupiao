# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-01-27 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yingyong1', '0005_auto_20190127_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gupiao',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
