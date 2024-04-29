from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import APIKey, User

def api_key_required(view_func):
    def _decorator(request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        api_secret = request.headers.get('X-API-SECRET')

        if not api_key or not api_secret:
            return JsonResponse({"error": "please send X-API-KEY and X-API-SECRET in header"}, status=403)

        try:
            api_key_obj = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            return JsonResponse({"error": "Invalid API key"}, status=403)

        if not check_password(api_secret, api_key_obj.secret):
            return JsonResponse({"error": "Invalid API secret"}, status=403)

        return view_func(request, *args, **kwargs)

    return _decorator

def admin_required(view_func):
    def _decorator(request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        api_secret = request.headers.get('X-API-SECRET')

        if not api_key or not api_secret:
            return JsonResponse({"error": "You are not authorized to access this endpoint"}, status=403)
        try:
            ##check if the user is an superuser
            api_key_obj = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            return JsonResponse({"error": "Invalid API key"}, status=403)
        
        user = User.objects.get(firebase_id=api_key_obj.user_id)
        if not user.is_superuser:
            return JsonResponse({"error": "You are not authorized to access this endpoint"}, status=403)

        if not check_password(api_secret, api_key_obj.secret):
            return JsonResponse({"error": "Invalid API secret"}, status=403)

        return view_func(request, *args, **kwargs)

    return _decorator
