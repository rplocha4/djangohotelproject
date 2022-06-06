from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home,
    rooms,
    new_room,
    remove_room,
    edit_room,
    customers,
    edit_customers,
    remove_customers,
    managers,
    add_manager,
    remove_manager,
    edit_manager,
    filters,
    dashboard,
    rooms,
)

app_name = "booking"
urlpatterns = (
    [
        path("", home, name="home"),
        path("room/<int:id>/", rooms, name="rooms"),
        path("new_room/", new_room, name="new_room"),
        path("remove_room/<int:id>", remove_room, name="remove_room"),
        path("room/<int:id>/edit", edit_room, name="edit_room"),
        path("customers/", customers, name="customers"),
        path("rooms/", rooms, name="rooms"),
        path("customers/<int:id>/edit", edit_customers, name="edit_customers"),
        path("remove_customers/<int:id>", remove_customers, name="remove_customers"),
        path("managers/", managers, name="managers"),
        path("add_managers/", add_manager, name="add_managers"),
        path("managers/<int:id>/edit", edit_manager, name="edit_manager"),
        path("remove_manager/<int:id>", remove_manager, name="remove_manager"),
        path("filters/", filters, name="filters"),
        path("dashboard/", dashboard, name="dashboard"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
