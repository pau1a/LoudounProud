from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.advertising.views import advertise
from apps.articles.views import author_detail, section_page, town_page
from apps.core.sitemaps import ArticleSitemap, SectionSitemap, StaticViewSitemap, TownSitemap
from apps.core.views_admin import cdn_browser

sitemaps = {
    "static": StaticViewSitemap,
    "sections": SectionSitemap,
    "articles": ArticleSitemap,
    "towns": TownSitemap,
}

urlpatterns = [
    path("admin/cdn/", cdn_browser, name="cdn_browser"),
    path("admin/", admin.site.urls),
    path("subscribe/", include("apps.newsletter.urls")),
    path("advertise/", advertise, name="advertise"),
    path("ads/", include("apps.advertising.urls")),
    path("article/", include("apps.articles.urls")),
    path("authors/<slug:slug>/", author_detail, name="author_detail"),
    path("towns/<slug:slug>/", town_page, name="town_page"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("<slug:section>/", section_page, name="section_page"),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
