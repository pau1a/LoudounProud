import hashlib
import uuid

from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source_placement = models.CharField(max_length=100, blank=True, help_text="Placement key where this subscriber signed up")

    class Meta:
        ordering = ["-date_subscribed"]

    def __str__(self):
        return self.email


STYLE_CHOICES = [
    ("compact", "Compact (email + button)"),
    ("full", "Full (headline + description + form)"),
    ("inline", "Inline (horizontal bar)"),
]


class NewsletterPlacement(models.Model):
    key = models.SlugField(unique=True, help_text="Unique identifier, e.g. rail_primary, footer_global")
    title = models.CharField(max_length=200, help_text="Headline copy")
    description = models.TextField(blank=True, help_text="Value proposition text")
    cta_text = models.CharField(max_length=50, default="Subscribe")
    incentive_text = models.CharField(max_length=200, blank=True, help_text="e.g. 'No spam. Unsubscribe anytime.'")
    success_message = models.CharField(max_length=300, blank=True, default="Check your inbox to confirm your subscription.")
    is_active = models.BooleanField(default=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default="compact")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "Newsletter Placement"
        verbose_name_plural = "Newsletter Placements"

    def __str__(self):
        return f"{self.key} — {self.title}"


EVENT_TYPE_CHOICES = [
    ("impression", "Impression"),
    ("submission", "Submission"),
    ("confirmation", "Confirmation"),
]


class NewsletterEvent(models.Model):
    placement = models.ForeignKey(
        NewsletterPlacement,
        on_delete=models.CASCADE,
        related_name="events",
        null=True,
        blank=True,
    )
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    ip_hash = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Newsletter Event"
        verbose_name_plural = "Newsletter Events"

    def __str__(self):
        placement_key = self.placement.key if self.placement else "unknown"
        return f"{self.event_type} — {placement_key}"

    @staticmethod
    def hash_ip(ip):
        """Hash IP for privacy-safe dedup tracking."""
        return hashlib.md5(ip.encode(), usedforsecurity=False).hexdigest()[:16]
