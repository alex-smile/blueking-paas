# -*- coding: utf-8 -*-
import logging
from typing import Optional, Tuple

from bkpaas_auth import get_user_by_user_id
from bkpaas_auth.core.token import LoginToken
from bkpaas_auth.models import User
from blue_krill.auth.client import check_client_role
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication

logger = logging.getLogger(__name__)


# How long until the faked LoginToken objects were considered expired, in seconds
FAKE_TOKEN_EXPIRES_IN = 86400


class UserFromVerifiedClientAuthentication(BaseAuthentication):
    """Consider user provided by verified client as current user"""

    valid_jwt_role = 'service-proxy'

    def authenticate(self, request: HttpRequest) -> Optional[Tuple[User, None]]:
        if not check_client_role(request, self.valid_jwt_role):
            # Return `None` to indicate that current authenticator fail to succeed, this follows the protocol
            # of DRF's authenticator, see: https://www.django-rest-framework.org/api-guide/authentication/
            return None

        user_pk = request.extra_payload.get('current_user_pk')
        if user_pk:
            user = get_user_by_user_id(user_pk, username_only=True)
            # Set an un-expired token to make user "authenticated", otherwise it will be treated
            # as un-authenticated.
            user.token = LoginToken(login_token='any_token', expires_in=FAKE_TOKEN_EXPIRES_IN)
            return user, None
        return None
