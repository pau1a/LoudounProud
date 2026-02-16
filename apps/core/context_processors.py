from .models import SiteSettings


def base_context(request):
    return {
        "settings": SiteSettings.load(),
    }
