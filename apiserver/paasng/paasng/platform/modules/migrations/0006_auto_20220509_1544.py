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
# Generated by Django 3.2.12 on 2022-05-09 07:44

from django.db import migrations, models
import paasng.platform.modules.models.deploy_config


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0005_deployconfig'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appbuildpack',
            old_name='description',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='appbuildpack',
            old_name='display_name',
            new_name='display_name_zh_cn',
        ),
        migrations.RenameField(
            model_name='appslugbuilder',
            old_name='description',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='appslugbuilder',
            old_name='display_name',
            new_name='display_name_zh_cn',
        ),
        migrations.RenameField(
            model_name='appslugrunner',
            old_name='description',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='appslugrunner',
            old_name='display_name',
            new_name='display_name_zh_cn',
        ),
        migrations.AddField(
            model_name='appbuildpack',
            name='description_en',
            field=models.CharField(blank=True, max_length=1024, verbose_name='描述'),
        ),
        migrations.AddField(
            model_name='appbuildpack',
            name='display_name_en',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='展示名称'),
        ),
        migrations.AddField(
            model_name='appslugbuilder',
            name='description_en',
            field=models.CharField(blank=True, max_length=1024, verbose_name='描述'),
        ),
        migrations.AddField(
            model_name='appslugbuilder',
            name='display_name_en',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='展示名称'),
        ),
        migrations.AddField(
            model_name='appslugrunner',
            name='description_en',
            field=models.CharField(blank=True, max_length=1024, verbose_name='描述'),
        ),
        migrations.AddField(
            model_name='appslugrunner',
            name='display_name_en',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='展示名称'),
        ),
        migrations.AlterField(
            model_name='appslugbuilder',
            name='is_default',
            field=models.BooleanField(default=False, null=True, verbose_name='是否为默认运行时'),
        ),
        migrations.AlterField(
            model_name='appslugrunner',
            name='is_default',
            field=models.BooleanField(default=False, null=True, verbose_name='是否为默认运行时'),
        ),
        migrations.AlterField(
            model_name='deployconfig',
            name='hooks',
            field=paasng.platform.modules.models.deploy_config.HookListField(default=paasng.platform.modules.models.deploy_config.HookList, help_text='部署钩子'),
        ),
    ]
