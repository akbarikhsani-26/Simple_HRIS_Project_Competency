from django.db import models
from django.utils import timezone

from apps.employees.models import Employee


class Attendance(models.Model):
    karyawan = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="attendances"
    )
    tanggal = models.DateField(default=timezone.localdate)
    jam_masuk = models.TimeField(default=timezone.now)
    jam_keluar = models.TimeField(null=True, blank=True)

    STATUS_CHOICES = (
        ("TEPAT_WAKTU", "Tepat Waktu"),
        ("TERLAMBAT", "Terlambat"),
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="TEPAT_WAKTU"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("karyawan", "tanggal")

    def __str__(self):
        return f"{self.karyawan.nama} - {self.tanggal}"
