from django.http import HttpResponse
from django.conf import settings
import os

def robots_txt(request):
    robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
    try:
        with open(robots_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/plain")
    except FileNotFoundError:
        return HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")
