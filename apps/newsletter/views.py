import logging
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .forms import SubscribeForm
from .models import NewsletterEvent, NewsletterPlacement, Subscriber

logger = logging.getLogger(__name__)


def _record_event(placement_key, event_type, ip=""):
    """Record a newsletter event for tracking."""
    try:
        placement = NewsletterPlacement.objects.filter(key=placement_key).first()
        NewsletterEvent.objects.create(
            placement=placement,
            event_type=event_type,
            ip_hash=NewsletterEvent.hash_ip(ip) if ip else "",
        )
    except Exception:
        logger.exception("Failed to record newsletter event")


def _send_confirmation_email(subscriber, request):
    """Send double opt-in confirmation email."""
    confirm_url = request.build_absolute_uri(f"/subscribe/confirm/{subscriber.confirmation_token}/")
    subject = f"Confirm your subscription to {settings.DEFAULT_FROM_EMAIL.split('@')[-1] if '@' in getattr(settings, 'DEFAULT_FROM_EMAIL', '') else 'Loudoun Proud'}"
    subject = "Confirm your Loudoun Proud subscription"
    body = (
        f"Thanks for subscribing!\n\n"
        f"Please confirm your email by clicking the link below:\n\n"
        f"{confirm_url}\n\n"
        f"If you didn't sign up, you can safely ignore this email.\n\n"
        f"— Loudoun Proud"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[subscriber.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception("Failed to send confirmation email to %s", subscriber.email)


def subscribe(request: HttpRequest) -> HttpResponse:
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if request.method == "POST":
        form = SubscribeForm(request.POST)
        placement_key = request.POST.get("placement", "")
        ip = request.META.get("REMOTE_ADDR", "")

        # Honeypot check — silently reject bots
        if form.is_honeypot():
            if is_ajax:
                return JsonResponse({"status": "ok", "message": "Thanks! Check your inbox."})
            return redirect("newsletter:subscribe_success")

        # Check for existing unconfirmed re-subscribe
        email = request.POST.get("email", "").lower().strip()
        existing = Subscriber.objects.filter(email=email, is_confirmed=False).first()
        if existing:
            existing.confirmation_token = uuid.uuid4()
            existing.first_name = request.POST.get("first_name", existing.first_name)
            existing.source_placement = placement_key or existing.source_placement
            existing.save()
            _send_confirmation_email(existing, request)
            _record_event(placement_key, "submission", ip)
            if is_ajax:
                placement = NewsletterPlacement.objects.filter(key=placement_key).first()
                msg = placement.success_message if placement and placement.success_message else "Check your inbox to confirm."
                return JsonResponse({"status": "ok", "message": msg})
            return redirect("newsletter:subscribe_success")

        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.source_placement = placement_key
            subscriber.save()
            _send_confirmation_email(subscriber, request)
            _record_event(placement_key, "submission", ip)
            if is_ajax:
                placement = NewsletterPlacement.objects.filter(key=placement_key).first()
                msg = placement.success_message if placement and placement.success_message else "Check your inbox to confirm."
                return JsonResponse({"status": "ok", "message": msg})
            return redirect("newsletter:subscribe_success")

        # Form invalid
        if is_ajax:
            errors = "; ".join(
                msg for field_errors in form.errors.values() for msg in field_errors
            )
            return JsonResponse({"status": "error", "message": errors}, status=400)

    else:
        form = SubscribeForm()

    return render(request, "newsletter/subscribe.html", {"form": form})


def subscribe_success(request: HttpRequest) -> HttpResponse:
    return render(request, "newsletter/subscribe_success.html")


def confirm(request: HttpRequest, token: str) -> HttpResponse:
    try:
        subscriber = Subscriber.objects.get(confirmation_token=token)
        if not subscriber.is_confirmed:
            subscriber.is_confirmed = True
            subscriber.save()
            # Track confirmation
            _record_event(subscriber.source_placement, "confirmation")
        confirmed = True
    except Subscriber.DoesNotExist:
        confirmed = False

    return render(request, "newsletter/confirm.html", {"confirmed": confirmed})
