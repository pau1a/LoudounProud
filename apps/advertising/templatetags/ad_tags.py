import logging

from django import template
from django.core.cache import cache
from django.utils import timezone
from django.utils.safestring import mark_safe

from ..models import AdSlot
from ..resolvers import SlotResolver

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def ad_slot(context, slot_name):
    """
    Render an ad slot by name.

    Usage: {% load ad_tags %}{% ad_slot "leaderboard" %}

    Returns rendered HTML from the resolved creative's provider renderer.
    On any error, returns empty string — never breaks the page.
    """
    try:
        now = timezone.now()
        bucket = int(now.timestamp() // 300)
        cache_key = f"ad_slot:{slot_name}:{bucket}"

        cached = cache.get(cache_key)
        if cached is not None:
            return mark_safe(cached)

        try:
            slot = AdSlot.objects.get(name=slot_name, is_active=True)
        except AdSlot.DoesNotExist:
            return ""

        request = context.get("request")
        resolver = SlotResolver(slot, request)
        html = resolver.resolve_and_render()

        cache.set(cache_key, html, timeout=300)
        return mark_safe(html)

    except Exception:
        logger.exception("Error rendering ad slot '%s'", slot_name)
        return ""
