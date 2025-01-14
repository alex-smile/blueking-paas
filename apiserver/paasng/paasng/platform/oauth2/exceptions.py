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


class BkOauthApiException(Exception):
    """BaseException for Bk Oauth"""


class BkOauthApiResponseError(BkOauthApiException):
    """Bk Oauth API Response Error"""

    def __init__(self, message, status_code: int, request_url: str, response_text: str, request_id: str):
        self.message = message
        self.status_code = status_code
        self.request_url = request_url
        self.response_text = response_text
        self.request_id = request_id
        super().__init__(message)


class BkOauthClientDoesNotExist(Exception):
    """Bk Oauth client not exist"""
