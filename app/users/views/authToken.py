from django.http import JsonResponse

from ..models import CustomUser


def auth_user(request):
    return JsonResponse({
        "success": True,
    })