import json
from django.http import HttpRequest

from utils.responses import fail_response, success_response
from utils.errors import InvalidPasswordError

from ..models import CustomUser, LoginAttempt


def auth_user(request: HttpRequest):
    ## TODO protect this against timing attacks
    headers = request.headers
    if headers['Content-Type'] != 'application/json':
        return fail_response('Request body must be JSON', status=400)
    data = json.loads(request.body)

    try:
        assert 'email' in data
        user = CustomUser.objects.get(email=data['email'])
    except (AssertionError, CustomUser.DoesNotExist):
        return fail_response('Invalid Credentials')
    
    attempt = LoginAttempt(
        user=user
    )

    try:
        assert 'password' in data
        user.validate_password(data['password'])
    except (AssertionError, InvalidPasswordError):
        attempt.success = False
        attempt.save()
        return fail_response('Invalid Credentials')
    
    attempt.success = True
    attempt.save()
        
    token = user.set_token()
    response = success_response({ "token": token })

    response.set_cookie('auth_token', token)

    return response