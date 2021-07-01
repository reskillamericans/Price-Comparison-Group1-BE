from django.http import HttpResponse
from django.shortcuts import redirect


# Restricts pages that unauthenticated users can access (used in views.py)
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        # If user is logged in, redirect to homepage
        if request.user.is_authenticated:
            return redirect('index')

        # If user is not logged in, show the page they tried to access
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# Allows users with the given roles to access certain pages (used in views.py)
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # Check if user is apart of any Groups
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # If User group is allowed, show the page
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If User group is not allowed, show unauthorized message
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
