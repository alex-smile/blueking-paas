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
# Generated by Django 2.2.17 on 2021-11-26 09:51

from django.db import migrations

from paasng.engine.models import DeployPhaseTypes


def list_metas_by_phase(self, phase_type: DeployPhaseTypes):
    # Tips: StepMetaSet 与 DeployStepMeta 是 N-N 的关系, 这里借助中间表的自增 id 进行排序
    return [
        relationship.deploystepmeta
        for relationship in self.metas.through.objects.filter(
            deploystepmeta__phase=phase_type.value, stepmetaset_id=self.pk
        )
        .order_by("id")
        .prefetch_related("deploystepmeta")
    ]


def forwards_func(apps, schema_editor):
    StepMetaSet = apps.get_model("engine", "StepMetaSet")
    DeployStepMeta = apps.get_model("engine", "DeployStepMeta")

    new_metas = [
        DeployStepMeta.objects.get_or_create(name=name, phase=DeployPhaseTypes.RELEASE.value)[0]
        for name in ["执行部署前置命令"]
    ]

    for meta_set in StepMetaSet.objects.all():
        old_metas = list_metas_by_phase(meta_set, DeployPhaseTypes.RELEASE)
        for meta in old_metas:
            meta_set.metas.remove(meta)
        for meta in new_metas + old_metas:
            meta_set.metas.add(meta)


def reverse_func(apps, schema_editor):
    DeployStepMeta = apps.get_model("engine", "DeployStepMeta")
    DeployStepMeta.objects.filter(name="执行部署前置命令").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0009_auto_20211118_1944'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
