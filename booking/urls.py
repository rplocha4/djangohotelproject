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
    book_rooms,
    remove_room_from_dashboard,
    view_payments,
    view_bookings,
    view_room_types,
    remove_room_type,
    edit_room_type,
)

app_name = "booking"
urlpatterns = (
    [
        path("", home, name="home"),
        path("rooms/", rooms, name="rooms"),
        path("new_room/", new_room, name="new_room"),
        path("remove_room/<int:id>", remove_room, name="remove_room"),
        path("room/<int:id>/edit", edit_room, name="edit_room"),
        path("customers/", customers, name="customers"),
        path("book_rooms/<int:id>/", book_rooms, name="book_rooms"),
        path("customers/<int:id>/edit", edit_customers, name="edit_customers"),
        path("remove_customers/<int:id>", remove_customers, name="remove_customers"),
        path("managers/", managers, name="managers"),
        path("add_managers/", add_manager, name="add_managers"),
        path("managers/<int:id>/edit", edit_manager, name="edit_manager"),
        path("remove_manager/<int:id>", remove_manager, name="remove_manager"),
        path("filters/", filters, name="filters"),
        path("view_payments/", view_payments, name="view_payments"),
        path("view_bookings/", view_bookings, name="view_bookings"),
        path("dashboard/", dashboard, name="dashboard"),
        path(
            "remove_room_from_dashboard/<int:id>",
            remove_room_from_dashboard,
            name="remove_room_from_dashboard",
        ),
        path("view_room_types/", view_room_types, name="view_room_types"),
        path("edit_room_type/<int:id>/edit", edit_room_type, name="edit_room_type"),
        path("remove_room_type/<int:id>", remove_room_type, name="remove_room_type"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
