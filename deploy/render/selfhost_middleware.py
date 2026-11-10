from django.utils.deprecation import MiddlewareMixin


class ForceJHUMiddleware(MiddlewareMixin):
    """Serve JHU on any hostname."""

    def process_request(self, request):
        request.subdomain = "jhu"


def selfhost_context(request):
    """Template context processor: show the self-hosted notice popup."""
    return {"SELFHOST_NOTICE": True}
