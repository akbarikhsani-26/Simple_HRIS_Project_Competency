import os

project_path = "."

# Create directories
directories = [
    "core",
    "apps/authentication",
    "apps/employees",
    "apps/attendance",
    "static/css",
    "static/js",
    "templates"
]

for d in directories:
    os.makedirs(os.path.join(project_path, d), exist_ok=True)
    if "apps/" in d or "core" == d:
        open(os.path.join(project_path, d, "__init__.py"), "w").close()
open(os.path.join(project_path, "apps", "__init__.py"), "w").close()

# apps/authentication/apps.py
with open(os.path.join(project_path, "apps/authentication", "apps.py"), "w") as f:
    f.write("from django.apps import AppConfig\n\nclass AuthenticationConfig(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = 'apps.authentication'\n")

# apps/employees/apps.py
with open(os.path.join(project_path, "apps/employees", "apps.py"), "w") as f:
    f.write("from django.apps import AppConfig\n\nclass EmployeesConfig(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = 'apps.employees'\n")

# apps/attendance/apps.py
with open(os.path.join(project_path, "apps/attendance", "apps.py"), "w") as f:
    f.write("from django.apps import AppConfig\n\nclass AttendanceConfig(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = 'apps.attendance'\n")

# empty files requested
open(os.path.join(project_path, "apps/authentication", "models.py"), "w").close()
open(os.path.join(project_path, "apps/authentication", "decorators.py"), "w").close()
open(os.path.join(project_path, "apps/authentication", "permissions.py"), "w").close()
open(os.path.join(project_path, "apps/authentication", "views.py"), "w").close()
open(os.path.join(project_path, "apps/authentication", "api_views.py"), "w").close()

open(os.path.join(project_path, "apps/employees", "models.py"), "w").close()
open(os.path.join(project_path, "apps/employees", "views.py"), "w").close()
open(os.path.join(project_path, "apps/employees", "api_views.py"), "w").close()
open(os.path.join(project_path, "apps/employees", "serializers.py"), "w").close()

open(os.path.join(project_path, "apps/attendance", "models.py"), "w").close()
open(os.path.join(project_path, "apps/attendance", "views.py"), "w").close()
open(os.path.join(project_path, "apps/attendance", "api_views.py"), "w").close()
open(os.path.join(project_path, "apps/attendance", "serializers.py"), "w").close()

print("Directories and init files created.")
