from django.contrib import admin
from django.urls import reverse

from .models import ContentCard, SiteSettings


# Inject CDN Browser into the admin index app list
_original_get_app_list = admin.AdminSite.get_app_list


def _patched_get_app_list(self, request, app_label=None):
    app_list = _original_get_app_list(self, request, app_label=app_label)
    if app_label is None:
        app_list.append({
            "name": "CDN Browser",
            "app_label": "cdn_browser",
            "app_url": reverse("cdn_browser"),
            "has_module_perms": True,
            "models": [{
                "name": "Browse & manage files",
                "object_name": "CDNBrowser",
                "admin_url": reverse("cdn_browser"),
                "view_only": True,
            }],
        })
    return app_list


admin.AdminSite.get_app_list = _patched_get_app_list


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
    list_display = ("headline", "lead_style", "sort_order", "is_featured", "is_active", "published_date", "updated")
    list_editable = ("sort_order", "is_featured", "is_active")
    list_filter = ("is_active", "is_featured", "lead_style")
    search_fields = ("headline", "body_text")
