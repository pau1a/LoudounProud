from django.contrib import admin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "date_subscribed", "is_confirmed", "is_active")
    list_filter = ("is_confirmed", "is_active")
    search_fields = ("email", "first_name")
    readonly_fields = ("confirmation_token", "date_subscribed")
