from django.http import JsonResponse

def success_response(data, **kwargs):
    response = JsonResponse({
        "success": True,
        "data": data
    }, **kwargs)

    return response
    

def fail_response(reason, **kwargs):
    response = JsonResponse({
        "success": False,
        "reason": reason
    }, **kwargs)

    return response