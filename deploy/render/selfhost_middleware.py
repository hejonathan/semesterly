from django.utils.deprecation import MiddlewareMixin


class ForceJHUMiddleware(MiddlewareMixin):
    """Serve JHU on any hostname."""

    def process_request(self, request):
        request.subdomain = "jhu"
