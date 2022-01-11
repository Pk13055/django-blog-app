from django.urls import path

from .views import (
    BlogCreateView,
    BlogDeleteView,
    BlogListView,
    BlogUpdateView,
    EntryAuthorListView,
    EntryCreateView,
    EntryDeleteView,
    EntryDetailView,
    EntryListView,
    EntryUpdateView,
)


app_name = "blog"


urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("new/", BlogCreateView.as_view(), name="blog_create"),
    path("edit/<int:pk>", BlogUpdateView.as_view(), name="blog_update"),
    path("delete/<int:pk>", BlogDeleteView.as_view(), name="blog_delete"),
    path("entries/<int:pk>", EntryListView.as_view(), name="entry_list"),
    path(
        "entries/author/<int:author_id>",
        EntryAuthorListView.as_view(),
        name="entry_author_list",
    ),
    path(
        "entries/<int:blog_id>/entry/new",
        EntryCreateView.as_view(),
        name="entry_create",
    ),
    path(
        "entries/<int:blog_id>/entry/<int:pk>",
        EntryDetailView.as_view(),
        name="entry_details",
    ),
    path(
        "entries/<int:blog_id>/entry/<int:pk>/delete",
        EntryDeleteView.as_view(),
        name="entry_delete",
    ),
    path(
        "entries/<int:blog_id>/entry/<int:pk>/edit",
        EntryUpdateView.as_view(),
        name="entry_update",
    ),
]
