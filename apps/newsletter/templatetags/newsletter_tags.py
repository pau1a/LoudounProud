import logging

from django import template
from django.core.cache import cache

register = template.Library()
logger = logging.getLogger(__name__)


@register.inclusion_tag("includes/_newsletter_signup.html", takes_context=True)
def newsletter_signup(context, placement_key):
    """Render a newsletter signup form for the given placement key.

    Usage: {% newsletter_signup "rail_primary" %}

    Fetches placement from DB (cached 5 min). Returns empty context
    if placement is inactive or missing, rendering nothing.
    """
    cache_key = f"newsletter_placement:{placement_key}"
    placement = cache.get(cache_key)

    if placement is None:
        from apps.newsletter.models import NewsletterPlacement

        try:
            placement = NewsletterPlacement.objects.get(key=placement_key, is_active=True)
            cache.set(cache_key, placement, timeout=300)
        except NewsletterPlacement.DoesNotExist:
            cache.set(cache_key, False, timeout=300)
            placement = False

    if not placement:
        return {"show": False}

    return {
        "show": True,
        "placement": placement,
        "request": context.get("request"),
    }
