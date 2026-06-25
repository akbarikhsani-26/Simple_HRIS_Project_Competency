from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['jam_masuk', 'jam_keluar', 'status']
        widgets = {
            'jam_masuk': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'jam_keluar': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
