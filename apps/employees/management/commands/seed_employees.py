import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from apps.employees.models import Employee

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with dummy employees"

    def handle(self, *args, **kwargs):
        fake = Faker("id_ID")  # Using Indonesian locale for realistic names

        # 1. Ensure admin account exists
        admin_email = "admin@hr.com"
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email, password="admin123", role="HR_ADMIN"
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created HR_ADMIN account: {admin_email}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"HR_ADMIN account {admin_email} already exists."
                )
            )

        # 1.5 Create specific documented dummy users (from README)
        fixed_users = [
            ("fnarpati@example.com", "Fajar Narpati"),
            ("galur93@example.net", "Galur Hidayat"),
            ("rpangestu@example.net", "Restu Pangestu"),
        ]
        
        for f_email, f_name in fixed_users:
            if not User.objects.filter(email=f_email).exists():
                try:
                    user = User.objects.create_user(
                        email=f_email, password="password123", role="EMPLOYEE"
                    )
                    Employee.objects.create(
                        user=user,
                        nama=f_name,
                        email=f_email,
                        jabatan="Staff IT",
                        tanggal_masuk=fake.date_between(start_date="-5y", end_date="today"),
                        status_aktif=True,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created fixed employee: {f_email}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed fixed user {f_email}: {e}"))

        # 2. Generate 30 dummy employees
        num_employees = 30
        jabatan_choices = [
            "Staff IT",
            "HR Staff",
            "Marketing",
            "Sales",
            "Finance",
            "Operations",
            "Designer",
        ]
        created_count = 0
        for _ in range(num_employees):
            nama = fake.name()
            # Generate a unique email
            email = fake.unique.email()

            # Create CustomUser for employee
            try:
                user = User.objects.create_user(
                    email=email, password="password123", role="EMPLOYEE"
                )

                # Create Employee profile
                tanggal_masuk = fake.date_between(
                    start_date="-5y", end_date="today"
                )
                Employee.objects.create(
                    user=user,
                    nama=nama,
                    email=email,
                    jabatan=random.choice(jabatan_choices),
                    tanggal_masuk=tanggal_masuk,
                    status_aktif=True,
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to create employee {nama}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {created_count} employees."
            )
        )
