# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making
蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
Copyright (C) 2017-2022THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.

We undertake not to change the open source license (MIT license) applicable

to the current version of the project delivered to anyone in the future.
"""
# Generated by Django 2.2.17 on 2022-01-12 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_move_app_logo'),
        ('bk_plugins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bkpluginprofile',
            name='contact',
            field=models.CharField(blank=True, help_text='使用 ; 分隔的用户名', max_length=128, null=True, verbose_name='联系人'),
        ),
        migrations.CreateModel(
            name='BkPluginDistributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='插件使用方名称', max_length=32, unique=True, verbose_name='名称')),
                ('code_name', models.CharField(help_text='插件使用方的英文代号，可替代主键使用', max_length=32, unique=True, verbose_name='英文代号')),
                ('bk_app_code', models.CharField(help_text='插件使用方所绑定的蓝鲸应用代号', max_length=20, unique=True, verbose_name='蓝鲸应用代号')),
                ('introduction', models.CharField(blank=True, max_length=512, null=True, verbose_name='使用方简介')),
                ('plugins', models.ManyToManyField(db_constraint=False, related_name='distributors', to='applications.Application')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
