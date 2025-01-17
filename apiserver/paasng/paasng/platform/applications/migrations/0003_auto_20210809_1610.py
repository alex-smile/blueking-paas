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
# Generated by Django 2.2.17 on 2021-08-09 08:10

from django.db import migrations, models
import paasng.platform.applications.constants


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20201127_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='app_type',
        ),
        migrations.RemoveField(
            model_name='application',
            name='source_init_template',
        ),
        migrations.RemoveField(
            model_name='application',
            name='source_repo_id',
        ),
        migrations.RemoveField(
            model_name='application',
            name='source_type',
        ),
        migrations.AddField(
            model_name='application',
            name='is_smart_app',
            field=models.BooleanField(default=False, verbose_name='是否为 S-Mart 应用'),
        ),
        migrations.AddField(
            model_name='application',
            name='type',
            field=models.CharField(default='default', max_length=16, verbose_name='应用类型'),
        ),
    ]
