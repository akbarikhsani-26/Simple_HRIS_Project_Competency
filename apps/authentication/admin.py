from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_staff", "is_active")
    search_fields = ("email",)
    list_filter = ("role", "is_staff", "is_active")
