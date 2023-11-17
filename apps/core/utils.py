from django.utils import timezone
from rest_framework.permissions import BasePermission
from apps.auth_module.auth import Authentication
from apps.auth_module.models import User, Jwt
from apps.core.models import File, GuestUser
from apps.core.exceptions import RequestError
from apps.betting.models import Bet
from apps.game.models import Player
from datetime import timedelta
from uuid import UUID
from django.db import transaction


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        if not http_auth:
            raise RequestError(err_msg="Auth Bearer not provided!", status_code=401)
        user = Authentication.decodeAuthorization(http_auth)
        if not user:
            raise RequestError(
                err_msg="Auth Token is Invalid or Expired!", status_code=401
            )
        request.user = user
        if request.user and request.user.is_authenticated:
            return True
        return False


class IsGuestOrAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        guest_id = request.headers.get("Guestuserid")
        if http_auth:
            user = Authentication.decodeAuthorization(http_auth)
            if not user:
                raise RequestError(
                    err_msg="Auth Token is Invalid or Expired!", status_code=401
                )
            request.user = user
        elif guest_id:
            guest = GuestUser.objects.filter(id=guest_id)
            if guest.exists():
                request.user = guest.get()
            else:
                request.user = None
        else:
            request.user = None
        return True


def is_uuid(value):
    try:
        return str(UUID(value))
    except:
        return None


def is_int(value):
    if not value:
        return None
    try:
        return int(value)
    except:
        raise RequestError(err_msg="Invalid Quantity params", status_code=422)


def match_players():
    # Get players with their total stakes
    players_with_stakes = Player.objects.filter("game__stake")

    # Iterate through players and try to find a match
    for player in players_with_stakes:
        # Find a player with the same stake (excluding the current player)
        match = (
            Player.objects.exclude(id=player.id)
            .filter(game__stake=player.total_stake)
            .first()
        )

        if match:
            # Players found with the same stake, perform matching logic
            with transaction.atomic():
                # Perform any matching logic here
                # For example, you can create a new Match model or update existing ones
                # Remember to handle edge cases and ensure that the logic is atomic (using transaction.atomic)

                print(
                    f"Matched {player} with {match} based on stake {player.total_stake}"
                )


# Test Utils
class TestUtil:
    def new_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
        }
        user = User(**user_dict)
        user.set_password("testpassword")
        user.save()
        return user

    def verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Verified",
            "email": "testverifieduser@example.com",
            "is_email_verified": True,
        }
        user = User(**user_dict)
        user.set_password("testpassword")
        user.save()
        return user

    def another_verified_user():
        create_user_dict = {
            "first_name": "AnotherTest",
            "last_name": "UserVerified",
            "email": "anothertestverifieduser@example.com",
            "is_email_verified": True,
        }
        user = User(**create_user_dict)
        user.set_password("anothertestverifieduser123")
        user.save()
        return user

    def auth_token(verified_user):
        access = Authentication.create_access_token({"user_id": str(verified_user.id)})
        refresh = Authentication.create_refresh_token()
        Jwt.objects.create(user_id=verified_user.id, access=access, refresh=refresh)
        return access
