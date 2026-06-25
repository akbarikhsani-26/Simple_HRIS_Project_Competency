from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.authentication.models import CustomUser

from .models import Employee


class HRAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "HR_ADMIN"


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "employees/list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == "HR_ADMIN":
            return Employee.objects.all().order_by("-created_at")
        return Employee.objects.filter(user=user)


class EmployeeCreateView(LoginRequiredMixin, HRAdminRequiredMixin, CreateView):
    model = Employee
    template_name = "employees/form.html"
    success_url = reverse_lazy("employee_list")

    def get_form_class(self):
        from django import forms

        class EmployeeCreateForm(forms.ModelForm):
            password = forms.CharField(
                widget=forms.PasswordInput(),
                help_text="Password untuk login karyawan.",
            )

            class Meta:
                model = Employee
                fields = [
                    "nama",
                    "email",
                    "jabatan",
                    "tanggal_masuk",
                    "status_aktif",
                ]

        return EmployeeCreateForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "role": "EMPLOYEE",
            },
        )
        if created:
            user.set_password(password)
            user.save()

        form.instance.user = user
        messages.success(self.request, "Karyawan berhasil ditambahkan.")
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, HRAdminRequiredMixin, UpdateView):
    model = Employee
    template_name = "employees/form.html"
    success_url = reverse_lazy("employee_list")

    def get_form_class(self):
        from django import forms

        class EmployeeForm(forms.ModelForm):
            password = forms.CharField(
                widget=forms.PasswordInput(),
                required=False,
                help_text="Kosongkan jika tidak ingin mengubah password.",
            )

            class Meta:
                model = Employee
                fields = [
                    "nama",
                    "email",
                    "jabatan",
                    "tanggal_masuk",
                    "status_aktif",
                ]

        return EmployeeForm

    def get_queryset(self):
        return Employee.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Profil karyawan berhasil diperbarui.")

        # Jika email diubah, update juga di model CustomUser
        if "email" in form.changed_data:
            form.instance.user.email = form.cleaned_data["email"]

        # Jika password diisi, ubah passwordnya
        password = form.cleaned_data.get("password")
        if password:
            form.instance.user.set_password(password)

        form.instance.user.save()
        return super().form_valid(form)


class EmployeeDeleteView(LoginRequiredMixin, HRAdminRequiredMixin, DeleteView):
    model = Employee
    template_name = "employees/confirm_delete.html"
    success_url = reverse_lazy("employee_list")

    def form_valid(self, form):
        messages.success(self.request, "Karyawan berhasil dihapus.")
        # Hapus user terkait
        self.object.user.delete()
        return super().form_valid(form)
