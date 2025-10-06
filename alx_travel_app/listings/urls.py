# alx_travel_app/listings/urls.py

from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path("listings/", views.ListingListCreateAPIView.as_view(), name="listing-list-create"),
    path("listings/<int:pk>/", views.ListingRetrieveAPIView.as_view(), name="listing-detail"),
    path("bookings/", views.BookingCreateAPIView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", views.BookingRetrieveAPIView.as_view(), name="booking-detail"),
    path("my-bookings/", views.UserBookingListAPIView.as_view(), name="user-bookings"),
]
