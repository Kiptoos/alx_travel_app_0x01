# Milestone 2 — Models, Serializers, and Seeder

This package contains the Django models, DRF serializers, and a management command to seed the database for the ALX travel app exercise.

## Files included
- `alx_travel_app/listings/models.py` — Listing, Booking, Review models
- `alx_travel_app/listings/serializers.py` — DRF serializers for Listing and Booking
- `alx_travel_app/listings/management/commands/seed.py` — Management command to seed the DB
- `requirements.txt` — minimal requirements for running the seeder locally

## Quick setup
1. Duplicate project to `alx_travel_app_0x00` and place this `alx_travel_app` inside.
2. Create & activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # on Windows use venv\\Scripts\\activate
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py makemigrations listings
   python manage.py migrate
   ```
5. (Optional) Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run seed:
   ```
   python manage.py seed --users 5 --listings 12 --bookings 20 --reviews 30
   ```

## Notes
- The seeder uses `Faker`. Default seeder user password is `password123`.
- Adjust values as needed for your environment.
