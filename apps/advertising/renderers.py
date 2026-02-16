from abc import ABC, abstractmethod

from django.utils.html import escape


def get_renderer(creative):
    """Factory: return the appropriate renderer for a creative's provider."""
    renderer_map = {
        "adsense": AdsenseRenderer,
        "direct": DirectRenderer,
        "house": HouseRenderer,
        "sponsor": SponsorRenderer,
    }
    cls = renderer_map.get(creative.provider, HouseRenderer)
    return cls(creative)


class BaseRenderer(ABC):
    def __init__(self, creative):
        self.creative = creative

    @abstractmethod
    def render(self, request):
        """Return HTML string for this creative."""


class AdsenseRenderer(BaseRenderer):
    """Render Google AdSense script block stored in markup field."""

    def render(self, request):
        return self.creative.markup


class DirectRenderer(BaseRenderer):
    """Render direct-sold image ad with click-through link."""

    def render(self, request):
        c = self.creative
        if not c.image:
            return ""
        alt = escape(c.image_alt)
        return (
            f'<a href="{escape(c.target_url)}" target="_blank" rel="noopener sponsored"'
            f' data-creative-id="{c.pk}">'
            f'<img src="{c.image.url}" alt="{alt}"'
            f' width="{c.slot.width}" height="{c.slot.height}" loading="lazy">'
            f"</a>"
        )


class HouseRenderer(BaseRenderer):
    """Render internal house ads — image or HTML based on creative_type."""

    def render(self, request):
        c = self.creative
        if c.creative_type == "image" and c.image:
            alt = escape(c.image_alt)
            if c.target_url:
                return (
                    f'<a href="{escape(c.target_url)}" data-creative-id="{c.pk}">'
                    f'<img src="{c.image.url}" alt="{alt}"'
                    f' width="{c.slot.width}" height="{c.slot.height}" loading="lazy">'
                    f"</a>"
                )
            return (
                f'<img src="{c.image.url}" alt="{alt}"'
                f' width="{c.slot.width}" height="{c.slot.height}" loading="lazy"'
                f' data-creative-id="{c.pk}">'
            )
        if c.markup:
            return c.markup
        return ""


class SponsorRenderer(BaseRenderer):
    """Render sponsor/partner ad with 'Sponsored by' label."""

    def render(self, request):
        c = self.creative
        if not c.image:
            return ""
        alt = escape(c.image_alt)
        return (
            f'<div class="sponsor-ad" data-creative-id="{c.pk}">'
            f'<span class="sponsor-ad__label">Sponsored by</span>'
            f'<a href="{escape(c.target_url)}" target="_blank" rel="noopener sponsored">'
            f'<img src="{c.image.url}" alt="{alt}"'
            f' width="{c.slot.width}" height="{c.slot.height}" loading="lazy">'
            f"</a></div>"
        )
