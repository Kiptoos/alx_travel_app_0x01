# alx_travel_app/listings/views.py

from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingCreateSerializer, BookingSerializer

class ListingListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: list active listings
    POST: create a listing (host is taken from request.user)
    """
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class ListingRetrieveAPIView(generics.RetrieveAPIView):
    """
    GET: retrieve a single listing by pk
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]


class BookingCreateAPIView(generics.CreateAPIView):
    """
    POST: create a booking. If authenticated, guest is set to request.user.
    """
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # set the guest to the authenticated user
        serializer.save(guest=self.request.user)


class BookingRetrieveAPIView(generics.RetrieveAPIView):
    """
    GET: retrieve booking details (only owner or staff should access in real apps)
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        # basic protection: only guest or host or staff can view
        user = self.request.user
        if user.is_staff or obj.guest == user or obj.listing.host == user:
            return obj
        # else, return 404 to avoid leaking existence
        raise generics.Http404


class UserBookingListAPIView(generics.ListAPIView):
    """
    GET: list bookings for the authenticated user (as guest)
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user).order_by("-created_at")
