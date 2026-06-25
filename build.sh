#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create initial superuser
python manage.py shell -c "
import os
import django
from django.contrib.auth import get_user_model

User = get_user_model()
email = 'admin@hr.com'
password = 'admin123'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print(f'Superuser {email} created successfully.')
"
