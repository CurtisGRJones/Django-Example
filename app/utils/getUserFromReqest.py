from django.http import HttpRequest

from utils.errors.authErrors import InvalidTokenError

from .responses import success_response, fail_response

from users.models import CustomUser


def get_user_from_request(request: HttpRequest):
    try:
        assert 'auth_token' in request.COOKIES
        user = CustomUser.get_user_from_token(request.COOKIES['auth_token'])
    except (AssertionError, CustomUser.DoesNotExist):
        raise InvalidTokenError()
        

    return user