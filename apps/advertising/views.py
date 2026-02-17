import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import AdvertiserLeadForm
from .models import AdCreative, AdImpression

logger = logging.getLogger(__name__)


def track_impression(request):
    """Record an ad impression or click via AJAX beacon."""
    if request.method != "POST":
        return JsonResponse({"status": "error"}, status=405)

    creative_id = request.POST.get("creative_id")
    event_type = request.POST.get("event_type", "impression")

    if event_type not in ("impression", "click"):
        return JsonResponse({"status": "error"}, status=400)

    try:
        creative = AdCreative.objects.get(pk=creative_id)
    except (AdCreative.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"status": "error"}, status=404)

    AdImpression.objects.create(
        creative=creative,
        event_type=event_type,
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        ip_address=request.META.get("REMOTE_ADDR"),
        referrer=request.META.get("HTTP_REFERER", "")[:200],
    )
    return JsonResponse({"status": "ok"})


def _send_admin_notification(lead):
    """Notify admin of a new advertiser enquiry."""
    sales_email = getattr(settings, "SALES_EMAIL", None) or settings.DEFAULT_FROM_EMAIL
    subject = f"New advertiser enquiry — {lead.business_name}"
    body = (
        f"New enquiry from the Advertise page:\n\n"
        f"Name: {lead.name}\n"
        f"Business: {lead.business_name}\n"
        f"Email: {lead.email}\n"
        f"Phone: {lead.phone or '—'}\n"
        f"Budget: {lead.get_budget_range_display() or '—'}\n"
        f"Goal: {lead.get_campaign_goal_display() or '—'}\n"
        f"Message: {lead.message or '—'}\n\n"
        f"Manage leads in admin: /admin/advertising/advertiserlead/"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=None,
            recipient_list=[sales_email],
            fail_silently=True,
        )
    except Exception:
        logger.exception("Failed to send admin notification for lead %s", lead.pk)


def _send_auto_reply(lead):
    """Send a brief confirmation to the enquirer."""
    subject = "Thanks for your interest in Loudoun Proud"
    body = (
        f"Hi {lead.name},\n\n"
        f"Thanks for getting in touch about advertising with Loudoun Proud.\n\n"
        f"We've received your enquiry and will respond shortly.\n\n"
        f"— The Loudoun Proud Team"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=None,
            recipient_list=[lead.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception("Failed to send auto-reply to %s", lead.email)


def advertise(request: HttpRequest) -> HttpResponse:
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == "POST":
        form = AdvertiserLeadForm(request.POST)

        # Honeypot check
        if form.is_honeypot():
            if is_ajax:
                return JsonResponse({"ok": True, "message": "Thanks — we'll be in touch shortly."})
            return render(request, "advertising/advertise_thanks.html")

        if form.is_valid():
            lead = form.save()
            _send_admin_notification(lead)
            _send_auto_reply(lead)
            if is_ajax:
                return JsonResponse({"ok": True, "message": "Thanks — we'll be in touch shortly."})
            return render(request, "advertising/advertise_thanks.html")

        # Invalid form
        if is_ajax:
            errors = "; ".join(
                msg for field_errors in form.errors.values() for msg in field_errors
            )
            return JsonResponse({"ok": False, "message": errors}, status=400)
    else:
        form = AdvertiserLeadForm()

    return render(request, "advertising/advertise.html", {"form": form})
