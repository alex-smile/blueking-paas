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
# Generated by Django 2.2.17 on 2020-11-27 02:50

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import paasng.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MigrationProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('legacy_app_id', models.IntegerField()),
                ('status', models.IntegerField(choices=[(0, '默认'), (1, '正在迁移'), (2, '已失败'), (3, '完成迁移'), (4, '正在回滚'), (5, '已回滚'), (6, '正在确认'), (7, '已确认'), (8, '回滚失败')], default=0)),
                ('failed_date', models.DateTimeField(null=True)),
                ('migrated_date', models.DateTimeField(null=True)),
                ('confirmed_date', models.DateTimeField(null=True)),
                ('rollbacked_date', models.DateTimeField(null=True)),
                ('ongoing_migration', jsonfield.fields.JSONField(null=True)),
                ('finished_migrations', jsonfield.fields.JSONField(null=True)),
                ('finished_rollbacks', jsonfield.fields.JSONField(null=True)),
                ('legacy_app_logo', models.CharField(default=None, max_length=64, null=True)),
                ('legacy_app_is_already_online', models.BooleanField(default=True)),
                ('legacy_app_state', models.IntegerField(default=4)),
                ('legacy_app_has_all_deployed', models.BooleanField(default=True)),
                ('app', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
