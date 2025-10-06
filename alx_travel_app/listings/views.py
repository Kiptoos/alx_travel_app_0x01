# listings/views.py
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Read for anyone; write only for the owner (assumes Listing has `owner` FK to User).
    If your model has a different ownership field or none, adjust or remove this.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "owner", None)
        return owner == request.user if owner is not None else True


class ListingViewSet(viewsets.ModelViewSet):
    """
    CRUD for listings.
    Common query params:
      - search: free-text on title, location, description
      - ordering: price_per_night, -price_per_night, created_at, -created_at
      - min_price / max_price: numeric filters on price_per_night
      - available: true/false (simple filter if you keep a boolean on the model)
    """
    queryset = Listing.objects.all().order_by("-id")
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "location", "description"]
    ordering_fields = ["price_per_night", "created_at", "updated_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        available = self.request.query_params.get("available")

        if min_price:
            qs = qs.filter(price_per_night__gte=min_price)
        if max_price:
            qs = qs.filter(price_per_night__lte=max_price)
        if available is not None:
            val = str(available).lower() in ("true", "1", "yes", "y")
            if hasattr(Listing, "available"):
                qs = qs.filter(available=val)
        return qs

    def perform_create(self, serializer):
        # If your model has `owner`, set it here. Otherwise remove this method.
        owner_field = Listing._meta.get_field("owner") if "owner" in [f.name for f in Listing._meta.fields] else None
        if owner_field:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=["get"], url_path="bookings")
    def bookings(self, request, pk=None):
        """Optional: list bookings for a listing: GET /api/listings/{id}/bookings/"""
        listing = self.get_object()
        qs = Booking.objects.filter(listing=listing).order_by("-start_date")
        page = self.paginate_queryset(qs)
        serializer = BookingSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    CRUD for bookings.
    Query params:
      - listing: filter by listing id
      - from / to: ISO dates to filter bookings that overlap a date range (optional)
    """
    queryset = Booking.objects.select_related("listing").all().order_by("-id")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        listing_id = self.request.query_params.get("listing")
        date_from = self.request.query_params.get("from")
        date_to = self.request.query_params.get("to")

        if listing_id:
            qs = qs.filter(listing_id=listing_id)
        # Optional overlap filter: bookings that intersect [from, to]
        if date_from and date_to:
            qs = qs.filter(start_date__lte=date_to, end_date__gte=date_from)
        return qs

    def perform_create(self, serializer):
        # Optional guardrails: basic validation (no past end date, start <= end)
        start = serializer.validated_data.get("start_date")
        end = serializer.validated_data.get("end_date")
        if start and end and start > end:
            return Response(
                {"detail": "start_date must be before or equal to end_date."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if end and end < timezone.now().date():
            return Response(
                {"detail": "end_date cannot be in the past."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
