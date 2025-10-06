# alx_travel_app_0x01

## Objective
Expose CRUD APIs for Listings and Bookings using Django REST Framework and document them with Swagger.

## Endpoints
- `GET /api/listings/`
- `POST /api/listings/`
- `GET /api/listings/{id}/`
- `PUT /api/listings/{id}/`
- `PATCH /api/listings/{id}/`
- `DELETE /api/listings/{id}/`
- `GET /api/listings/{id}/bookings/` — bookings for a listing
- `GET /api/bookings/`
- `POST /api/bookings/`
- `GET /api/bookings/{id}/`
- `PUT /api/bookings/{id}/`
- `PATCH /api/bookings/{id}/`
- `DELETE /api/bookings/{id}/`

### Query params
- Listings: `search`, `ordering`, `min_price`, `max_price`, `available`
- Bookings: `listing`, `from`, `to`

## Swagger Docs
- Swagger UI: `/swagger/`
- Redoc: `/redoc/`
- JSON schema: `/openapi.json`

## Quickstart
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
