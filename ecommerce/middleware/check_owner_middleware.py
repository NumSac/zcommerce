# ownership_check_middleware.py

from django.http import Http404


class CheckOwnerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the current view requires ownership check
        if hasattr(request, "view") and hasattr(request.view, "check_ownership"):
            view = request.view
            # Get the object to be checked for ownership
            obj = view.get_object()
            if obj.owner != request.user.id:
                raise Http404("You do not have permission to view this object.")

        response = self.get_response(request)
        return response
