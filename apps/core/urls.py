from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("api/track-view/", views.track_view, name="track_view"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
