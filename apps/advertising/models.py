import logging

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class AdSlot(models.Model):
    """Physical ad placement on the site."""

    ROTATION_CHOICES = [
        ("priority", "Priority-first"),
        ("weighted", "Weighted random"),
        ("random", "Random"),
        ("sequential", "Sequential"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique key used in template tags, e.g. 'leaderboard'",
    )
    display_name = models.CharField(max_length=200)
    location = models.CharField(
        max_length=200,
        help_text="Human-readable location, e.g. 'Below lead story'",
    )
    width = models.PositiveIntegerField(help_text="Width in pixels")
    height = models.PositiveIntegerField(help_text="Height in pixels")
    is_responsive = models.BooleanField(
        default=False,
        help_text="Allow fluid sizing on mobile",
    )
    max_creatives = models.PositiveIntegerField(
        default=1,
        help_text="Maximum creatives in rotation pool",
    )
    rotation_strategy = models.CharField(
        max_length=20,
        choices=ROTATION_CHOICES,
        default="priority",
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ad Slot"
        verbose_name_plural = "Ad Slots"
        ordering = ["name"]

    def __str__(self):
        return f"{self.display_name} ({self.name})"

    def get_eligible_creatives(self):
        """Return active creatives within their scheduled date range."""
        now = timezone.now()
        return self.creatives.filter(
            is_active=True,
            start_datetime__lte=now,
            end_datetime__gte=now,
        ).order_by("-priority", "-weight")


class AdCreative(models.Model):
    """Content that displays in an ad slot."""

    PROVIDER_CHOICES = [
        ("adsense", "Google AdSense"),
        ("direct", "Direct Sale"),
        ("house", "House Ad"),
        ("sponsor", "Sponsor"),
    ]

    TYPE_CHOICES = [
        ("image", "Image"),
        ("html", "HTML / Script"),
        ("text", "Text Only"),
    ]

    slot = models.ForeignKey(
        AdSlot,
        on_delete=models.CASCADE,
        related_name="creatives",
    )
    name = models.CharField(max_length=200, help_text="Internal reference name")
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default="house",
    )
    creative_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="image",
    )

    # Content fields
    markup = models.TextField(
        blank=True,
        help_text="HTML/JavaScript code (for AdSense or custom HTML creatives)",
    )
    image = models.ImageField(
        upload_to="ads/",
        blank=True,
        help_text="Image file for direct/house/sponsor ads",
    )
    image_alt = models.CharField(max_length=200, blank=True)
    target_url = models.URLField(
        blank=True,
        help_text="Click-through URL",
    )

    # Scheduling
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(help_text="When to stop showing this creative")

    # Prioritisation
    priority = models.IntegerField(
        default=0,
        help_text="Higher number = higher priority (0–100)",
    )
    weight = models.PositiveIntegerField(
        default=1,
        help_text="Relative weight for weighted rotation (1–100)",
    )

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ad Creative"
        verbose_name_plural = "Ad Creatives"
        ordering = ["-priority", "name"]

    def __str__(self):
        return f"{self.name} ({self.slot.name})"

    def clean(self):
        if self.creative_type == "image" and not self.image:
            raise ValidationError("Image is required for image-type creatives.")
        if self.creative_type == "html" and not self.markup:
            raise ValidationError("Markup is required for HTML-type creatives.")
        if self.end_datetime and self.start_datetime and self.end_datetime <= self.start_datetime:
            raise ValidationError("End date must be after start date.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._invalidate_slot_cache()

    def delete(self, *args, **kwargs):
        self._invalidate_slot_cache()
        super().delete(*args, **kwargs)

    def _invalidate_slot_cache(self):
        """Clear cached slot resolution so changes appear promptly."""
        now = timezone.now()
        for i in range(3):
            bucket = int(now.timestamp() // 300) - i
            cache.delete(f"ad_slot:{self.slot.name}:{bucket}")


class AdImpression(models.Model):
    """Track ad impressions and clicks."""

    EVENT_CHOICES = [
        ("impression", "Impression"),
        ("click", "Click"),
    ]

    creative = models.ForeignKey(
        AdCreative,
        on_delete=models.CASCADE,
        related_name="events",
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
        default="impression",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    referrer = models.URLField(blank=True)

    class Meta:
        verbose_name = "Ad Impression"
        verbose_name_plural = "Ad Impressions"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["creative", "event_type", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.event_type} — {self.creative.name} — {self.timestamp:%Y-%m-%d %H:%M}"
