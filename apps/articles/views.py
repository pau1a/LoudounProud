from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    CATEGORY_CHOICES,
    SECTION_DESCRIPTIONS,
    VALID_SECTIONS,
    Article,
    Author,
    SlugRedirect,
    Town,
)


def article_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Public article detail page — published articles only."""
    article = (
        Article.objects.filter(slug=slug, status="published")
        .select_related("author")
        .first()
    )
    if article:
        return render(request, "articles/detail.html", {"article": article})

    # Check for slug redirect (old URL → new slug)
    slug_redirect = SlugRedirect.objects.filter(old_slug=slug).select_related("article").first()
    if slug_redirect and slug_redirect.article.status == "published":
        return redirect(slug_redirect.article.get_absolute_url(), permanent=True)

    # 404
    get_object_or_404(Article, slug=slug, status="published")


@staff_member_required
def article_preview(request: HttpRequest, slug: str) -> HttpResponse:
    """Staff-only preview for draft/scheduled articles."""
    article = get_object_or_404(Article.objects.select_related("author"), slug=slug)
    return render(request, "articles/detail.html", {
        "article": article,
        "is_preview": True,
    })


def section_page(request: HttpRequest, section: str) -> HttpResponse:
    """Section front page — curated layout mirroring homepage grammar."""
    if section not in VALID_SECTIONS:
        from django.http import Http404
        raise Http404

    section_display = dict(CATEGORY_CHOICES)[section]
    section_description = SECTION_DESCRIPTIONS.get(section, "")

    articles = (
        Article.objects.filter(category=section, status="published")
        .select_related("author")
        .order_by("-section_lead", "-section_priority", "-published_at")
    )

    # Resolve lead story
    lead = articles.first()
    if not lead:
        return render(request, "articles/section.html", {
            "section_key": section,
            "section_display": section_display,
            "section_description": section_description,
            "active_section": section,
            "lead": None,
            "secondaries": [],
            "articles": None,
        })

    remaining = articles.exclude(pk=lead.pk)

    # Secondary tier: next 3 articles
    secondaries = list(remaining[:3])
    secondary_pks = [a.pk for a in secondaries]

    # Grid: everything else, paginated
    grid_qs = remaining.exclude(pk__in=secondary_pks)
    paginator = Paginator(grid_qs, 12)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "articles/section.html", {
        "section_key": section,
        "section_display": section_display,
        "section_description": section_description,
        "active_section": section,
        "lead": lead,
        "secondaries": secondaries,
        "articles": page,
    })


def town_page(request: HttpRequest, slug: str) -> HttpResponse:
    """Town landing page — articles tagged with this town."""
    town = get_object_or_404(Town, slug=slug)

    articles = (
        Article.objects.filter(towns=town, status="published")
        .select_related("author")
        .order_by("-published_at")
    )

    lead = articles.first()
    if not lead:
        return render(request, "articles/town.html", {
            "town": town,
            "lead": None,
            "secondaries": [],
            "articles": None,
            "active_section": None,
        })

    remaining = articles.exclude(pk=lead.pk)
    secondaries = list(remaining[:3])
    secondary_pks = [a.pk for a in secondaries]

    grid_qs = remaining.exclude(pk__in=secondary_pks)
    paginator = Paginator(grid_qs, 12)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "articles/town.html", {
        "town": town,
        "lead": lead,
        "secondaries": secondaries,
        "articles": page,
        "active_section": None,
    })


def author_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Author page with bio and paginated article list."""
    author = get_object_or_404(Author, slug=slug)
    articles_qs = (
        Article.objects.filter(author=author, status="published")
        .order_by("-published_at")
    )
    paginator = Paginator(articles_qs, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "articles/author.html", {
        "author": author,
        "articles": page,
    })
