from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [
    path("", views.subscribe, name="subscribe"),
    path("success/", views.subscribe_success, name="subscribe_success"),
    path("confirm/<uuid:token>/", views.confirm, name="confirm"),
]
