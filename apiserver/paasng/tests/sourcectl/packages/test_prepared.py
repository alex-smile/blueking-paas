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
from pathlib import Path

import pytest

from paasng.extensions.smart_app.prepared import PreparedSourcePackage


class TestPreparedSourcePackage:
    @pytest.mark.parametrize(
        'file_path,expected_basename',
        [
            ('/var/本地日志3.log', '3.log'),
            ('/var/app$3-.tar.gz', 'app3.tar.gz'),
        ],
    )
    def test_generate_storage_path(self, file_path, expected_basename, rf, bk_user):
        request = rf.get('/')
        request.user = bk_user
        path = PreparedSourcePackage(request).generate_storage_path(file_path)
        assert Path(path).name.endswith(expected_basename)
