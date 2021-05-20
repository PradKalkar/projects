from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("contribute/<str:page>", views.contribute, name="contribute"),
    path("newpage", views.newpage, name="newpage"),
    path("search", views.search, name="search")
]
