from django import template

register = template.Library()


@register.inclusion_tag("includes/_most_read.html")
def most_read(window="24h", count=5):
    """
    Render the Most Read list for a given time window.

    Usage: {% load most_read_tags %}{% most_read "24h" 5 %}
    Windows: "3h" (trending), "24h" (today), "7d" (this week)
    """
    from apps.core.most_read import get_most_read

    count = int(count)
    cards = get_most_read(window=window, count=count)
    return {"cards": cards, "window": window}
