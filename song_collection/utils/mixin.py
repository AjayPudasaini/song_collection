from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator


class SuperuserRequiredMixin:
    """
    View mixin to restrict access to superusers (admin users).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
