from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("<slug:slug>/preview/", views.article_preview, name="preview"),
    path("<slug:slug>/", views.article_detail, name="detail"),
]
