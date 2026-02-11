from django.http import JsonResponse
from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'admin':
            return JsonResponse({'error': 'Доступ запрещен'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
