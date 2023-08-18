import json
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

from ..errors.authErrors import InvalidPasswordError

from ..models import CustomUser


def auth_user(request: HttpRequest):
    headers = request.headers
    print(headers)
    if headers['Content-Type'] != 'application/json':
        return HttpResponseBadRequest('Request body must be JSON')
    data = json.loads(request.body)
    print(data)
    ## TODO assert body params
    try:
        user = CustomUser.objects.get(email=data['email'])
        user.validate_password(data['password'])
    except (CustomUser.DoesNotExist, InvalidPasswordError):
        return HttpResponseForbidden('Invalid credentials')
        
    token = 'new_token'
    user.set_token(token)
    user.save()
    return JsonResponse({
        "success": True,
        "data": {
            "token": token
        }
    })