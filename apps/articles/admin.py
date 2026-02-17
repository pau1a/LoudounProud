from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Article, Author, SlugRedirect


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ("name", "slug", "role_title", "bio", "photo"),
        }),
        ("Details", {
            "fields": ("location", "email", "is_staff_writer", "is_active"),
        }),
        ("Social Links", {
            "fields": ("website_url", "x_url", "linkedin_url"),
            "classes": ("collapse",),
        }),
    ]
    list_display = ("name", "role_title", "is_staff_writer", "is_active", "article_count")
    list_filter = ("is_active", "is_staff_writer")
    list_editable = ("is_active",)
    search_fields = ("name", "bio")
    prepopulated_fields = {"slug": ("name",)}

    def article_count(self, obj):
        return obj.articles.filter(status="published").count()
    article_count.short_description = "Published"


class SlugRedirectInline(admin.TabularInline):
    model = SlugRedirect
    extra = 0
    readonly_fields = ("old_slug", "created")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Info", {
            "fields": ("title", "slug", "deck", "category", "author", "byline_override"),
        }),
        ("Content", {
            "fields": ("body_markdown",),
            "description": "Write in Markdown. Headings, bold, italic, links, lists, and blockquotes are supported.",
        }),
        ("Hero Image", {
            "fields": ("hero_image", "hero_caption", "hero_alt"),
            "classes": ("collapse",),
        }),
        ("Publishing", {
            "fields": ("status", "published_at", "is_featured", "sort_order", "section_lead", "section_priority"),
        }),
        ("Sponsorship", {
            "fields": ("is_sponsored", "sponsor_name", "sponsor_url"),
            "classes": ("collapse",),
        }),
        ("Settings", {
            "fields": ("exclude_from_most_read",),
            "classes": ("collapse",),
        }),
        ("Preview", {
            "fields": ("body_html_preview", "preview_link"),
            "classes": ("collapse",),
        }),
    ]

    list_display = (
        "title", "category", "status", "author",
        "published_at", "is_featured", "section_lead", "sort_order", "section_priority", "updated",
    )
    list_filter = ("status", "category", "is_featured", "section_lead", "author", "is_sponsored")
    list_editable = ("status", "is_featured", "section_lead", "sort_order", "section_priority")
    search_fields = ("title", "deck", "body_markdown")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    readonly_fields = ("body_html_preview", "preview_link")
    inlines = [SlugRedirectInline]

    actions = ["publish_now", "archive", "mark_draft"]

    def body_html_preview(self, obj):
        if obj.body_html:
            return format_html('<div style="max-width:700px;font-family:serif;line-height:1.6">{}</div>', obj.body_html)
        return "—"
    body_html_preview.short_description = "Rendered preview"

    def preview_link(self, obj):
        if obj.pk and obj.slug:
            url = obj.get_absolute_url().replace(f"/{obj.slug}/", f"/{obj.slug}/preview/")
            return format_html('<a href="{}" target="_blank">Open preview ↗</a>', url)
        return "Save first to generate preview link"
    preview_link.short_description = "Preview"

    @admin.action(description="Publish selected articles now")
    def publish_now(self, request, queryset):
        updated = queryset.update(status="published", published_at=timezone.now())
        self.message_user(request, f"{updated} article(s) published.")

    @admin.action(description="Archive selected articles")
    def archive(self, request, queryset):
        updated = queryset.update(status="archived")
        self.message_user(request, f"{updated} article(s) archived.")

    @admin.action(description="Revert to draft")
    def mark_draft(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} article(s) reverted to draft.")

    class Media:
        css = {"all": ()}
        js = ()
