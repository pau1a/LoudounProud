from django.core.cache import cache

from .models import SiteSettings


def base_context(request):
    all_towns = cache.get("all_towns")
    if all_towns is None:
        from apps.articles.models import Town
        all_towns = list(Town.objects.all())
        cache.set("all_towns", all_towns, 300)

    return {
        "settings": SiteSettings.load(),
        "all_towns": all_towns,
    }
