from datetime import datetime

import holidays
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, TemplateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from apps.employees.models import Employee

from .models import Attendance
from .forms import AttendanceForm


class AttendancePersonalView(LoginRequiredMixin, ListView):
    template_name = "attendance/personal.html"
    context_object_name = "attendance_history"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(karyawan__user=user).order_by(
            "-tanggal", "-jam_masuk"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()

        context["today"] = today
        id_holidays = holidays.ID()
        context["is_holiday"] = today in id_holidays
        context["holiday_name"] = (
            id_holidays.get(today) if context["is_holiday"] else None
        )
        context["is_weekend"] = today.weekday() >= 5

        try:
            attendance = Attendance.objects.get(
                karyawan__user=user, tanggal=today
            )
            context["has_checked_in"] = True
            context["has_checked_out"] = attendance.jam_keluar is not None
            context["jam_masuk"] = attendance.jam_masuk
            context["jam_keluar"] = attendance.jam_keluar
        except Attendance.DoesNotExist:
            context["has_checked_in"] = False
            context["has_checked_out"] = False

        return context


class AttendanceManagementView(UserPassesTestMixin, TemplateView):
    template_name = "attendance/management.html"

    def test_func(self):
        return self.request.user.role == "HR_ADMIN"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get query parameters
        search_query = self.request.GET.get("search", "")
        date_query = self.request.GET.get("date", "")
        status_query = self.request.GET.get("status", "")

        # Default date is today if not specified
        if not date_query:
            target_date = timezone.localdate()
            context["selected_date"] = target_date.strftime("%Y-%m-%d")
        else:
            try:
                target_date = datetime.strptime(date_query, "%Y-%m-%d").date()
                context["selected_date"] = date_query
            except ValueError:
                target_date = timezone.localdate()
                context["selected_date"] = target_date.strftime("%Y-%m-%d")

        context["search_query"] = search_query
        context["status_query"] = status_query

        employees = Employee.objects.filter(status_aktif=True)
        if search_query:
            employees = employees.filter(nama__icontains=search_query)

        attendances_dict = {
            att.karyawan_id: att
            for att in Attendance.objects.filter(tanggal=target_date)
        }

        combined_history = []
        for emp in employees:
            att = attendances_dict.get(emp.id)
            status_display = att.get_status_display() if att else "Tidak Masuk"

            # Apply status filter
            if status_query:
                # Value matches: TEPAT_WAKTU, TERLAMBAT, ALPA (Tidak Masuk)
                if status_query == "ALPA" and status_display != "Tidak Masuk":
                    continue
                if (
                    status_query == "TEPAT_WAKTU"
                    and status_display != "Tepat Waktu"
                ):
                    continue
                if (
                    status_query == "TERLAMBAT"
                    and status_display != "Terlambat"
                ):
                    continue

            combined_history.append(
                {
                    "id": att.id if att else None,
                    "karyawan": emp,
                    "tanggal": target_date,
                    "jam_masuk": att.jam_masuk if att else None,
                    "jam_keluar": att.jam_keluar if att else None,
                    "status_display": status_display,
                }
            )

        # Basic Manual Pagination (Since we are using a list)
        from django.core.paginator import Paginator

        page_number = self.request.GET.get("page", 1)
        paginator = Paginator(combined_history, 15)  # 15 items per page
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        context["attendance_history"] = page_obj.object_list

        return context

class AttendanceUpdateView(UserPassesTestMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "attendance/form.html"

    def test_func(self):
        return self.request.user.role == "HR_ADMIN"

    def get_object(self, queryset=None):
        emp_id = self.kwargs.get("emp_id")
        date_str = self.kwargs.get("date_str")
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        try:
            return Attendance.objects.get(karyawan_id=emp_id, tanggal=target_date)
        except Attendance.DoesNotExist:
            return Attendance(karyawan_id=emp_id, tanggal=target_date)

    def form_valid(self, form):
        messages.success(self.request, "Data absensi berhasil diperbarui.")
        return super().form_valid(form)
        
    def get_success_url(self):
        date_str = self.kwargs.get("date_str")
        return f"{reverse_lazy('attendance_management')}?date={date_str}"

class AttendanceResetView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == "HR_ADMIN"

    def post(self, request, emp_id, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            attendance = get_object_or_404(Attendance, karyawan_id=emp_id, tanggal=target_date)
            attendance.delete()
            messages.success(request, f"Absensi berhasil direset. Karyawan kini dianggap belum absen pada tanggal {date_str}.")
        except ValueError:
            messages.error(request, "Format tanggal tidak valid.")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")
            
        # Redirect back to management page with same parameters if possible, 
        # or just to the management page
        return redirect(f"{reverse_lazy('attendance_management')}?date={date_str}")

