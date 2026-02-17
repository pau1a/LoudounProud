from django.contrib import admin
from django.utils.html import format_html

from .models import AdCreative, AdImpression, AdSlot, AdvertiserLead


class AdCreativeInline(admin.TabularInline):
    model = AdCreative
    extra = 0
    fields = (
        "name",
        "provider",
        "creative_type",
        "start_datetime",
        "end_datetime",
        "priority",
        "is_active",
    )
    show_change_link = True


@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_name",
        "dimensions",
        "rotation_strategy",
        "active_creatives_count",
        "is_active",
        "updated",
    )
    list_filter = ("is_active", "rotation_strategy", "is_responsive")
    search_fields = ("name", "display_name", "location")
    list_editable = ("is_active",)
    fieldsets = [
        ("Basic Information", {"fields": ("name", "display_name", "location")}),
        ("Dimensions", {"fields": ("width", "height", "is_responsive")}),
        ("Rotation", {"fields": ("max_creatives", "rotation_strategy")}),
        ("Status", {"fields": ("is_active",)}),
    ]
    inlines = [AdCreativeInline]

    @admin.display(description="Size")
    def dimensions(self, obj):
        return f"{obj.width}\u00d7{obj.height}px"

    @admin.display(description="Active Creatives")
    def active_creatives_count(self, obj):
        count = obj.creatives.filter(is_active=True).count()
        colour = "green" if count > 0 else "#999"
        return format_html('<span style="color:{}">{}</span>', colour, count)


@admin.register(AdCreative)
class AdCreativeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slot",
        "provider",
        "creative_type",
        "preview_thumbnail",
        "date_range",
        "priority",
        "weight",
        "is_active",
        "impression_count",
        "click_count",
    )
    list_filter = ("provider", "creative_type", "is_active", "slot")
    search_fields = ("name", "slot__name")
    list_editable = ("priority", "is_active")
    date_hierarchy = "start_datetime"
    fieldsets = [
        ("Basic Information", {"fields": ("slot", "name", "provider", "creative_type")}),
        (
            "Content",
            {
                "fields": ("markup", "image", "image_alt", "target_url"),
                "description": "Provide markup (for HTML/AdSense) or image (for image ads).",
            },
        ),
        ("Scheduling", {"fields": ("start_datetime", "end_datetime")}),
        ("Prioritisation", {"fields": ("priority", "weight")}),
        ("Status", {"fields": ("is_active",)}),
    ]

    @admin.display(description="Preview")
    def preview_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:3px">',
                obj.image.url,
            )
        if obj.creative_type == "html":
            return format_html('<span style="color:#666">HTML</span>')
        return "-"

    @admin.display(description="Schedule")
    def date_range(self, obj):
        return f"{obj.start_datetime:%d/%m/%Y} \u2192 {obj.end_datetime:%d/%m/%Y}"

    @admin.display(description="Impressions")
    def impression_count(self, obj):
        return obj.events.filter(event_type="impression").count()

    @admin.display(description="Clicks")
    def click_count(self, obj):
        return obj.events.filter(event_type="click").count()


@admin.register(AdImpression)
class AdImpressionAdmin(admin.ModelAdmin):
    list_display = ("creative", "event_type", "timestamp", "ip_address")
    list_filter = ("event_type", "timestamp")
    search_fields = ("creative__name", "ip_address")
    date_hierarchy = "timestamp"
    readonly_fields = ("creative", "event_type", "timestamp", "user_agent", "ip_address", "referrer")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AdvertiserLead)
class AdvertiserLeadAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "name",
        "email",
        "budget_range",
        "campaign_goal",
        "status",
        "created",
    )
    list_filter = ("status", "budget_range", "campaign_goal")
    list_editable = ("status",)
    search_fields = ("name", "business_name", "email")
    date_hierarchy = "created"
    readonly_fields = (
        "name",
        "business_name",
        "email",
        "phone",
        "budget_range",
        "campaign_goal",
        "message",
        "created",
        "updated",
    )
    fieldsets = [
        ("Enquiry Details", {
            "fields": (
                "name",
                "business_name",
                "email",
                "phone",
                "budget_range",
                "campaign_goal",
                "message",
            ),
        }),
        ("Pipeline", {
            "fields": ("status", "notes"),
        }),
        ("Dates", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    ]
