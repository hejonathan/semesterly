from django.utils.deprecation import MiddlewareMixin


class ForceJHUMiddleware(MiddlewareMixin):
    """Serve JHU on any hostname."""

    def process_request(self, request):
        request.subdomain = "jhu"


def selfhost_context(request):
    """Template context processor: show the self-hosted notice popup."""
    import os

    return {
        "SELFHOST_NOTICE": True,
        # Your own Google Analytics ID (G-XXXX); unset = no analytics.
        "SELFHOST_GA_ID": os.environ.get("GA_MEASUREMENT_ID", ""),
    }
