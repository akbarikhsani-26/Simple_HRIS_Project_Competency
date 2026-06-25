from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "email",
        "jabatan",
        "tanggal_masuk",
        "status_aktif",
    )
    search_fields = ("nama", "email", "jabatan")
    list_filter = ("jabatan", "status_aktif", "tanggal_masuk")
