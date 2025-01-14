# -*- coding: utf-8 -*-
import pytest

from paas_wl.cluster.models import Cluster
from paas_wl.cluster.utils import get_cluster_by_app
from tests.utils.app import random_fake_app

pytestmark = pytest.mark.django_db


class TestGetClusterByApp:
    @pytest.fixture(autouse=True)
    def setup(self, example_cluster_config):
        clusters = [
            {
                "name": "region1-default",
                "region": "region-1",
                "is_default": True,
                **example_cluster_config,
            },
            {
                "name": "region2-default",
                "region": "region-2",
                "is_default": True,
                **example_cluster_config,
            },
            {
                "name": "region2-custom",
                "region": "region-2",
                "is_default": False,
                **example_cluster_config,
            },
        ]
        for cluster in clusters:
            Cluster.objects.register_cluster(**cluster)

    def test_get_cluster_by_app_normal(self):
        app = random_fake_app(force_app_info={'region': 'region-2'})
        cluster = get_cluster_by_app(app)
        assert cluster.name == 'region2-default'

    def test_get_cluster_by_app_cluster_configured(self):
        app = random_fake_app(force_app_info={'region': 'region-2'})
        config = app.config_set.latest()
        config.cluster = 'region2-custom'
        config.save()

        cluster = get_cluster_by_app(app)
        assert cluster.name == 'region2-custom'
