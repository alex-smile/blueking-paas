# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making BlueKing - PaaS System available.
Copyright (C) 2017-2022 THL A29 Limited, a Tencent company. All rights reserved.
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
import logging

from django.conf import settings
from iam import IAM, Action, Request, Subject
from iam.contrib.converter.sql import SQLConverter
from iam.exceptions import AuthAPIError

from paasng.accessories.bk_iam.constants import ActionEnum

logger = logging.getLogger(__name__)


class Permission:
    def __init__(self):
        self._iam = IAM(
            settings.IAM_APP_CODE, settings.IAM_APP_SECRET, settings.BK_IAM_V3_INNER_URL, settings.BK_PAAS2_URL
        )

    def _make_request_without_resources(self, username: str, action_id: str) -> 'Request':
        request = Request(
            settings.IAM_SYSTEM_ID,
            Subject("user", username),
            Action(action_id),
            None,
            None,
        )
        return request

    def allowed_manage_smart(self, username):
        """
        smart管理权限
        """
        try:
            request = self._make_request_without_resources(username, ActionEnum.MANAGE_SMART)
            return self._iam.is_allowed_with_cache(request)
        except AuthAPIError as e:
            logger.exception(f"check is allowed to manage smart app error: {e}")
            return False

    def app_filters(self, username):
        """
        用户有权限的应用列表

        拉回策略, 自己算!
        """
        request = self._make_request_without_resources(username, ActionEnum.DEVELOP_APP)

        # 两种策略 1) 实例级别 2) 用户级别
        # 只有条件 code in []
        key_mapping = {"app.id": "paas_app.code"}

        try:
            filters = self._iam.make_filter(request, converter_class=SQLConverter, key_mapping=key_mapping)
        except AuthAPIError as e:
            return None
        return filters
