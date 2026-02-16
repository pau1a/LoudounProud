from django.db import models


class SiteSettings(models.Model):
    """Singleton model for site-wide configuration."""

    site_name = models.CharField(max_length=200, default="Loudoun Proud")
    tagline = models.CharField(
        max_length=300,
        default="Your weekly dose of what's happening in Ayrshire",
    )
    hero_headline = models.CharField(max_length=300, default="Welcome to Loudoun Proud")
    hero_subheadline = models.TextField(
        blank=True,
        default="Ayrshire's community newsletter — local stories, events, and the people who make this place special.",
    )
    hero_video_url = models.URLField(blank=True, help_text="YouTube or Vimeo embed URL for the hero video")
    hero_image = models.ImageField(upload_to="hero/", blank=True, help_text="Fallback hero background image")
    about_heading = models.CharField(max_length=300, default="About Loudoun Proud")
    about_text = models.TextField(blank=True)
    about_image = models.ImageField(upload_to="about/", blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)
    newsletter_day = models.CharField(max_length=20, default="Friday")
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        default="Loudoun Proud — your weekly Ayrshire community newsletter covering Kilmarnock, Troon, Ayr, and beyond.",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContentCard(models.Model):
    """Homepage featured content card in Axios/Morning Brew style."""

    LEAD_CHOICES = [
        ("why_it_matters", "Why it matters:"),
        ("whats_happening", "What's happening:"),
        ("the_big_picture", "The big picture:"),
        ("go_deeper", "Go deeper:"),
        ("icymi", "ICYMI:"),
        ("one_fun_thing", "One fun thing:"),
        ("custom", "Custom"),
    ]

    lead_style = models.CharField(max_length=30, choices=LEAD_CHOICES, default="whats_happening")
    custom_lead = models.CharField(max_length=100, blank=True, help_text="Used when lead_style is 'Custom'")
    headline = models.CharField(max_length=300)
    body_text = models.TextField()
    image = models.ImageField(upload_to="cards/", blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    link_url = models.URLField(blank=True)
    link_text = models.CharField(max_length=100, default="Go deeper →")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Feature as the dominant story")
    published_date = models.DateTimeField(blank=True, null=True, help_text="When this story was published (shown as timestamp)")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created"]
        verbose_name = "Content Card"
        verbose_name_plural = "Content Cards"

    def __str__(self):
        return self.headline

    @property
    def lead_phrase(self):
        if self.lead_style == "custom":
            return self.custom_lead
        return dict(self.LEAD_CHOICES).get(self.lead_style, "")

    @property
    def time_label(self):
        from django.utils import timezone
        if not self.published_date:
            return ""
        now = timezone.now()
        diff = now - self.published_date
        if diff.days == 0:
            hours = diff.seconds // 3600
            if hours < 1:
                return "Just now"
            if hours == 1:
                return "1 hour ago"
            return f"{hours} hours ago"
        if diff.days == 1:
            return "Yesterday"
        if diff.days < 7:
            return f"{diff.days} days ago"
        return "This week"
