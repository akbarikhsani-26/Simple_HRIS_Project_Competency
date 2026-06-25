from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authentication.permissions import IsHRAdminOrReadOnlyOwnData

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsHRAdminOrReadOnlyOwnData]
    filter_backends = [filters.SearchFilter]
    search_fields = ["nama", "jabatan"]

    def get_queryset(self):
        """
        HR_ADMIN sees all employees.
        EMPLOYEE sees only their own employee profile.
        """
        user = self.request.user
        if user.role == "HR_ADMIN":
            return Employee.objects.all()
        return Employee.objects.filter(user=user)
