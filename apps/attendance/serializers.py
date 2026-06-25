from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    karyawan_nama = serializers.CharField(
        source="karyawan.nama", read_only=True
    )
    karyawan_jabatan = serializers.CharField(
        source="karyawan.jabatan", read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "karyawan",
            "karyawan_nama",
            "karyawan_jabatan",
            "tanggal",
            "jam_masuk",
            "jam_keluar",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "karyawan",
            "tanggal",
            "jam_masuk",
            "jam_keluar",
            "created_at",
        ]
