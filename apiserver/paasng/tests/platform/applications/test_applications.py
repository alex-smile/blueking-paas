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
import logging

import pytest
from django.conf import settings
from django.test import TestCase
from django_dynamic_fixture import G

from paasng.platform.applications.constants import ApplicationType
from paasng.platform.applications.models import Application, ApplicationMembership, UserApplicationFilter
from paasng.platform.applications.utils import create_default_module
from paasng.platform.modules.constants import SourceOrigin
from paasng.platform.modules.models import Module
from tests.utils.auth import create_user

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.django_db


class TestCreateDefaultModule(TestCase):
    def setUp(self):
        self.user = create_user()
        self.application = G(
            Application, owner=self.user.pk, code='awesome-app', language='Python', region=settings.DEFAULT_REGION_NAME
        )

    def test_create_default_module(self):
        assert Module.objects.filter(application=self.application).count() == 0
        create_default_module(self.application)

        assert Module.objects.filter(application=self.application).count() == 1
        assert self.application.get_default_module().application == self.application


class BaseCaseWithApps:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user = create_user()
        self.another_user = create_user(username='another_user')
        self.app1 = G(
            Application,
            owner=self.user.pk,
            code='awesome-app',
            language='Python',
            region=settings.DEFAULT_REGION_NAME,
            type=ApplicationType.DEFAULT,
        )
        create_default_module(self.app1, source_origin=SourceOrigin.AUTHORIZED_VCS, language='Python')
        self.app_another1 = G(
            Application,
            owner=self.another_user.pk,
            code='awesome-bk',
            language='PHP',
            region=settings.DEFAULT_REGION_NAME,
            type=ApplicationType.BK_PLUGIN,
        )
        create_default_module(self.app_another1, source_origin=SourceOrigin.AUTHORIZED_VCS, language='PHP')
        self.app_another2 = G(
            Application,
            owner=self.another_user.pk,
            code='gcloud',
            language='Python',
            region=settings.DEFAULT_REGION_NAME,
        )
        create_default_module(self.app_another2, source_origin=SourceOrigin.BK_LESS_CODE, language='Python')
        self.app_another3 = G(
            Application,
            owner=self.another_user.pk,
            code='awesome-php',
            language='PHP',
            region=settings.DEFAULT_REGION_NAME,
        )
        create_default_module(self.app_another3, source_origin=SourceOrigin.BK_LESS_CODE, language='PHP')

        # Add self.user as collaborators
        G(ApplicationMembership, application=self.app1, user=self.user.pk, region=settings.DEFAULT_REGION_NAME)
        G(ApplicationMembership, application=self.app_another1, user=self.user.pk, region=settings.DEFAULT_REGION_NAME)
        G(ApplicationMembership, application=self.app_another2, user=self.user.pk, region=settings.DEFAULT_REGION_NAME)


class TestApplicationManager(BaseCaseWithApps):
    def test_filter_by_user_normal(self):
        apps = Application.objects.filter_by_user(self.user)
        assert set(apps) == {self.app1, self.app_another1, self.app_another2}

    def test_filter_by_userremove(self):
        ApplicationMembership.objects.filter(application=self.app_another2).delete()
        apps = Application.objects.filter_by_user(self.user)
        assert set(apps) == {self.app1, self.app_another1}

    def test_filter_language(self):
        apps = Application.objects.filter_by_user(self.user).filter_by_languages(['Python'])
        assert set(apps) == {self.app1, self.app_another2}

        # 给 app_another1 添加 Python 语言的模块后能过滤出来
        Module.objects.create(
            region=self.app_another1.region, application=self.app_another1, name="python", language="Python"
        )
        apps_new = Application.objects.filter_by_user(self.user).filter_by_languages(['Python'])
        assert set(apps_new) == {self.app1, self.app_another2, self.app_another1}

    def test_active_only(self):
        apps = Application.objects.filter_by_user(self.user).filter_by_languages(['Python']).only_active()
        assert set(apps) == {self.app1, self.app_another2}

        self.app1.is_active = False
        self.app1.save()
        apps = Application.objects.filter_by_user(self.user).filter_by_languages(['Python']).only_active()
        assert set(apps) == {self.app_another2}

    def test_search_by_code_or_name(self):
        apps = Application.objects.filter_by_user(self.user).search_by_code_or_name('awesome')
        assert set(apps) == {self.app1, self.app_another1}

    def test_filter_by_user(self):
        apps = Application.objects.filter_by_user(self.user)
        assert set(apps) == {self.app1, self.app_another1, self.app_another2}

        apps = Application.objects.filter_by_user(self.user, exclude_collaborated=True)
        assert set(apps) == {self.app1}

    def test_filter_by_source_origin(self):
        apps = Application.objects.filter_by_user(self.user).filter_by_source_origin(SourceOrigin.BK_LESS_CODE)
        assert set(apps) == {self.app_another2}


class TestUserApplication(BaseCaseWithApps):
    def test_filter(self):
        apps_filter = UserApplicationFilter(self.user)
        assert set(apps_filter.filter(languages=['Python'])) == {self.app1, self.app_another2}
        assert set(apps_filter.filter(search_term='awesome')) == {self.app1, self.app_another1}

    def test_filter_by_type_(self):
        apps_filter = UserApplicationFilter(self.user)
        assert set(apps_filter.filter(type_=ApplicationType.DEFAULT)) == {self.app1, self.app_another2}
        assert set(apps_filter.filter(type_=ApplicationType.BK_PLUGIN)) == {self.app_another1}
