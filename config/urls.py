from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import StaticViewSitemap
from apps.core.views_admin import cdn_browser

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/cdn/", cdn_browser, name="cdn_browser"),
    path("admin/", admin.site.urls),
    path("subscribe/", include("apps.newsletter.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
