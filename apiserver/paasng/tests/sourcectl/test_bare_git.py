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
from unittest import mock

import pytest

from paasng.dev_resources.sourcectl.controllers.bare_git import BareGitRepoController
from paasng.dev_resources.sourcectl.models import GitRepository, RepoBasicAuthHolder
from paasng.dev_resources.sourcectl.source_types import get_sourcectl_names

pytestmark = pytest.mark.django_db


class TestGeneralGitController:
    """测试通用 General Git Controller"""

    @staticmethod
    def get_fake_repo(bk_module, repo_url):
        r = GitRepository.objects.create(server_name=get_sourcectl_names().bare_git, repo_url=repo_url)
        bk_module.source_type = get_sourcectl_names().bare_git
        bk_module.source_repo_id = r.pk
        bk_module.save(update_fields=['source_type', 'source_repo_id'])
        return r

    @staticmethod
    def get_fake_auth_holder(bk_module, repo, username, password):
        return RepoBasicAuthHolder.objects.create(
            username=username,
            password=password,
            repo_id=repo.pk,
            repo_type=get_sourcectl_names().bare_git,
            module=bk_module,
        )

    @pytest.mark.parametrize(
        "auth_token_pair,repo_url,target_url",
        [
            (("admin", "tokenfake"), "http://asdf.com/ddd.git", "http://admin:tokenfake@asdf.com/ddd.git"),
            (("admin", "tokenfake"), "git://asdf.com/ddd.git", "git://admin:tokenfake@asdf.com/ddd.git"),
            (
                ("blues@Smith", "token@fake"),
                "git://asdf.com/ddd.git",
                "git://blues%40Smith:token%40fake@asdf.com/ddd.git",
            ),
        ],
    )
    def test_init_by_module(self, bk_module, auth_token_pair, repo_url, target_url):
        """测试初始化"""
        fake_repo = self.get_fake_repo(bk_module, repo_url)
        self.get_fake_auth_holder(bk_module, fake_repo, auth_token_pair[0], auth_token_pair[1])
        with mock.patch("paasng.dev_resources.sourcectl.models.GitRepository.get_repo_url") as patched_get_repo_url:

            def return_fake_url():
                return repo_url

            patched_get_repo_url.side_effect = return_fake_url

            c = BareGitRepoController.init_by_module(bk_module, "admin")
            assert c.repo_url == target_url
