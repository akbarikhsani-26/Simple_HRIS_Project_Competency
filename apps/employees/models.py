from django.conf import settings
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    jabatan = models.CharField(max_length=100)
    tanggal_masuk = models.DateField()
    status_aktif = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama} ({self.jabatan})"


class ProfileUpdateRequest(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Menunggu Persetujuan"),
        ("APPROVED", "Disetujui"),
        ("REJECTED", "Ditolak"),
    )

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="update_requests"
    )
    nama_baru = models.CharField(max_length=255)
    email_baru = models.EmailField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pengajuan Update Profil: {self.employee.nama} ({self.get_status_display()})"
