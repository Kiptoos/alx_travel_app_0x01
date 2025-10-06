# alx_travel_app/urls.py  (your project root urls)
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel API",
        default_version="v1",
        description="CRUD APIs for Listings and Bookings",
        contact=openapi.Contact(email="dev@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("listings.urls")),  # mounts /api/listings/ and /api/bookings/
    # Swagger endpoints
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("openapi.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
