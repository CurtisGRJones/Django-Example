import json
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

from ..errors.authErrors import InvalidPasswordError

from ..models import CustomUser, LoginAttempt


def auth_user(request: HttpRequest):
    ## TODO protect this against timing attacks
    headers = request.headers
    if headers['Content-Type'] != 'application/json':
        return HttpResponseBadRequest('Request body must be JSON')
    data = json.loads(request.body)

    
    try:
        assert 'email' in data
        user = CustomUser.objects.get(email=data['email'])
    except (AssertionError, CustomUser.DoesNotExist):
        return HttpResponseForbidden('Invalid credentials')
    
    attempt = LoginAttempt(
        user=user
    )

    try:
        assert 'password' in data
        user.validate_password(data['password'])
    except (AssertionError, InvalidPasswordError):
        attempt.success = False
        attempt.save()
        return HttpResponseForbidden('Invalid credentials')
    
    attempt.success = True
    attempt.save()
        
    token = user.set_token()
    return JsonResponse({
        "success": True,
        "data": {
            "token": token
        }
    })