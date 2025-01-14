# -*- coding: utf-8 -*-
import json

import pytest

from paas_wl.platform.applications.models.app import App
from paas_wl.platform.system_api.serializers import AppSerializer
from paas_wl.utils.error_codes import error_codes

pytestmark = pytest.mark.django_db


class TestApp:
    @pytest.fixture
    def single_url(self, fake_app):
        return f"/regions/{fake_app.region}/apps/{fake_app.name}/"

    @pytest.fixture
    def multi_url(self, fake_app):
        return f"/regions/{fake_app.region}/apps/"

    def test_retrieve(self, fake_app, api_client, single_url):
        response = api_client.get(single_url)
        assert response.status_code == 200
        assert response.json() == AppSerializer(fake_app).data

    def test_update(self, fake_app, api_client, single_url):
        exc = error_codes.ENGINE_NOT_IMPLEMENTED
        response = api_client.post(single_url)
        response_content = json.loads(response.content)
        assert response.status_code == 501
        assert response_content == {'code': exc.code, 'detail': exc.message}

    def test_list(self, fake_app, api_client, multi_url):
        response = api_client.get(multi_url)
        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "previous": None,
            "next": None,
            "results": [AppSerializer(fake_app).data],
        }

    def test_create(self, fake_app, api_client, multi_url, bk_user):
        data = {"name": fake_app.name + '-to-create'}
        response = api_client.post(multi_url, data=data)
        assert response.status_code == 201
        assert response.json() == AppSerializer(App.objects.get(name=data["name"])).data

    def test_create_fail(self, fake_app, api_client, multi_url, bk_user):
        data = {"name": fake_app.name}
        response = api_client.post(multi_url, data=data)
        assert response.status_code == 400
        assert json.loads(response.content) == {"code": "APP_ALREADY_EXISTS", "detail": "创建失败，名称为 %(name)s 的应用已经存在。"}
