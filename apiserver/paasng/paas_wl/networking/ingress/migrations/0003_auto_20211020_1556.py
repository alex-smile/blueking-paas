# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

    http://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and
limitations under the License.

We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""
# Generated by Django 2.2.17 on 2021-10-20 07:56
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0002_appsubpath'),
    ]
    # 由于架构调整, 该 DjangoApp 从 services 重命名为 ingress
    # 为避免 migrations 重复执行, 使用 replaces 声明该 migration 的历史名称
    if getattr(settings, "WL_APP_SERVICES_RENAMED", False):
        replaces = [
            ("services", "0003_auto_20211020_1556"),
        ]

    operations = [
        migrations.AddField(
            model_name='appdomain',
            name='path_prefix',
            field=models.CharField(default='/', help_text='the accessable path for current domain', max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='appdomain',
            unique_together={('region', 'host', 'path_prefix')},
        ),
    ]