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
import json

from django.conf import settings
from django.utils.translation import get_language

from .component import BaseComponent
from .http import http_get, http_post


class APIGWDashboardComponent(BaseComponent):

    host = getattr(settings, 'APIGW_DASHBOARD_HOST', '')
    system_name = "apigw-dashboard"

    def get(self, path: str, bk_username: str = '', **kwargs):
        return self._call_api(http_get, path, headers=self._prepare_headers(bk_username), **kwargs)

    def post(self, path: str, bk_username: str = '', **kwargs):
        return self._call_api(http_post, path, headers=self._prepare_headers(bk_username), **kwargs)

    def _prepare_headers(self, bk_username: str):
        headers = {
            'x-bkapi-authorization': json.dumps(
                {
                    'bk_app_code': settings.BK_APP_CODE,
                    'bk_app_secret': settings.BK_APP_SECRET,
                    'bk_username': bk_username,
                }
            )
        }

        language = get_language()
        if language:
            headers["Accept-Language"] = language

        return headers


apigw_dashboard_component = APIGWDashboardComponent()
