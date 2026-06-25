from django.urls import path

from .views import (
    AttendanceManagementView,
    AttendancePersonalView,
    AttendanceUpdateView,
    AttendanceResetView,
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
    path(
        "management/<int:emp_id>/<str:date_str>/reset/",
        AttendanceResetView.as_view(),
        name="attendance_reset",
    ),
]
