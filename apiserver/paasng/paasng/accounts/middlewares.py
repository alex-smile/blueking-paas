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
from typing import Optional

from bkpaas_auth.models import DatabaseUser
from blue_krill.auth.utils import validate_jwt_token
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_text
from django.utils.translation import gettext as _
from rest_framework.authentication import get_authorization_header

from paasng.utils.basic import get_client_ip
from paasng.utils.local import local

from .models import AuthenticatedAppAsUser, User, UserPrivateToken
from .permissions.tools import user_has_perm

logger = logging.getLogger(__name__)


class SiteAccessControlMiddleware(MiddlewareMixin):
    """Control who can visit which paths in macro way"""

    def process_request(self, request):
        # TODO: Find a better way to determine which views are belongs to admin42
        if request.path_info.startswith('/admin42/'):
            if request.user.is_anonymous or not request.user.is_authenticated:
                # 用户验证失败，重定向到登录页面
                return HttpResponseRedirect(f"{settings.LOGIN_FULL}?c_url={request.build_absolute_uri()}")

            if not user_has_perm(request.user, 'visit_admin', 'site'):
                raise PermissionDenied('You are not allowed to visit this')

            return

        # Ignore anonymous user
        if not request.user.is_authenticated:
            return

        if not user_has_perm(request.user, 'visit_site', 'site'):
            # Use a custom
            return JsonResponse({"code": "PRODUCT_NOT_READY", "detail": _('产品灰度测试中，尚未开放，敬请期待')}, status=404)


class PrivateTokenAuthenticationMiddleware:
    """Authenticate user by private token"""

    AUTH_HEADER_TYPE = 'Bearer'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self.get_user(request)
        if user:
            logger.info(
                'Authenticated user by PrivateToken, username: %s, ip: %s, path: %s',
                user.username,
                get_client_ip(request),
                request.path_info,
            )
            set_database_user(request, user)

        response = self.get_response(request)
        return response

    def get_user(self, request) -> Optional[User]:
        """Get user object from current request"""
        token_string = self.get_token_string(request)
        # Ignore empty or JWT format token
        if not token_string or validate_jwt_token(token_string):
            return None
        try:
            token_obj = UserPrivateToken.objects.get(token=token_string)
        except UserPrivateToken.DoesNotExist:
            logger.warning(f'private token {token_string} does not exist in database')
            return None

        if token_obj.has_expired():
            logger.warning(f'private token {token_string} has expired')
            return None

        logger.debug(f'private token {token_string} is valid, user is {token_obj.user.username}')
        return token_obj.user

    def get_token_string(self, request) -> Optional[str]:
        """Get private token string from current request"""
        # Source: query string
        token_from_qs = request.GET.get('private_token', None)
        if token_from_qs:
            return token_from_qs

        # Source: Authorization header
        token_from_header = self.get_token_string_from_header(request)
        if token_from_header:
            return token_from_header

        return None

    def get_token_string_from_header(self, request) -> Optional[str]:
        """Get private token string from current request header"""
        auth = get_authorization_header(request).split()
        # Turn bytestring into str
        auth = [smart_text(s) for s in auth]

        if not auth or auth[0].lower() != self.AUTH_HEADER_TYPE.lower():
            return None

        if len(auth) == 1:
            logger.warning('Invalid token header. No private token provided.')
            return None
        elif len(auth) > 2:
            logger.warning('Invalid token header. Token string should not contain spaces.')
            return None
        return auth[1]


class AuthenticatedAppAsUserMiddleware:
    """When an API request forwarded by API Gateway was received, if it includes an authenticated
    app(aka "OAuth client") and has no authenticated user info too. This middleware will try to find
    a `DatabaseUser` object by querying `AuthenticatedAppAsUser` relations.

    If other services want to call apiserver's SYSTEM APIs, this middleware can be very useful.
    Under these circumstances, a valid "app_code/app_secret" pair usually was already provided in every
    request, if "app_code" was configured in `AuthenticatedAppAsUser`, no extra credentials were
    needed in order to make a authenticated request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ignore already authenticated requests
        if getattr(request, 'user', None) and request.user.is_authenticated:
            return self.get_response(request)

        user = self.get_user(request)
        if user:
            logger.info(
                'Authenticated user by AuthenticatedApp, username: %s, ip: %s, path: %s',
                user.username,
                get_client_ip(request),
                request.path_info,
            )
            set_database_user(request, user)

        response = self.get_response(request)
        return response

    def get_user(self, request) -> Optional[User]:
        """Get user object from current request"""
        if not getattr(request, 'app', None):
            return None
        if not request.app.verified:
            return None

        try:
            obj = AuthenticatedAppAsUser.objects.get(bk_app_code=request.app.bk_app_code, is_active=True)
            return obj.user
        except AuthenticatedAppAsUser.DoesNotExist:
            logger.info(f'No user was found by authenticated app: {request.app.bk_app_code}')
            return None


class RequestIDProvider:
    """向 request，response 注入 request_id"""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        local.request = request
        request.request_id = local.get_http_request_id()

        response = self.get_response(request)
        response[settings.REQUEST_ID_HEADER_KEY] = request.request_id

        local.release()
        return response


def set_database_user(request: HttpRequest, user: User, set_non_cookies: bool = True):
    """Mark current request authenticated with a user stored in database

    :param user: a `models.User` object
    :param set_non_cookies: whether set a special attribute to mark current request was NOT authenticated
        via user cookies.
    """
    # Translate user into module "bkpaas_auth"'s User object to mantain consistency.
    request.user = DatabaseUser.from_db_obj(user=user)
    if set_non_cookies:
        # Reference from bkpaas_auth
        # Set a special attribute on request to mark this user was not authenticated from
        # cookie, so we may apply other logics afterwards, such as skipping CSRF checks.
        setattr(request, '_bkpaas_auth_authenticated_from_non_cookies', True)
