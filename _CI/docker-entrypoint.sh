#!/bin/bash

python manage.py migrate --no-input

python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8000 rental_platform_demo.wsgi:application --max-requests=50 --workers=4 --timeout=60
