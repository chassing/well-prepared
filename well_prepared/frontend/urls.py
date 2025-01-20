from django.urls import path

from . import views

app_name = "frontend"
urlpatterns = [
    path(r"empty/", views.empty, name="empty"),
    #
    # Templates
    #
    path(r"template/", views.template_list, name="template-list"),
    path(r"template/create", views.template_create, name="template-create"),
    path(r"template/import", views.template_import, name="template-import"),
    path(r"template/<int:template_pk>", views.template_detail, name="template-detail"),
    path(r"template/<int:template_pk>/edit", views.template_edit, name="template-edit"),
    path(
        r"template/<int:template_pk>/delete",
        views.template_delete,
        name="template-delete",
    ),
    path(
        r"template/<int:template_pk>/export",
        views.template_export,
        name="template-export",
    ),
    path(
        r"template/<int:template_pk>/category/create",
        views.template_category_create,
        name="template-category-create",
    ),
    path(
        r"template-category/<int:category_pk>/item/create",
        views.template_item_create,
        name="template-item-create",
    ),
    path(
        r"template-item/<int:item_pk>",
        views.template_item_detail,
        name="template-item-detail",
    ),
    path(
        r"template-item/<int:item_pk>/delete",
        views.template_item_delete,
        name="template-item-delete",
    ),
    path(
        r"template-item/<int:item_pk>/edit",
        views.template_item_edit,
        name="template-item-edit",
    ),
    #
    # Events
    #
    path(
        r"template/<int:template_pk>/event/create",
        views.event_create,
        name="event-create",
    ),
    path(r"event/", views.event_list, name="event-list"),
    path(r"event/<int:event_pk>", views.event_detail, name="event-detail"),
    path(
        r"event/<int:event_pk>/toggle-open",
        views.event_toggle_open,
        name="event-toggle-open",
    ),
    path(r"category/<int:category_pk>/items", views.item_list, name="item-list"),
    path(
        r"category/<int:category_pk>/toggle-display-closed-items",
        views.category_toggle_display_closed_items,
        name="category-toggle-display-closed-items",
    ),
    path(
        r"item/<int:item_pk>/toggle-status",
        views.item_toggle_status,
        name="item-toggle-status",
    ),
    path(r"", views.dashboard, name="dashboard"),
]
