from django.contrib import admin

from .models import ContentCard, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General", {"fields": ("site_name", "tagline", "newsletter_day", "email_address", "meta_description")}),
        ("Hero Section", {"fields": ("hero_headline", "hero_subheadline", "hero_video_url", "hero_image")}),
        ("About Page", {"fields": ("about_heading", "about_text", "about_image")}),
        ("Social Links", {"fields": ("facebook_url", "instagram_url", "twitter_url")}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContentCard)
class ContentCardAdmin(admin.ModelAdmin):
    list_display = ("headline", "lead_style", "sort_order", "is_active", "updated")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active", "lead_style")
    search_fields = ("headline", "body_text")
