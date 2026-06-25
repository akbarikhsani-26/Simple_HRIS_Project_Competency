from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # To be added later
    path("", include("apps.authentication.urls")),
    path("employees/", include("apps.employees.web_urls")),
    path("attendance/", include("apps.attendance.web_urls")),
    path("api/employees/", include("apps.employees.urls")),
    path("api/attendance/", include("apps.attendance.urls")),
]
