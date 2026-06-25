#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create or update initial superuser
python manage.py shell -c "
import os
import django
from django.contrib.auth import get_user_model

User = get_user_model()
email = 'admin@hr.com'
password = 'admin123'

user, created = User.objects.get_or_create(email=email)
if created:
    user.set_password(password)

user.is_staff = True
user.is_superuser = True
user.role = 'HR_ADMIN'
user.save()
print(f'Superuser {email} role ensured as HR_ADMIN.')
"

# Seed employee dummy data
python manage.py seed_employees
