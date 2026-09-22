from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def hello_world(request: HttpRequest) -> HttpResponse:
    """Return the application's greeting for the root endpoint."""
    return HttpResponse("Hello, world!", content_type="text/plain; charset=utf-8")
