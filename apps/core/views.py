from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import ContentCard, SiteSettings


def home(request: HttpRequest) -> HttpResponse:
    all_cards = ContentCard.objects.filter(is_active=True)
    featured = all_cards.filter(is_featured=True).first()
    if featured:
        cards = all_cards.exclude(pk=featured.pk)
    else:
        cards = all_cards
    return render(request, "core/home.html", {
        "featured": featured,
        "cards": cards,
    })


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")


def robots_txt(request: HttpRequest) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
