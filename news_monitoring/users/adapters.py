from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from news_monitoring.source.models import Source

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

    from news_monitoring.users.models import User

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):

    def authenticate(self, request, email, password, **kwargs):
        """Override the authenticate method to use email as username."""
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    def generate_unique_username(self, email):
        """
        Override this to return the email as the username and ensure uniqueness.
        """
        # Ensure the email is unique
        if User.objects.filter(username=email).exists():
            raise ValidationError(_("This email is already in use."))

        return email

    def get_login_redirect_url(self, request):
        """
        Redirect users based on source availability.
        """
        user = request.user

        # Ensure the user is logged in before redirecting
        if not user.is_authenticated:
            login(request, user)

        if user.is_staff:
            return resolve_url("source:source_list")  # Staff goes to source list

        # Check if the user has any sources
        has_sources = Source.objects.filter(added_by=user).exists()
        return resolve_url("source:add_source" if not has_sources else "source:source_list")

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = super().populate_user(request, sociallogin, data)
        if not user.name:
            if name := data.get("name"):
                user.name = name
            elif first_name := data.get("first_name"):
                user.name = first_name
                if last_name := data.get("last_name"):
                    user.name += f" {last_name}"
        return user
