# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 15:53
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20160520_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='文章内容'),
        ),
    ]
