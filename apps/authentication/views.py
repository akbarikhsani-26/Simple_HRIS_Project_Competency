import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from apps.attendance.models import Attendance
from apps.employees.models import Employee


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "login"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Determine target month
        import calendar
        from datetime import datetime

        import holidays

        month_query = self.request.GET.get("month", "")
        day_query = self.request.GET.get("day", "")
        today = timezone.localdate()

        target_year, target_month = today.year, today.month
        target_date = today
        is_daily_filter = False

        if day_query:
            try:
                target_year, target_month, target_day = map(
                    int, day_query.split("-")
                )
                target_date = datetime(
                    target_year, target_month, target_day
                ).date()
                is_daily_filter = True
            except ValueError:
                pass
        elif month_query:
            try:
                target_year, target_month = map(int, month_query.split("-"))
                target_date = datetime(target_year, target_month, 1).date()
            except ValueError:
                pass

        context["selected_month"] = f"{target_year}-{target_month:02d}"
        if is_daily_filter:
            context["selected_day"] = (
                f"{target_year}-{target_month:02d}-{target_day:02d}"
            )
            context["month_name"] = target_date.strftime("%d %B %Y")
            days_range = [target_day]
        else:
            context["selected_day"] = ""
            context["month_name"] = target_date.strftime("%B %Y")
            _, days_in_month = calendar.monthrange(target_year, target_month)
            days_range = range(1, days_in_month + 1)

        if user.role == "HR_ADMIN":
            # 1. Statistik Dasar
            context["total_employees"] = Employee.objects.count()
            context["active_employees"] = Employee.objects.filter(
                status_aktif=True
            ).count()

            # 2. Grafik 1: Karyawan per Jabatan
            jabatan_data = Employee.objects.values("jabatan").annotate(
                total=Count("id")
            )
            context["chart_jabatan_labels"] = json.dumps(
                [item["jabatan"] for item in jabatan_data]
            )
            context["chart_jabatan_data"] = json.dumps(
                [item["total"] for item in jabatan_data]
            )

            # 3. Grafik 2: Rekap Kehadiran (Bulan/Hari Ini)
            attendance_labels = []
            tepat_waktu_counts = []
            terlambat_counts = []
            alpa_counts = []

            id_holidays = holidays.ID()

            for day in days_range:
                current_day = datetime(target_year, target_month, day).date()
                if current_day > today and not is_daily_filter:
                    break  # Don't show future days unless specifically selected

                attendance_labels.append(str(day))

                day_attendances = Attendance.objects.filter(
                    tanggal=current_day
                )
                tepat = day_attendances.filter(status="TEPAT_WAKTU").count()
                terlambat = day_attendances.filter(status="TERLAMBAT").count()

                # Hitung Alpa (hanya jika hari kerja)
                alpa = 0
                if (
                    current_day.weekday() < 5
                    and current_day not in id_holidays
                ):
                    alpa = context["active_employees"] - (tepat + terlambat)
                    if alpa < 0:
                        alpa = 0

                tepat_waktu_counts.append(tepat)
                terlambat_counts.append(terlambat)
                alpa_counts.append(alpa)

            context["chart_attendance_labels"] = json.dumps(attendance_labels)
            context["chart_tepat_waktu_data"] = json.dumps(tepat_waktu_counts)
            context["chart_terlambat_data"] = json.dumps(terlambat_counts)
            context["chart_alpa_data"] = json.dumps(alpa_counts)
        else:
            # Chart untuk Karyawan
            id_holidays = holidays.ID()

            try:
                karyawan = user.employee_profile
                attendances = Attendance.objects.filter(
                    karyawan=karyawan,
                    tanggal__year=target_year,
                    tanggal__month=target_month,
                )

                if is_daily_filter:
                    attendances = attendances.filter(tanggal__day=target_day)

                tepat_waktu = attendances.filter(status="TEPAT_WAKTU").count()
                terlambat = attendances.filter(status="TERLAMBAT").count()

                # Hitung hari kerja wajib
                hari_kerja = 0
                for day in days_range:
                    current_day = datetime(
                        target_year, target_month, day
                    ).date()
                    if current_day > today and not is_daily_filter:
                        break  # Stop at today

                    # Skip if weekend or holiday
                    if (
                        current_day.weekday() < 5
                        and current_day not in id_holidays
                    ):
                        hari_kerja += 1

                alpa = hari_kerja - (tepat_waktu + terlambat)
                if alpa < 0:
                    alpa = 0

                context["emp_chart_labels"] = json.dumps(
                    ["Tepat Waktu", "Terlambat", "Tidak Masuk (Hari Kerja)"]
                )
                context["emp_chart_data"] = json.dumps(
                    [tepat_waktu, terlambat, alpa]
                )

            except Employee.DoesNotExist:
                context["emp_chart_labels"] = json.dumps([])
                context["emp_chart_data"] = json.dumps([])

        return context
