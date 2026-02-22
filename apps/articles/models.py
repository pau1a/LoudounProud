import markdown
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


STATUS_CHOICES = [
    ("draft", "Draft"),
    ("scheduled", "Scheduled"),
    ("published", "Published"),
    ("archived", "Archived"),
]

CATEGORY_CHOICES = [
    ("news", "News"),
    ("business", "Business"),
    ("community", "Community"),
    ("sport", "Sport"),
    ("culture", "Culture"),
]

VALID_SECTIONS = {key for key, _ in CATEGORY_CHOICES}

COUNCIL_AREA_CHOICES = [
    ("east_ayrshire", "East Ayrshire"),
    ("north_ayrshire", "North Ayrshire"),
    ("south_ayrshire", "South Ayrshire"),
]

SECTION_DESCRIPTIONS = {
    "news": "Breaking stories, council updates, and the issues shaping Ayrshire.",
    "business": "Local companies, hiring, development, and economic activity across Ayrshire.",
    "community": "The people, places, and initiatives that bring our communities together.",
    "sport": "Match reports, results, and the stories behind Ayrshire's sporting life.",
    "culture": "Arts, heritage, events, and the creative pulse of the region.",
}


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Display name")
    slug = models.SlugField(unique=True)
    role_title = models.CharField(max_length=100, blank=True, help_text="e.g. Editor, Contributor, Sports Reporter")
    bio = models.TextField(blank=True, help_text="Short bio — aim for 1–2 sentences")
    photo = models.ImageField(upload_to="authors/", blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="e.g. Ayrshire")
    email = models.EmailField(blank=True)
    is_staff_writer = models.BooleanField(default=True, verbose_name="Staff", help_text="Staff writer vs external contributor")
    is_active = models.BooleanField(default=True, help_text="Inactive authors are hidden from listings but keep historical attribution")

    website_url = models.URLField(blank=True, verbose_name="Website")
    x_url = models.URLField(blank=True, verbose_name="X / Twitter")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"slug": self.slug})

    @property
    def short_bio(self):
        """Bio truncated to 280 chars for card display."""
        if len(self.bio) <= 280:
            return self.bio
        return self.bio[:277].rsplit(" ", 1)[0] + "..."


class Town(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    council_area = models.CharField(max_length=20, choices=COUNCIL_AREA_CHOICES)
    description = models.TextField(blank=True, help_text="SEO description for the town page")
    sort_order = models.IntegerField(default=0, help_text="Display order within council area")

    class Meta:
        ordering = ["council_area", "sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("town_page", kwargs={"slug": self.slug})


class Article(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    deck = models.CharField(max_length=500, blank=True, help_text="Standfirst / summary shown below the headline")
    body_markdown = models.TextField(blank=True, verbose_name="Body (Markdown)")
    body_html = models.TextField(editable=False, blank=True)

    main_image = models.ImageField(upload_to="articles/", blank=True, help_text="Primary article image — used on cards and at the top of the article page")
    hero_image = models.ImageField(upload_to="articles/", blank=True)
    hero_caption = models.CharField(max_length=200, blank=True)
    hero_alt = models.CharField(max_length=200, blank=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="news")
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True, help_text="Publish date (or scheduled date)")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_featured = models.BooleanField(default=False, help_text="Feature as the lead story on the homepage")
    byline_override = models.CharField(
        max_length=200,
        blank=True,
        help_text="Override the author byline (e.g. 'Staff Writer', 'From the newsroom')",
    )

    is_sponsored = models.BooleanField(default=False)
    sponsor_name = models.CharField(max_length=200, blank=True)
    sponsor_url = models.URLField(blank=True)

    exclude_from_most_read = models.BooleanField(
        default=False,
        help_text="Hide from Most Read lists (legal, sensitive, sponsored)",
    )
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first on the homepage")
    section_lead = models.BooleanField(default=False, help_text="Feature as the lead story on its section page")
    section_priority = models.IntegerField(default=0, help_text="Higher number = appears earlier on section page")
    homepage_secondary = models.BooleanField(default=False, help_text="Show in the secondary authority band on the homepage")
    secondary_priority = models.IntegerField(default=0, help_text="Higher number = appears earlier in the secondary band")
    feature_frame = models.BooleanField(default=False, help_text="Add subtle keyline frame to featured image (use sparingly)")
    towns = models.ManyToManyField("Town", blank=True, related_name="articles")

    class Meta:
        ordering = ["sort_order", "-created"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title on first save
        if not self.slug:
            base_slug = slugify(self.title)[:290]
            slug = base_slug
            n = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug

        # Track slug changes on published articles for redirects
        if self.pk and self.status == "published":
            try:
                old = Article.objects.get(pk=self.pk)
                if old.slug and old.slug != self.slug:
                    SlugRedirect.objects.get_or_create(
                        old_slug=old.slug,
                        defaults={"article": self},
                    )
            except Article.DoesNotExist:
                pass

        # Render markdown → HTML
        if self.body_markdown:
            self.body_html = markdown.markdown(
                self.body_markdown,
                extensions=["extra", "smarty", "toc"],
            )
        else:
            self.body_html = ""

        # Auto-set published_at when publishing
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})

    @property
    def time_label(self):
        if not self.published_at:
            return ""
        now = timezone.now()
        diff = now - self.published_at
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
        return self.published_at.strftime("%-d %b %Y")

    @property
    def meta_description(self):
        if self.deck:
            return self.deck[:160]
        # Strip HTML and take first 160 chars of body
        from django.utils.html import strip_tags
        plain = strip_tags(self.body_html)
        return plain[:160] if plain else ""

    @property
    def byline_display(self):
        """Rendered byline text following priority: override > author name + role."""
        if self.byline_override:
            return self.byline_override
        if self.author:
            name = self.author.name
            if self.author.role_title:
                return f"{name}, {self.author.role_title}"
            return name
        return ""

    @property
    def headline(self):
        """Alias for template compatibility with ContentCard."""
        return self.title

    @property
    def lead_phrase(self):
        """Category label for card display."""
        return self.get_category_display()

    @property
    def body_text(self):
        """Short summary for card display."""
        return self.deck

    @property
    def display_image(self):
        """Preferred image for rendering: main_image first, then hero_image."""
        return self.main_image or self.hero_image

    @property
    def link_text(self):
        return "Read more →"

    @property
    def link_url(self):
        return self.get_absolute_url()


class SlugRedirect(models.Model):
    old_slug = models.SlugField(max_length=300, unique=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="slug_redirects")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Slug Redirect"
        verbose_name_plural = "Slug Redirects"

    def __str__(self):
        return f"{self.old_slug} → {self.article.slug}"
