from django.http import HttpRequest

from utils.getUserFromReqest import get_user_from_request
from utils.errors import InvalidTokenError
from utils.responses import fail_response, success_response



def user_from_token(request: HttpRequest):
    try:
        user = get_user_from_request(request)
    except InvalidTokenError:
        return fail_response('Invalid credentials')
    
    return success_response(user.user_data())