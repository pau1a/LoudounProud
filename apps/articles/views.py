from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Article, Author, SlugRedirect


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
