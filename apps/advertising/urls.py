from django.urls import path

from . import views

app_name = "advertising"

urlpatterns = [
    path("track/", views.track_impression, name="track_impression"),
]
