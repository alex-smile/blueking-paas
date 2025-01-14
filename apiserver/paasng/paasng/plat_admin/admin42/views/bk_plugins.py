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
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from paasng.extensions.bk_plugins.models import BkPluginDistributor, BkPluginTag
from paasng.plat_admin.admin42.serializers.bk_plugins import BkPluginDistributorSLZ, BKPluginTagSLZ
from paasng.plat_admin.admin42.utils.mixins import GenericTemplateView


class BKPluginTagManageView(GenericTemplateView):
    """平台服务管理-插件分类配置"""

    template_name = "admin42/configuration/bk_plugin_tag.html"
    queryset = BkPluginTag.objects.all()
    serializer_class = BKPluginTagSLZ
    name = "插件分类配置"


class BKPluginTagView(CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """平台服务管理-插件分类配置API"""

    queryset = BkPluginTag.objects.all()
    serializer_class = BKPluginTagSLZ


class BKPluginDistributorsManageView(GenericTemplateView):
    """平台服务管理-插件使用方配置"""

    template_name = "admin42/configuration/bk_plugin_distributor.html"
    queryset = BkPluginDistributor.objects.all()
    serializer_class = BkPluginDistributorSLZ
    name = "插件使用方配置"


class BKPluginDistributorsView(CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """平台服务管理-插件使用方配置API"""

    queryset = BkPluginDistributor.objects.all()
    serializer_class = BkPluginDistributorSLZ
