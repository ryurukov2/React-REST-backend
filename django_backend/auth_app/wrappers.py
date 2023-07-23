from functools import wraps
from rest_framework.response import Response


def header_checker(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        print(request.user)
        if 'Authorization' not in request.headers:
            return Response({"Data": "Unauthorized"}, status=401)
        token = request.headers['Authorization']
        print(token)
        return view_func(request, *args, **kwargs)

    return wrapped_view


def header_check(err_message="Admin authorization required."):
    def decorator(view_function):
        def decorated_function(request, *args, **kwargs):
            # validate token existence
            if not 'Authorization' in request.headers:
                return Response({"detail": err_message}, status=401)

            else:
                token = request.headers['Authorization']
                print(token)
                return view_function(request, *args, **kwargs)

        return decorated_function
    return decorator
