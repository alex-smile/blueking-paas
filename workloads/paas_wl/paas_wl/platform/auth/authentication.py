# -*- coding: utf-8 -*-
"""Auth module for Django REST Framework"""
import logging
from typing import Optional, Tuple

from bkpaas_auth.core.constants import ProviderType
from bkpaas_auth.core.token import LoginToken
from bkpaas_auth.models import User
from blue_krill.auth.client import check_client_role
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication

logger = logging.getLogger(__name__)


FAKE_USERNAME = 'iadmin'
# How long until the faked LoginToken objects were considered expired, in seconds
FAKE_TOKEN_EXPIRES_IN = 86400


class AsInternalUserAuthentication(BaseAuthentication):
    """Consider current user is a fake 'admin' user.

    This middleware must be placed after `VerifiedClientRequired` middleware in order to
    read `request.extra_payload` attribute.
    """

    valid_jwt_role = 'internal-sys'

    def authenticate(self, request: HttpRequest) -> Optional[Tuple[User, None]]:
        if not check_client_role(request, self.valid_jwt_role):
            return None
        if request.extra_payload.get('current_user_pk'):
            # Request is bound with a real user, abort current process, let other authenticators proceed.
            return None

        token = LoginToken(login_token='any_token', expires_in=FAKE_TOKEN_EXPIRES_IN)
        user = User(token=token, provider_type=ProviderType.BK, username=FAKE_USERNAME)
        user.is_superuser = True
        return user, None
