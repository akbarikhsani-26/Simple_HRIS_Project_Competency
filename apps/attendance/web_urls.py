from django.urls import path

from .views import (
    AttendanceManagementView,
    AttendancePersonalView,
    AttendanceUpdateView,
)

urlpatterns = [
    path("", AttendancePersonalView.as_view(), name="attendance_personal"),
    path(
        "management/",
        AttendanceManagementView.as_view(),
        name="attendance_management",
    ),
    path(
        "management/<int:emp_id>/<str:date_str>/edit/",
        AttendanceUpdateView.as_view(),
        name="attendance_edit",
    ),
]
