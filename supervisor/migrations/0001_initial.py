# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-08 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='节点名')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('host', models.CharField(max_length=128, verbose_name='IP或域名')),
                ('port', models.IntegerField(verbose_name='端口')),
                ('username', models.CharField(max_length=128, null=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, null=True, verbose_name='密码')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'ordering': ['-c_time'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='node',
            unique_together=set([('host', 'port')]),
        ),
    ]
