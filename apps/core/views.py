from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.articles.models import Article


def home(request: HttpRequest) -> HttpResponse:
    all_articles = Article.objects.filter(status="published")
    featured = all_articles.filter(is_featured=True).first()
    if featured:
        cards = all_articles.exclude(pk=featured.pk)
    else:
        cards = all_articles
    return render(request, "core/home.html", {
        "featured": featured,
        "cards": cards,
        "active_section": None,
    })


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")


@csrf_exempt
@require_POST
def track_view(request):
    """Record an article view via JS beacon."""
    card_id = request.POST.get("card_id")
    if not card_id:
        return JsonResponse({"status": "error"}, status=400)

    try:
        int(card_id)
    except (ValueError, TypeError):
        return JsonResponse({"status": "error"}, status=400)

    from .most_read import record_view

    ip = request.META.get("REMOTE_ADDR", "")
    ua = request.META.get("HTTP_USER_AGENT", "")
    record_view(card_id, ip, ua)
    return JsonResponse({"status": "ok"})


def robots_txt(request: HttpRequest) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
