from django.urls import path

from . import views

app_name = "frontend"
urlpatterns = [
    path(r"templates/", views.template_list_view, name="template-list"),
    path(
        r"templates/<int:template_pk>",
        views.template_detail_view,
        name="template-detail",
    ),
    path(
        r"item-template/<int:section_pk>/create",
        views.item_template_create_view,
        name="item-template-create",
    ),
    path(
        r"item-template/<int:item_pk>/detail",
        views.item_template_detail_view,
        name="item-template-detail",
    ),
    path(
        r"item-template/<int:item_pk>/delete",
        views.item_template_delete_view,
        name="item-template-delete",
    ),
    path(
        r"item-template/<int:item_pk>/edit",
        views.item_template_edit_view,
        name="item-template-edit",
    ),
    path(
        r"event/<int:template_pk>/create", views.event_create_view, name="event-create"
    ),
    path(r"event/<int:event_pk>/detail", views.event_detail_view, name="event-detail"),
    path(
        r"event/<int:event_pk>/toggle-open",
        views.event_toggle_open_view,
        name="event-toggle-open",
    ),
    path(
        r"item/<int:item_pk>/toggle-status",
        views.item_toggle_status_view,
        name="item-toggle-status",
    ),
    path(r"item/<int:section_pk>", views.item_list_view, name="item-list"),
    path(
        r"section/<int:section_pk>/toggle-display-closed-items",
        views.section_toggle_display_closed_items_view,
        name="section-toggle-display-closed-items",
    ),
    path(r"", views.dashboard_view, name="dashboard"),
]
