# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

import pytest

from paas_wl.resources.base.exceptions import ResourceMissing
from paas_wl.resources.base.generation import get_mapper_version
from paas_wl.resources.utils.basic import get_client_by_app
from paas_wl.workloads.processes.managers import AppProcessManager
from paas_wl.workloads.processes.utils import get_command_name
from tests.utils.app import release_setup

pytestmark = pytest.mark.django_db


class TestGeneration:
    @pytest.fixture
    def release(self, fake_app):
        return release_setup(
            fake_app=fake_app,
            build_params={"procfile": {"web": "gunicorn wsgi -w 4 -b :$PORT --access-logfile - --error-logfile"}},
            release_params={"version": 2},
        )

    @pytest.fixture
    def process(self, fake_app, release):
        return AppProcessManager(app=fake_app).assemble_process(process_type="web", release=release)

    @pytest.fixture
    def client(self, fake_app):
        return get_client_by_app(fake_app)

    @pytest.fixture
    def v1_mapper(self):
        return get_mapper_version("v1")

    @pytest.fixture
    def v2_mapper(self):
        return get_mapper_version("v2")

    def test_v1_pod_name(self, v1_mapper, process):
        assert (
            v1_mapper.pod(process=process).name == f"{process.app.region}-{process.app.scheduler_safe_name}-"
            f"{process.name}-{get_command_name(process.runtime.proc_command)}-deployment"
        )

        assert (
            v1_mapper.deployment(process=process).name == f"{process.app.region}-{process.app.scheduler_safe_name}-"
            f"{process.name}-{get_command_name(process.runtime.proc_command)}-deployment"
        )

    def test_preset_process_client(self, fake_app, process, client, v1_mapper):
        assert (
            v1_mapper.pod(process=process, client=client).name
            == f"{process.app.region}-{process.app.scheduler_safe_name}-"
            f"{process.name}-{get_command_name(process.runtime.proc_command)}-deployment"
        )

    def test_v1_get(self, fake_app, process, client, v1_mapper):
        with pytest.raises(ValueError):
            v1_mapper.pod(process=process).get()

        mapper = v1_mapper.pod(process=process, client=client)
        with pytest.raises(ResourceMissing):
            mapper.get()

        kp = Mock(return_value={"items": [1, 2, 3]})
        with patch('paas_wl.resources.base.kres.NameBasedOperations.get', kp):
            assert mapper.get() == {"items": [1, 2, 3]}

    def test_v1_delete(self, fake_app, process, client, v1_mapper):
        kd = Mock(return_value=None)
        with patch('paas_wl.resources.base.kres.NameBasedOperations.delete', kd):
            mapper = v1_mapper.pod(process=process, client=client)
            assert mapper.delete() is None
            args, kwargs = kd.call_args_list[0]
            assert kd.called
            assert kwargs['name'] == mapper.name
            assert kwargs['namespace'] == mapper.namespace

    def test_v1_create(self, fake_app, process, client, v1_mapper):
        kd = Mock(return_value={"items": [1, 2, 3]})
        with patch('paas_wl.resources.base.kres.NameBasedOperations.create', kd):
            mapper = v1_mapper.pod(process=process, client=client)
            assert mapper.create(body={}) == {"items": [1, 2, 3]}
            args, kwargs = kd.call_args_list[0]
            assert kd.called
            assert kwargs['name'] == mapper.name
            assert kwargs['namespace'] == mapper.namespace

    def test_v2_name(self, process, v2_mapper):
        assert v2_mapper.pod(process=process).name == f"{process.app.name.replace('_', '0us0')}--{process.name}"
        assert v2_mapper.deployment(process=process).name == f"{process.app.name.replace('_', '0us0')}--{process.name}"
