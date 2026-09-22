"""URL configuration for the Hello World project."""

from django.urls import include, path

urlpatterns = [path("", include("hello.urls"))]
