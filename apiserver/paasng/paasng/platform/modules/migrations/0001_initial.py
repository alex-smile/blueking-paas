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
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppBuildPack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('language', models.CharField(max_length=32, verbose_name='编程语言')),
                ('type', models.CharField(choices=[('git', 'git'), ('tar', 'tar')], max_length=32, verbose_name='引用类型')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('display_name', models.CharField(blank=True, default='', max_length=64, verbose_name='展示名称')),
                ('address', models.CharField(max_length=2048, verbose_name='地址')),
                ('version', models.CharField(max_length=32, verbose_name='版本')),
                ('environments', jsonfield.fields.JSONField(blank=True, default=dict, verbose_name='环境变量')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='是否隐藏')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('name', models.CharField(max_length=20, verbose_name='模块名称')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否为默认模块')),
                ('language', models.CharField(max_length=32, verbose_name='编程语言')),
                ('source_init_template', models.CharField(max_length=32, verbose_name='初始化模板类型')),
                ('source_origin', models.SmallIntegerField(null=True, verbose_name='源码来源')),
                ('source_type', models.CharField(max_length=16, null=True, verbose_name='源码托管类型')),
                ('source_repo_id', models.IntegerField(null=True, verbose_name='源码 ID')),
                ('exposed_url_type', models.IntegerField(null=True, verbose_name='访问 URL 版本')),
                ('last_deployed_date', models.DateTimeField(null=True, verbose_name='最近部署时间')),
                ('creator', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='applications.Application')),
            ],
            options={
                'unique_together': {('application', 'name')},
            },
        ),
        migrations.CreateModel(
            name='AppSlugRunner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('display_name', models.CharField(blank=True, default='', max_length=64, verbose_name='展示名称')),
                ('image', models.CharField(max_length=256, verbose_name='镜像')),
                ('tag', models.CharField(max_length=32, verbose_name='标签')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='是否隐藏')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
                ('environments', jsonfield.fields.JSONField(blank=True, default=dict, verbose_name='环境变量')),
                ('modules', models.ManyToManyField(related_name='slugrunners', to='modules.Module')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppSlugBuilder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('display_name', models.CharField(blank=True, default='', max_length=64, verbose_name='展示名称')),
                ('image', models.CharField(max_length=256, verbose_name='镜像')),
                ('tag', models.CharField(max_length=32, verbose_name='标签')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='是否隐藏')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
                ('environments', jsonfield.fields.JSONField(blank=True, default=dict, verbose_name='环境变量')),
                ('buildpacks', models.ManyToManyField(related_name='slugbuilders', to='modules.AppBuildPack')),
                ('modules', models.ManyToManyField(related_name='slugbuilders', to='modules.Module')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='appbuildpack',
            name='modules',
            field=models.ManyToManyField(related_name='buildpacks', to='modules.Module'),
        ),
    ]
