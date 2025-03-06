from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from .models import Teacher  # Import your Teacher model

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:  # Django default superuser check
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You are not authorized to access this page.")  # Forbidden response
        return redirect('login')  # Redirect to login if not authenticated
    return _wrapped_view

def hod_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                teacher = Teacher.objects.get(user_id=request.user)
                if teacher.is_hod:  # Check if the user is an HOD
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("You are not authorized to access this page.")  # Forbidden response
            except Teacher.DoesNotExist:
                return HttpResponseForbidden("You are not authorized to access this page.")  # User is not a teacher
        return redirect('login')  # Redirect to login if not authenticated
    return _wrapped_view
