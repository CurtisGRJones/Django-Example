from django.http import JsonResponse

from ..models import CustomUser


def auth_user_token(request):
    return JsonResponse({
        "success": True,
    })