from django.contrib import admin
from django.db.models import Count, Q

from .models import NewsletterEvent, NewsletterPlacement, Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "source_placement", "date_subscribed", "is_confirmed", "is_active")
    list_filter = ("is_confirmed", "is_active", "source_placement")
    search_fields = ("email", "first_name")
    readonly_fields = ("confirmation_token", "date_subscribed")


@admin.register(NewsletterPlacement)
class NewsletterPlacementAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "style", "is_active", "submissions_count", "impressions_count")
    list_editable = ("is_active",)
    list_filter = ("is_active", "style")
    search_fields = ("key", "title")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _submissions=Count("events", filter=Q(events__event_type="submission")),
            _impressions=Count("events", filter=Q(events__event_type="impression")),
        )

    def submissions_count(self, obj):
        return obj._submissions
    submissions_count.short_description = "Submissions"
    submissions_count.admin_order_field = "_submissions"

    def impressions_count(self, obj):
        return obj._impressions
    impressions_count.short_description = "Impressions"
    impressions_count.admin_order_field = "_impressions"


@admin.register(NewsletterEvent)
class NewsletterEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "placement", "created")
    list_filter = ("event_type", "placement")
    date_hierarchy = "created"
    readonly_fields = ("placement", "event_type", "ip_hash", "created")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
