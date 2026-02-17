from django.utils import timezone


class PublishScheduledMiddleware:
    """Auto-publish scheduled articles when their publish time arrives.

    Uses Django's default cache to throttle checks to at most once per 60 seconds.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.core.cache import cache

        if not cache.get("_publish_check"):
            cache.set("_publish_check", True, timeout=60)
            from apps.articles.models import Article

            Article.objects.filter(
                status="scheduled",
                published_at__lte=timezone.now(),
            ).update(status="published")

        return self.get_response(request)
