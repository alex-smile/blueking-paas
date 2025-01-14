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
import paasng.publish.market.models
import paasng.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='分类名称', max_length=64, verbose_name='分类名称')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=255, null=True, verbose_name='备注')),
                ('index', models.IntegerField(default=0, help_text='显示排序字段', verbose_name='排序')),
                ('enabled', models.BooleanField(default=True, help_text='创建应用时是否可选择该分类', verbose_name='是否可选')),
                ('region', models.CharField(help_text='部署区域', max_length=32, verbose_name='部署环境')),
                ('parent', models.ForeignKey(blank=True, help_text='对于一级分类，该字段为空', null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Tag', verbose_name='APP一级分类')),
            ],
            options={
                'ordering': ('index', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('code', models.CharField(help_text='应用编码', max_length=64, unique=True, verbose_name='应用编码')),
                ('name', models.CharField(help_text='目前与应用名称保持一致，在 2 个表中修改时都需要相互同步数据，不能超过20个字符', max_length=64, verbose_name='应用在市场中的名称')),
                ('logo', paasng.utils.models.ProcessedImageField(upload_to=paasng.publish.market.models.upload_renamed_to_app_code)),
                ('introduction', models.TextField(help_text='应用简介', verbose_name='应用简介')),
                ('description', models.TextField(default='', help_text='应用描述', verbose_name='应用描述')),
                ('type', models.SmallIntegerField(choices=[(1, '蓝鲸应用'), (2, '第三方应用')], help_text='按实现方式分类', verbose_name='应用类型')),
                ('state', models.SmallIntegerField(choices=[(1, '开发中'), (2, '已发布'), (3, '市场下架')], default=1, help_text='应用状态', verbose_name='状态')),
                ('related_corp_products', jsonfield.fields.JSONField(default=[], help_text='所属业务')),
                ('application', models.OneToOneField(blank=True, help_text='PAAS应用', null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.Application', verbose_name='PAAS 应用')),
                ('tag', models.ForeignKey(blank=True, default=None, help_text='按用途分类', null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.Tag', verbose_name='app分类')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MarketConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('enabled', models.BooleanField(verbose_name='是否开启')),
                ('auto_enable_when_deploy', models.NullBooleanField(verbose_name='成功部署主模块正式环境后, 是否自动打开市场')),
                ('source_url_type', models.SmallIntegerField(verbose_name='访问地址类型')),
                ('source_tp_url', models.URLField(blank=True, null=True, verbose_name='第三方访问地址')),
                ('custom_domain_url', models.URLField(blank=True, null=True, verbose_name='绑定的独立域名访问地址')),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='market_config', to='applications.Application', verbose_name='蓝鲸应用')),
                ('source_module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modules.Module', verbose_name='访问目标模块')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DisplayOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, help_text='选项: true(是)，false(否)', verbose_name='是否显示在桌面')),
                ('width', models.IntegerField(default=890, help_text='应用页面宽度，必须为整数，单位为px', verbose_name='app页面宽度')),
                ('height', models.IntegerField(default=550, help_text='应用页面高度，必须为整数，单位为px', verbose_name='app页面高度')),
                ('is_win_maximize', models.BooleanField(default=False, verbose_name='是否默认窗口最大化')),
                ('win_bars', models.BooleanField(default=True, help_text='选项: true(on)，false(off)', verbose_name='窗口是否显示评分和介绍按钮')),
                ('resizable', models.BooleanField(default=True, help_text='选项：true(可以拉伸)，false(不可以拉伸)', verbose_name='是否能对窗口进行拉伸')),
                ('contact', models.CharField(blank=True, max_length=128, null=True, verbose_name='联系人')),
                ('open_mode', models.CharField(choices=[('desktop', '桌面'), ('new_tab', '新标签页')], default='desktop', max_length=20, verbose_name='打开方式')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='market.Product')),
            ],
        ),
    ]
