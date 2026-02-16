import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SubscribeForm
from .models import Subscriber


def subscribe(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Handle both the full form and the simple email-only form (hero/footer)
        form = SubscribeForm(request.POST)

        # Check if this is an unconfirmed re-subscribe
        email = request.POST.get("email", "").lower().strip()
        existing = Subscriber.objects.filter(email=email, is_confirmed=False).first()
        if existing:
            # Reset token and let them re-confirm
            existing.confirmation_token = uuid.uuid4()
            existing.first_name = request.POST.get("first_name", existing.first_name)
            existing.save()
            return redirect("newsletter:subscribe_success")

        if form.is_valid():
            form.save()
            return redirect("newsletter:subscribe_success")
    else:
        form = SubscribeForm()

    return render(request, "newsletter/subscribe.html", {"form": form})


def subscribe_success(request: HttpRequest) -> HttpResponse:
    return render(request, "newsletter/subscribe_success.html")


def confirm(request: HttpRequest, token: str) -> HttpResponse:
    try:
        subscriber = Subscriber.objects.get(confirmation_token=token)
        subscriber.is_confirmed = True
        subscriber.save()
        confirmed = True
    except Subscriber.DoesNotExist:
        confirmed = False

    return render(request, "newsletter/confirm.html", {"confirmed": confirmed})
