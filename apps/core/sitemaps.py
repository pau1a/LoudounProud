from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.articles.models import Article, CATEGORY_CHOICES, Town


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["core:home", "core:about", "newsletter:subscribe", "advertise"]

    def location(self, item):
        return reverse(item)


class SectionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return [key for key, _ in CATEGORY_CHOICES]

    def location(self, item):
        return reverse("section_page", kwargs={"section": item})


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Article.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated


class TownSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Town.objects.all()

    def location(self, item):
        return item.get_absolute_url()
