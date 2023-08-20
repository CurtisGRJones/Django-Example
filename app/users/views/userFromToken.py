from django.http import HttpRequest

from ..utils.responses import success_response, fail_response

from ..models import CustomUser


def user_from_token(request: HttpRequest):
    try:
        assert 'auth_token' in request.COOKIES
        user = CustomUser.get_user_from_token(request.COOKIES['auth_token'])
    except (AssertionError, CustomUser.DoesNotExist):
        return fail_response('Invalid credentials')

    return success_response(user.user_data())