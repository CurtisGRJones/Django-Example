import json
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

from ..errors.authErrors import InvalidPasswordError

from ..models import CustomUser


def auth_user(request: HttpRequest):
    headers = request.headers
    if headers['Content-Type'] != 'application/json':
        return HttpResponseBadRequest('Request body must be JSON')
    data = json.loads(request.body)
    ## TODO assert body params
    try:
        assert 'email' in data
        assert 'password' in data
        user = CustomUser.objects.get(email=data['email'])
        user.validate_password(data['password'])
    except (CustomUser.DoesNotExist, InvalidPasswordError):
        return HttpResponseForbidden('Invalid credentials')
        
    token = user.set_token()
    return JsonResponse({
        "success": True,
        "data": {
            "token": token
        }
    })