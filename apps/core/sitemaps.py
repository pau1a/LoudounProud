from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.articles.models import Article


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["core:home", "core:about", "newsletter:subscribe", "advertise"]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Article.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated
