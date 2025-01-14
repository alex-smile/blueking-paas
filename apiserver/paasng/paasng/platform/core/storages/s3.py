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
from django.conf import settings
from django.utils.functional import LazyObject

from paasng.utils.blobstore import get_storage_by_bucket


class S3Storage(LazyObject):
    def __init__(self, bucket: str):
        super().__init__()
        self.__dict__["__bucket__"] = bucket

    def _setup(self):
        self._wrapped = get_storage_by_bucket(self.__bucket__)


service_logo_storage = S3Storage(bucket=settings.SERVICE_LOGO_BUCKET)
app_logo_storage = S3Storage(bucket=settings.APP_LOGO_BUCKET)
