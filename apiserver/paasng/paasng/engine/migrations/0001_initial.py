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
import paasng.engine.models.base
import paasng.utils.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('operator', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('source_type', models.CharField(max_length=16, null=True, verbose_name='源码托管类型')),
                ('source_location', models.CharField(max_length=2048, verbose_name='代码地址')),
                ('source_version_type', models.CharField(max_length=64, verbose_name='代码版本类型')),
                ('source_version_name', models.CharField(max_length=64, verbose_name='代码版本名称')),
                ('source_revision', models.CharField(max_length=128, null=True, verbose_name='版本号')),
                ('source_comment', models.TextField(verbose_name='版本说明')),
                ('status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=16, verbose_name='部署状态')),
                ('build_process_id', models.UUIDField(null=True)),
                ('build_id', models.UUIDField(null=True)),
                ('build_status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=16)),
                ('release_id', models.UUIDField(null=True)),
                ('release_status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=16)),
                ('err_detail', models.TextField(blank=True, null=True, verbose_name='部署异常原因')),
                ('advanced_options', jsonfield.fields.JSONField(null=True, verbose_name='高级选项')),
                ('app_environment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deployments', to='applications.ApplicationEnvironment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeployPhase',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('preparation', '准备阶段'), ('build', '构建阶段'), ('release', '部署阶段')], max_length=32, verbose_name='部署阶段类型')),
                ('status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], max_length=32, null=True, verbose_name='状态')),
                ('start_time', models.DateTimeField(null=True, verbose_name='阶段开始时间')),
                ('complete_time', models.DateTimeField(null=True, verbose_name='阶段完成时间')),
                ('deployment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='engine.Deployment', verbose_name='关联部署操作')),
            ],
            options={
                'ordering': ['created'],
            },
            bases=(models.Model, paasng.engine.models.base.MarkStatusMixin),
        ),
        migrations.CreateModel(
            name='EngineApp',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('region', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否活跃')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OneOffCommand',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('engine_cmd_id', models.UUIDField(null=True, verbose_name='engine command id')),
                ('is_pre_run', models.BooleanField(default=True)),
                ('exit_code', models.SmallIntegerField(null=True, verbose_name='ExitCode')),
                ('status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=16)),
                ('command', models.TextField()),
                ('operator', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('deployment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oneoffcommands', to='engine.Deployment')),
            ],
            options={
                'ordering': ['-created'],
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='OfflineOperation',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('operator', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('source_type', models.CharField(max_length=16, null=True, verbose_name='源码托管类型')),
                ('source_location', models.CharField(max_length=2048, verbose_name='代码地址')),
                ('source_version_type', models.CharField(max_length=64, verbose_name='代码版本类型')),
                ('source_version_name', models.CharField(max_length=64, verbose_name='代码版本名称')),
                ('source_revision', models.CharField(max_length=128, null=True, verbose_name='版本号')),
                ('source_comment', models.TextField(verbose_name='版本说明')),
                ('status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=16, verbose_name='下线状态')),
                ('log', models.TextField(blank=True, null=True, verbose_name='下线日志')),
                ('err_detail', models.TextField(blank=True, null=True, verbose_name='下线异常原因')),
                ('app_environment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offlines', to='applications.ApplicationEnvironment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModuleEnvironmentOperations',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('operator', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('operation_type', models.CharField(choices=[('offline', 'OFFLINE'), ('online', 'ONLINE')], max_length=32)),
                ('object_uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='详情记录的UUID')),
                ('status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], default='pending', max_length=16, verbose_name='操作状态')),
                ('app_environment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='module_operations', to='applications.ApplicationEnvironment')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_operations', to='applications.Application')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MobileConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_enabled', models.BooleanField(default=False, verbose_name='移动端配置是否生效')),
                ('lb_plan', models.CharField(choices=[('LBDefaultPlan', 'requests from bk lb to bk cluster')], default='LBDefaultPlan', help_text='which one-level load balancer plan the domain use', max_length=64, verbose_name='load balancer plan')),
                ('environment', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='mobile_config', to='applications.ApplicationEnvironment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeployStep',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=32, verbose_name='步骤名称')),
                ('skipped', models.BooleanField(default=False, verbose_name='是否跳过')),
                ('status', models.CharField(choices=[('successful', 'successful'), ('failed', 'failed'), ('pending', 'pending')], max_length=32, null=True, verbose_name='状态')),
                ('start_time', models.DateTimeField(null=True, verbose_name='阶段开始时间')),
                ('complete_time', models.DateTimeField(null=True, verbose_name='阶段完成时间')),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='engine.DeployPhase', verbose_name='关联阶段')),
            ],
            options={
                'ordering': ['created'],
            },
            bases=(models.Model, paasng.engine.models.base.MarkStatusMixin),
        ),
        migrations.AddField(
            model_name='deployphase',
            name='engine_app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.EngineApp', verbose_name='关联引擎应用'),
        ),
        migrations.CreateModel(
            name='CellPackagePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, verbose_name='计算资源组方案名称')),
                ('region', models.CharField(max_length=32)),
                ('environment', models.CharField(max_length=32, verbose_name='方案适用环境')),
                ('max_replicas', models.IntegerField(verbose_name='最大副本数')),
                ('limits', jsonfield.fields.JSONField(default={})),
                ('requests', jsonfield.fields.JSONField(default={})),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
            ],
            options={
                'get_latest_by': 'created',
                'unique_together': {('name', 'region', 'environment')},
            },
        ),
        migrations.CreateModel(
            name='CellPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, verbose_name='计算单元组名称')),
                ('type', models.CharField(choices=[('process', '进程'), ('vm', '虚拟机')], max_length=32, verbose_name='计算单元组类型')),
                ('target_replicas', models.IntegerField(default=1, verbose_name='副本数')),
                ('target_status', models.CharField(default='start', max_length=32, verbose_name='用户设置的状态')),
                ('engine_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cell_attachment', to='engine.EngineApp')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.CellPackagePlan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.CellPackage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=253)),
                ('lb_plan', models.CharField(choices=[('LBDefaultPlan', 'requests from bk lb to bk cluster')], default='LBDefaultPlan', help_text='which one-level load balancer plan the domain use', max_length=64, verbose_name='load balancer plan')),
                ('environment', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.ApplicationEnvironment')),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modules.Module')),
            ],
            options={
                'unique_together': {('module', 'name', 'environment')},
            },
        ),
        migrations.CreateModel(
            name='ConfigVar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_global', models.BooleanField(default=False)),
                ('key', models.CharField(max_length=128)),
                ('value', models.TextField()),
                ('description', models.CharField(max_length=200, null=True)),
                ('is_builtin', models.BooleanField(default=False)),
                ('environment', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.ApplicationEnvironment')),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modules.Module')),
            ],
            options={
                'unique_together': {('module', 'is_global', 'environment', 'key')},
            },
        ),
    ]
